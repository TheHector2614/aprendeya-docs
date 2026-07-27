#!/usr/bin/env bash
# ============================================================================
# Deploy AprendeYa Agent to OCI
# ============================================================================
# Builds Docker image, pushes to OCIR, creates/updates Container Instance
# in private subnet, and registers it with the Load Balancer.
#
# Usage: bash oci/deploy.sh [COMPARTMENT_OCID] [REGION]
#   Resources are loaded from oci/.oci-resources if exists (from setup script).
# ============================================================================
set -euo pipefail

# ── 1. Load resource IDs ───────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOURCE_FILE="$SCRIPT_DIR/.oci-resources"

if [ -f "$RESOURCE_FILE" ]; then
  source "$RESOURCE_FILE"
else
  COMPARTMENT_ID="${1:?Usage: deploy.sh <COMPARTMENT_OCID> [REGION]}"
  REGION="${2:-us-ashburn-1}"
  # Auto-discover resources
  echo "No .oci-resources found, discovering from OCI..."
  DISPLAY_NAME="aprendeya-agent"
  NS_NAME=$(oci os ns get --query "data" --raw-output)
  PRIVATE_SUBNET_ID=$(oci network subnet list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-private-subnet" --query "data[0].id" --raw-output)
  CI_NSG_ID=$(oci network network-security-group list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-ci-nsg" --query "data[0].id" --raw-output)
  LB_ID=$(oci lb load-balancer list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-lb" --query "data[0].id" --raw-output)
  LB_BACKEND_SET="${DISPLAY_NAME}-bs"
  BUCKET_NAME="${DISPLAY_NAME}-docs"
fi

COMPARTMENT_ID="${COMPARTMENT_ID:-${1:?Usage: deploy.sh <COMPARTMENT_OCID> [REGION]}}"
REGION="${REGION:-${2:-us-ashburn-1}}"
DISPLAY_NAME="${DISPLAY_NAME:-aprendeya-agent}"
NS_NAME="${OBJECT_STORAGE_NS:-$(oci os ns get --query "data" --raw-output)}"
PRIVATE_SUBNET_ID="${PRIVATE_SUBNET_ID:-$(oci network subnet list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-private-subnet" --query "data[0].id" --raw-output)}"
CI_NSG_ID="${CI_NSG_ID:-$(oci network network-security-group list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-ci-nsg" --query "data[0].id" --raw-output)}"
LB_ID="${LB_ID:-$(oci lb load-balancer list --compartment-id "$COMPARTMENT_ID" --display-name "${DISPLAY_NAME}-lb" --query "data[0].id" --raw-output)}"
LB_BACKEND_SET="${LB_BACKEND_SET:-${DISPLAY_NAME}-bs}"
BUCKET_NAME="${BUCKET_NAME:-${DISPLAY_NAME}-docs}"

OCIR_BASE="${REGION}.ocir.io/${NS_NAME}/${DISPLAY_NAME}"
SHORT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
IMAGE_TAG="${OCIR_BASE}:${SHORT_SHA}"

echo "=== Deploy AprendeYa Agent ==="
echo "Region:       $REGION"
echo "Image:        $IMAGE_TAG"
echo "Private subnet: $PRIVATE_SUBNET_ID"
echo ""

# ── 2. Build + Push ────────────────────────────────────────────────────
echo "--- Building ---"
docker build \
  --cache-from "${OCIR_BASE}:latest" \
  -t "${DISPLAY_NAME}:${SHORT_SHA}" \
  -t "${IMAGE_TAG}" \
  -t "${OCIR_BASE}:latest" \
  .

echo "--- Pushing to OCIR ---"
docker push "${IMAGE_TAG}"
docker push "${OCIR_BASE}:latest"

# ── 3. Get Vault secret ────────────────────────────────────────────────
VAULT_SECRET_ID="${OCI_VAULT_SECRET_ID:-}"
if [ -z "$VAULT_SECRET_ID" ]; then
  VAULT_SECRET_ID=$(oci kms management secret list \
    --compartment-id "$COMPARTMENT_ID" \
    --name "${DISPLAY_NAME}-groq-key" \
    --query "data[0].id" --raw-output 2>/dev/null || echo "")
fi

ENV_JSON='{}'
if [ -n "$VAULT_SECRET_ID" ]; then
  ENV_JSON="{\"OCI_VAULT_SECRET_ID\":\"${VAULT_SECRET_ID}\",\"OCI_OBJECT_STORAGE_BUCKET\":\"${BUCKET_NAME}\",\"OCI_OBJECT_STORAGE_NAMESPACE\":\"${NS_NAME}\"}"
