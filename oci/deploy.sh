#!/usr/bin/env bash
# ============================================================================
# Deploy AprendeYa Agent to OCI Container Instance
# ============================================================================
# Usage:
#   1. bash oci/setup-oci-resources.sh <COMPARTMENT_OCID>   (primera vez)
#   2. bash oci/deploy.sh <COMPARTMENT_OCID> <REGION>
# ============================================================================
set -euo pipefail

COMPARTMENT_ID="$1"
REGION="${2:-us-ashburn-1}"
DISPLAY_NAME="aprendeya-agent"

# ── 1. Config ─────────────────────────────────────────────────────────────
NS_NAME=$(oci os ns get --query "data" --raw-output)
OCIR_BASE="${REGION}.ocir.io/${NS_NAME}/${DISPLAY_NAME}"
IMAGE_TAG="${OCIR_BASE}:$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')"

echo "=== Deploy AprendeYa Agent ==="
echo "Region:       $REGION"
echo "Namespace:    $NS_NAME"
echo "Image:        $IMAGE_TAG"
echo ""

# ── 2. Build + Push to OCIR ──────────────────────────────────────────────
echo "--- Building Docker image ---"
docker build \
  --cache-from "${OCIR_BASE}:latest" \
  -t "${DISPLAY_NAME}:latest" \
  -t "${IMAGE_TAG}" \
  -t "${OCIR_BASE}:latest" \
  .

echo "--- Pushing to OCIR ---"
docker push "${IMAGE_TAG}"
docker push "${OCIR_BASE}:latest"

# ── 3. Get or create Container Instance ──────────────────────────────────
AD=$(oci iam availability-domain list \
  --compartment-id "$COMPARTMENT_ID" \
  --query "data[0].name" --raw-output)

SUBNET_ID=$(oci network subnet list \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-public-subnet" \
  --query "data[0].id" --raw-output)

NSG_ID=$(oci network network-security-group list \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-nsg" \
  --query "data[0].id" --raw-output)

VAULT_SECRET_ID=$(oci kms management secret list \
  --compartment-id "$COMPARTMENT_ID" \
  --name "${DISPLAY_NAME}-groq-key" \
  --query "data[0].id" --raw-output 2>/dev/null || echo "")

if [ -z "$VAULT_SECRET_ID" ]; then
  echo "ADVERTENCIA: No se encontró el secreto GROQ_API_KEY en OCI Vault."
  echo "Configúralo con: bash oci/setup-oci-resources.sh $COMPARTMENT_ID"
  echo "O pásalo directamente en la variable GROQ_API_KEY del container."
fi

# ── 4. Deploy / Update Container Instance ────────────────────────────────
CI_ID=$(oci compute-container-instance container-instance list \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-ci" \
  --query "data[0].id" --raw-output 2>/dev/null || echo "")

if [ -z "$CI_ID" ]; then
  echo "--- Creating Container Instance ---"
  oci compute-container-instance container-instance create \
    --compartment-id "$COMPARTMENT_ID" \
    --display-name "${DISPLAY_NAME}-ci" \
    --availability-domain "$AD" \
    --shape "CI.Standard.E4.Flex" \
    --shape-config '{"ocpus":2,"memoryInGBs":8}' \
    --vnic "{\"subnetId\":\"$SUBNET_ID\",\"assignPublicIp\":true,\"nsgIds\":[\"$NSG_ID\"]}" \
    --container "{\
      \"displayName\":\"${DISPLAY_NAME}-container\",\
      \"imageUrl\":\"${IMAGE_TAG}\",\
      \"healthChecks\":[{\"action\":\"NONE\",\"healthCheckType\":\"HTTP\",\"port\":8000,\"path\":\"/health\",\"intervalInSeconds\":30,\"failureThreshold\":3}],\
      \"environmentVariables\":{\"GROQ_API_KEY\":\"${GROQ_API_KEY:-}\",\"OCI_VAULT_SECRET_ID\":\"${VAULT_SECRET_ID}\"}\
    }" \
    --is-public-ip-assigned true
else
  echo "--- Updating Container Instance ---"
  oci compute-container-instance container-instance update \
    --container-instance-id "$CI_ID" \
    --containers "[{\
      \"displayName\":\"${DISPLAY_NAME}-container\",\
      \"imageUrl\":\"${IMAGE_TAG}\",\
      \"environmentVariables\":{\"GROQ_API_KEY\":\"${GROQ_API_KEY:-}\",\"OCI_VAULT_SECRET_ID\":\"${VAULT_SECRET_ID}\"}\
    }]" \
    --force
fi

# ── 5. Wait for health ───────────────────────────────────────────────────
echo ""
echo "--- Waiting for health check ---"
sleep 15

CI_ID=$(oci compute-container-instance container-instance list \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-ci" \
  --query "data[0].id" --raw-output)

PUBLIC_IP=$(oci compute-container-instance container-instance get \
  --container-instance-id "$CI_ID" \
  --query "data.\"vnics\"[0].\"public-ip\"" --raw-output)

for i in $(seq 1 24); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://${PUBLIC_IP}:8000/health" 2>/dev/null || echo "000")
  if [ "$STATUS" = "200" ]; then
    echo "=== DEPLOY EXITOSO ==="
    echo "API:     http://${PUBLIC_IP}:8000/"
    echo "Health:  http://${PUBLIC_IP}:8000/health"
    echo "Ask:     curl -X POST http://${PUBLIC_IP}:8000/ask -H 'Content-Type: application/json' -d '{\"question\":\"que es el NPS?\"}'"
    exit 0
  fi
  echo "  Esperando... (intento $i, status $STATUS)"
  sleep 5
done

echo "Health check falló después de 2 minutos"
echo "Revisa los logs: oci compute-container-instance container-instance get --container-instance-id $CI_ID"
exit 1
