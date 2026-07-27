#!/usr/bin/env bash
# ============================================================================
# OCI Resource Setup — AprendeYa Agent
# ============================================================================
# Crea toda la infraestructura necesaria en OCI:
#   VCN, 2 subnets, NAT GW, Service GW, NSGs, Object Storage, Vault, LB
#
# Prereqs: OCI CLI instalado y configurado
# Usage:   bash oci/setup-oci-resources.sh <COMPARTMENT_OCID> [REGION]
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
# 1. VCN + Gateways (IGW, NAT GW, Service GW)
# ------------------------------------------------------------------
echo "--- 1. VCN y Gateways ---"

VCN_ID=$(oci network vcn create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-vcn" \
  --cidr-block "10.0.0.0/16" \
  --dns-label "${DISPLAY_NAME}" \
  --query "data.id" --raw-output)
echo "VCN: $VCN_ID"

# Internet Gateway (for public subnet — LB)
IG_ID=$(oci network internet-gateway create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-igw" \
  --is-enabled true \
  --query "data.id" --raw-output)
echo "Internet Gateway: $IG_ID"

# NAT Gateway (for private subnet — container internet access)
NAT_ID=$(oci network nat-gateway create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-nat" \
  --query "data.id" --raw-output)
echo "NAT Gateway: $NAT_ID"

# Service Gateway (for private subnet — OCI services without internet)
SG_ID=$(oci network service-gateway create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-sg" \
  --services "[{\"serviceId\":\"$(oci network service list --query "data[?contains(\"name\",'All')].id" --raw-output)\"}]" \
  --query "data.id" --raw-output)
echo "Service Gateway: $SG_ID"

# ------------------------------------------------------------------
# 2. Route Tables
# ------------------------------------------------------------------
echo "--- 2. Route Tables ---"

# Public route table: 0.0.0.0/0 → IGW
PUB_RT_ID=$(oci network route-table create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-public-rt" \
  --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IG_ID\"}]" \
  --query "data.id" --raw-output)
echo "Public RT: $PUB_RT_ID"

# Private route table: 0.0.0.0/0 → NAT GW, OCI services → Service GW
OCI_SVC_CIDR=$(oci network service list --query "data[?contains(\"name\",'All')].\"cidr-block\"" --raw-output 2>/dev/null || echo "all-${REGION}-services-in-oracle-services-network")
PRIV_RT_ID=$(oci network route-table create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-private-rt" \
  --route-rules "[
    {\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$NAT_ID\"},
    {\"destinationType\":\"SERVICE_CIDR_BLOCK\",\"cidrBlock\":\"$OCI_SVC_CIDR\",\"networkEntityId\":\"$SG_ID\"}
  ]" \
  --query "data.id" --raw-output)
echo "Private RT: $PRIV_RT_ID"

# ------------------------------------------------------------------
# 3. Subnets
# ------------------------------------------------------------------
echo "--- 3. Subnets ---"

# Public subnet (10.0.1.0/24) — Load Balancer
PUB_SUBNET_ID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-public-subnet" \
  --cidr-block "10.0.1.0/24" \
  --route-table-id "$PUB_RT_ID" \
  --dns-label "public" \
  --prohibit-public-ip-on-vnic false \
  --query "data.id" --raw-output)
echo "Public Subnet: $PUB_SUBNET_ID"

# Private subnet (10.0.2.0/24) — Container Instance
PRIV_SUBNET_ID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-private-subnet" \
  --cidr-block "10.0.2.0/24" \
  --route-table-id "$PRIV_RT_ID" \
  --dns-label "private" \
  --prohibit-public-ip-on-vnic true \
  --query "data.id" --raw-output)
echo "Private Subnet: $PRIV_SUBNET_ID"

# ------------------------------------------------------------------
# 4. Network Security Groups
# ------------------------------------------------------------------
echo "--- 4. Network Security Groups ---"

# NSG for public subnet (LB)
LB_NSG_ID=$(oci network network-security-group create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-lb-nsg" \
  --query "data.id" --raw-output)

oci network network-security-group add-security-rules \
  --network-security-group-id "$LB_NSG_ID" \
  --security-rules "[
    {\"description\":\"HTTP\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"0.0.0.0/0\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":80,\"max\":80}}},
    {\"description\":\"HTTPS\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"0.0.0.0/0\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":443,\"max\":443}}},
    {\"description\":\"LB health checks\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"0.0.0.0/0\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":8000,\"max\":8000}}}
  ]" > /dev/null
echo "LB NSG: $LB_NSG_ID (ports 80, 443, 8000)"

# NSG for private subnet (Container)
CI_NSG_ID=$(oci network network-security-group create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "${DISPLAY_NAME}-ci-nsg" \
  --query "data.id" --raw-output)

# Allow traffic from LB subnet to container on port 8000
oci network network-security-group add-security-rules \
  --network-security-group-id "$CI_NSG_ID" \
  --security-rules "[
    {\"description\":\"LB → Container\",\"direction\":\"INGRESS\",\"protocol\":\"6\",\"source\":\"10.0.1.0/24\",\"sourceType\":\"CIDR_BLOCK\",\"tcpOptions\":{\"destinationPortRange\":{\"min\":8000,\"max\":8000}}}
  ]" > /dev/null
echo "Container NSG: $CI_NSG_ID (port 8000 from LB subnet only)"

# ------------------------------------------------------------------
# 5. Object Storage Bucket
# ------------------------------------------------------------------
echo "--- 5. Object Storage Bucket ---"
NS_NAME=$(oci os ns get --query "data" --raw-output)
BUCKET_NAME="${DISPLAY_NAME}-docs"

oci os bucket create \
  --compartment-id "$COMPARTMENT_ID" \
  --name "$BUCKET_NAME" \
  --namespace-name "$NS_NAME" > /dev/null 2>&1 || echo "Bucket already exists"
echo "Bucket: $BUCKET_NAME (namespace: $NS_NAME)"

# ------------------------------------------------------------------
# 6. Vault + Key
# ------------------------------------------------------------------
echo "--- 6. Vault y Key ---"
VAULT_ID=$(oci kms management vault create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-vault" \
  --vault-type "DEFAULT" \
  --query "data.id" --raw-output)
echo "Vault: $VAULT_ID (provisioning may take 1-2 min)..."
sleep 60

KEY_ID=$(oci kms management key create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-key" \
  --key-shape "{\"algorithm\":\"AES\",\"length\":32}" \
  --query "data.id" --raw-output)
echo "Key: $KEY_ID"

# ------------------------------------------------------------------
# 7. Load Balancer
# ------------------------------------------------------------------
echo "--- 7. Load Balancer ---"

LB_ID=$(oci lb load-balancer create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "${DISPLAY_NAME}-lb" \
  --shape-name "flexible" \
  --shape-details "{\"minimumBandwidthInMbps\":10,\"maximumBandwidthInMbps\":100}" \
  --subnet-ids "[\"$PUB_SUBNET_ID\"]" \
  --is-private false \
  --query "data.id" --raw-output)

# Wait for LB to be active
echo "Waiting for LB to be ACTIVE..."
while true; do
  STATUS=$(oci lb load-balancer get --load-balancer-id "$LB_ID" --query "data.\"lifecycle-state\"" --raw-output)
  [ "$STATUS" = "ACTIVE" ] && break
  sleep 10
done
echo "Load Balancer: $LB_ID"

# Backend set: HTTP 8000, round-robin, health check on /health
BS_NAME="${DISPLAY_NAME}-bs"
oci lb backend-set create \
  --load-balancer-id "$LB_ID" \
  --name "$BS_NAME" \
  --policy "ROUND_ROBIN" \
  --health-checker '{"protocol":"HTTP","port":8000,"urlPath":"/health","intervalMs":30000,"timeoutInMillis":5000,"retries":3,"returnCode":200}' \
  --backends '[]' > /dev/null

# Listener: HTTP 80 → backend set
oci lb listener create \
  --load-balancer-id "$LB_ID" \
  --default-backend-set-name "$BS_NAME" \
  --port 80 \
  --protocol "HTTP" \
  --name "${DISPLAY_NAME}-http-listener" > /dev/null
echo "LB listener: HTTP :80 → backend-set :8000"

# Get LB public IP
LB_IP=$(oci lb load-balancer get --load-balancer-id "$LB_ID" --query "data.\"ip-addresses\"[0].\"ip-address\"" --raw-output)
echo "LB Public IP: $LB_IP"

# ------------------------------------------------------------------
# 8. Save resource IDs for deploy scripts
# ------------------------------------------------------------------
CONFIG_FILE="$(dirname "$0")/.oci-resources"
cat > "$CONFIG_FILE" <<EOF
# OCI Resources — AprendeYa Agent (generated by setup-oci-resources.sh)
COMPARTMENT_ID=$COMPARTMENT_ID
REGION=$REGION
VCN_ID=$VCN_ID
PUBLIC_SUBNET_ID=$PUB_SUBNET_ID
PRIVATE_SUBNET_ID=$PRIV_SUBNET_ID
CI_NSG_ID=$CI_NSG_ID
LB_NSG_ID=$LB_NSG_ID
LB_ID=$LB_ID
LB_BACKEND_SET=$BS_NAME
BUCKET_NAME=$BUCKET_NAME
OBJECT_STORAGE_NS=$NS_NAME
VAULT_ID=$VAULT_ID
KEY_ID=$KEY_ID
EOF
echo "Resource IDs saved to $CONFIG_FILE"

# ------------------------------------------------------------------
echo ""
echo "=== RECURSOS CREADOS ==="
echo "VCN:            $VCN_ID"
echo "Public subnet:  $PUB_SUBNET_ID  (10.0.1.0/24) — LB"
echo "Private subnet: $PRIV_SUBNET_ID (10.0.2.0/24) — Container"
echo "LB NSG:         $LB_NSG_ID"
echo "Container NSG:  $CI_NSG_ID"
echo "Bucket:         $NS_NAME/$BUCKET_NAME"
echo "Vault:          $VAULT_ID"
echo "Key:            $KEY_ID"
echo "LB IP:          $LB_IP"
echo ""
echo "=== MANUAL STEP: Store GROQ_API_KEY ==="
echo 'read -s GROQ_KEY'
echo 'echo -n "$GROQ_KEY" | base64 > /tmp/secret.b64'
echo ""
echo "SECRET_ID=\$(oci kms management secret create \\"
echo "  --compartment-id \"$COMPARTMENT_ID\" \\"
echo "  --key-id \"$KEY_ID\" \\"
echo "  --secret-name \"${DISPLAY_NAME}-groq-key\" \\"
echo "  --description \"Groq API Key\" \\"
echo "  --secret-content-content-type \"BASE64\" \\"
echo "  --secret-content-name \"groq_api_key\" \\"
echo "  --secret-content \"\$(cat /tmp/secret.b64)\" \\"
echo "  --query \"data.id\" --raw-output)"
