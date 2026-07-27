#!/usr/bin/env bash
# ============================================================================
# OCI Resource Setup — AprendeYa Agent Deployment
# ============================================================================
# Prereqs: OCI CLI installed, configured with ~/.oci/config
# Usage:   bash oci/setup-oci-resources.sh <COMPARTMENT_OCID> <REGION>
# ============================================================================
set -euo pipefail

COMPARTMENT_ID="$1"
REGION="${2:-us-ashburn-1}"
DISPLAY_NAME="aprendeya-agent"

echo "=== OCI Resource Setup: $DISPLAY_NAME ==="
echo "Compartment: $COMPARTMENT_ID"
echo "Region:      $REGION"
echo ""

# ------------------------------------------------------------------
# 1. VCN + Subnets + Internet Gateway
# ------------------------------------------------------------------
echo "--- 1. Creando VCN ---"
VCN_ID=$(oci network vcn create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-vcn" \
  --cidr-block "10.0.0.0/16" \
  --query "data.id" --raw-output)
echo "VCN: $VCN_ID"

IG_ID=$(oci network internet-gateway create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-igw" \
  --is-enabled true \
  --query "data.id" --raw-output)
echo "Internet Gateway: $IG_ID"

RT_ID=$(oci network route-table list \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --query "data[0].id" --raw-output)

oci network route-table update \
  --rt-id "$RT_ID" \
  --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG_ID\"}]" \
  --force > /dev/null
echo "Route table updated"

PUBLIC_SUBNET_ID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-public-subnet" \
  --cidr-block "10.0.1.0/24" \
  --route-table-id "$RT_ID" \
  --query "data.id" --raw-output)
echo "Public Subnet: $PUBLIC_SUBNET_ID"

# ------------------------------------------------------------------
# 2. Network Security Group (allow 8000 from anywhere)
# ------------------------------------------------------------------
echo "--- 2. Creando NSG ---"
NSG_ID=$(oci network network-security-group create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-nsg" \
  --query "data.id" --raw-output)

oci network network-security-group add-security-rules \
  --network-security-group-id "$NSG_ID" \
  --security-rules "[
    {\"description\":\"HTTP API\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"0.0.0.0/0\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":8000,\"max\":8000}}},
    {\"description\":\"Health checks\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"0.0.0.0/0\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":8080,\"max\":8080}}}
  ]" > /dev/null
echo "NSG: $NSG_ID (ports 8000, 8080 open)"

# ------------------------------------------------------------------
# 3. Object Storage Bucket (for raw documents)
# ------------------------------------------------------------------
echo "--- 3. Creando Object Storage Bucket ---"
NS_NAME=$(oci os ns get --query "data" --raw-output)
BUCKET_NAME="${DISPLAY_NAME}-docs"

oci os bucket create \
  --compartment-id "$COMPARTMENT_ID" \
  --name "$BUCKET_NAME" \
  --namespace-name "$NS_NAME" > /dev/null
echo "Bucket: $BUCKET_NAME (namespace: $NS_NAME)"

# ------------------------------------------------------------------
# 4. Vault + Secret for GROQ_API_KEY
# ------------------------------------------------------------------
echo "--- 4. Creando Vault y Secret ---"
VAULT_ID=$(oci kms management vault create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-vault" \
  --vault-type "DEFAULT" \
  --query "data.id" --raw-output)

echo "Vault created: $VAULT_ID (provisioning may take a minute)..."
sleep 60

KEY_ID=$(oci kms management key create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-key" \
  --key-shape "{\"algorithm\":\"AES\",\"length\":32}" \
  --query "data.id" --raw-output)
echo "Key: $KEY_ID"

echo ""
echo "=== MANUAL STEP: Store your GROQ_API_KEY ==="
echo "Read the secret value from user input, then run:"
echo ""
echo 'read -s GROQ_KEY'
echo "echo \"\$GROQ_KEY\" | base64 > /tmp/secret.b64"
echo ""
echo "SECRET_ID=\$(oci kms management secret create \\"
echo "  --compartment-id \"$COMPARTMENT_ID\" \\"
echo "  --key-id \"$KEY_ID\" \\"
echo "  --secret-name \"${DISPLAY_NAME}-groq-key\" \\"
echo "  --description \"Groq API Key for AprendeYa Agent\" \\"
echo "  --secret-content-content-type \"BASE64\" \\"
echo "  --secret-content-name \"groq_api_key\" \\"
echo "  --secret-content \"\$(cat /tmp/secret.b64)\" \\"
echo "  --query \"data.id\" --raw-output)"
echo ""

# ------------------------------------------------------------------
# 5. Container Instance
# ------------------------------------------------------------------
echo "--- 5. Desplegando Container Instance ---"
echo "Primero construye y sube la imagen a OCIR:"
echo ""
echo "docker build -t aprendeya-agent:latest ."
echo ""
echo "docker tag aprendeya-agent:latest ${REGION}.ocir.io/${NS_NAME}/${DISPLAY_NAME}:latest"
echo "oci iam availability-domain list --compartment-id \"$COMPARTMENT_ID\" --query \"data[0].name\" --raw-output"
echo "docker push ${REGION}.ocir.io/${NS_NAME}/${DISPLAY_NAME}:latest"
echo ""

AD=$(oci iam availability-domain list \
  --compartment-id "$COMPARTMENT_ID" \
  --query "data[0].name" --raw-output)

echo "Availability Domain: $AD"
echo ""
echo "Luego despliega el Container Instance con:"
echo ""
echo "oci compute-container-instance container-instance create \\"
echo "  --compartment-id \"$COMPARTMENT_ID\" \\"
echo "  --display-name \"${DISPLAY_NAME}-ci\" \\"
echo "  --availability-domain \"$AD\" \\"
echo "  --shape \"CI.Standard.E4.Flex\" \\"
echo "  --shape-config '{\"ocpus\":2,\"memoryInGBs\":8}' \\"
echo "  --vnic \"{\\\"subnetId\\\":\\\"$PUBLIC_SUBNET_ID\\\",\\\"assignPublicIp\\\":true,\\\"nsgIds\\\":[\\\"$NSG_ID\\\"]}\" \\"
echo "  --container \"{\\\"displayName\\\":\\\"${DISPLAY_NAME}-container\\\",\\\"imageUrl\\\":\\\"${REGION}.ocir.io/${NS_NAME}/${DISPLAY_NAME}:latest\\\",\\\"healthChecks\\\":[{\\\"action\\\":\\\"NONE\\\",\\\"healthCheckType\\\":\\\"HTTP\\\",\\\"port\\\":8000,\\\"path\\\":\\\"/health\\\",\\\"intervalInSeconds\\\":30,\\\"failureThreshold\\\":3}],\\\"environmentVariables\\\":{\\\"OCI_VAULT_SECRET_ID\\\":\\\"\\\"}}\" \\"
echo "  --is-public-ip-assigned true"

echo ""
echo "=== RECURSOS OCI CREADOS ==="
echo "VCN:            $VCN_ID"
echo "Subnet:         $PUBLIC_SUBNET_ID"
echo "NSG:            $NSG_ID"
echo "Bucket:         $BUCKET_NAME"
echo "Vault:          $VAULT_ID"
echo "Key:            $KEY_ID"