else
  echo "WARNING: No GROQ_API_KEY secret found in Vault."
  echo "Set it manually or pass GROQ_API_KEY as env var."
  ENV_JSON="{\"OCI_OBJECT_STORAGE_BUCKET\":\"${BUCKET_NAME}\",\"OCI_OBJECT_STORAGE_NAMESPACE\":\"${NS_NAME}\"}"
fi

# ── 4. Deploy / Update Container Instance ──────────────────────────────
AD=$(oci iam availability-domain list --compartment-id "$COMPARTMENT_ID" --query "data[0].name" --raw-output)
CI_ID=$(oci compute-container-instance container-instance list \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-ci" \
  --query "data[0].id" --raw-output 2>/dev/null || echo "")

CI_CONTAINER=$(cat <<JSON
{
  "displayName":"${DISPLAY_NAME}-container",
  "imageUrl":"${IMAGE_TAG}",
  "healthChecks":[{
    "action":"NONE",
    "healthCheckType":"HTTP",
    "port":8000,
    "path":"/health",
    "intervalInSeconds":30,
    "failureThreshold":3
  }],
  "environmentVariables":${ENV_JSON}
}
JSON
)

CI_VNIC=$(cat <<JSON
{
  "subnetId":"${PRIVATE_SUBNET_ID}",
  "assignPublicIp":false,
  "nsgIds":["${CI_NSG_ID}"]
}
JSON
)

if [ -z "$CI_ID" ]; then
  echo "--- Creating Container Instance ---"
  CI_ID=$(oci compute-container-instance container-instance create \
    --compartment-id "$COMPARTMENT_ID" \
    --display-name "${DISPLAY_NAME}-ci" \
    --availability-domain "$AD" \
    --shape "CI.Standard.E4.Flex" \
    --shape-config '{"ocpus":2,"memoryInGBs":8}' \
    --vnic "$(echo "$CI_VNIC" | tr -d '\n')" \
    --container "$(echo "$CI_CONTAINER" | tr -d '\n')" \
    --is-public-ip-assigned false \
    --query "data.id" --raw-output)
  echo "Created CI: $CI_ID"
else
  echo "--- Updating Container Instance ---"
  oci compute-container-instance container-instance update \
    --container-instance-id "$CI_ID" \
    --containers "[$(echo "$CI_CONTAINER" | tr -d '\n')]" \
    --force > /dev/null
  echo "Updated CI: $CI_ID"
fi

# ── 5. Register container with Load Balancer ───────────────────────────
echo "--- Registering with Load Balancer ---"

# Get the container's private IP
sleep 10
CI_PRIVATE_IP=$(oci compute-container-instance container-instance get \
  --container-instance-id "$CI_ID" \
  --query "data.\"vnics\"[0].\"private-ip\"" --raw-output)
echo "Container private IP: $CI_PRIVATE_IP"

# Remove old backends (if any) and add the new one
oci lb backend-set update \
  --load-balancer-id "$LB_ID" \
  --backend-set-name "$LB_BACKEND_SET" \
  --backends "[{\"ipAddress\":\"${CI_PRIVATE_IP}\",\"port\":8000,\"weight\":1,\"drain\":false}]" \
  --health-checker '{"protocol":"HTTP","port":8000,"urlPath":"/health","intervalMs":30000,"timeoutInMillis":5000,"retries":3,"returnCode":200}' \
  --policy "ROUND_ROBIN" \
  --force > /dev/null
echo "Backend registered: $CI_PRIVATE_IP:8000"

# ── 6. Health check via LB ─────────────────────────────────────────────
echo ""
echo "--- Health check via Load Balancer ---"
LB_IP=$(oci lb load-balancer get --load-balancer-id "$LB_ID" --query "data.\"ip-addresses\"[0].\"ip-address\"" --raw-output)

for i in $(seq 1 30); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://${LB_IP}:80/health" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    echo ""
    echo "=== DEPLOY EXITOSO ==="
    echo "LB URL:    http://${LB_IP}:80/"
    echo "Health:    http://${LB_IP}:80/health"
    echo "Ask:       curl -X POST http://${LB_IP}:80/ask -H 'Content-Type: application/json' -d '{\"question\":\"que es el NPS?\"}'"
    echo ""
    echo "Para agregar HTTPS, subí un certificado al LB:"
    echo "  oci lb certificate create --load-balancer-id $LB_ID --certificate-name <name> --certificate-file cert.pem --private-key-file key.pem"
    echo "  oci lb listener update --load-balancer-id $LB_ID --listener-name ${DISPLAY_NAME}-http-listener --port 443 --protocol HTTP --ssl-certificate-name <name>"
    exit 0
  fi
  echo "  Esperando... (intento $i, status $STATUS)"
  sleep 5
done

echo "Health check falló después de 150s"
echo "Revisá logs del container:"
echo "  oci compute-container-instance container-instance get --container-instance-id $CI_ID"
exit 1
