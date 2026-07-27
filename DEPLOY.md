# Deploy AprendeYa Agent — paso a paso

## Prerrequisitos

```powershell
# 1. Verificar OCI CLI
oci --version

# 2. Verificar Docker
docker --version

# 3. Verificar git
git --version
```

## Paso 1: Configurar OCI CLI

```powershell
# Si no está instalado:
# Descargar: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm

oci setup config
# Te pedirá:
#   - User OCID (de tu perfil OCI)
#   - Tenancy OCID
#   - Region (ej: us-ashburn-1)
#   - Generar par de llaves RSA
```

## Paso 2: Autenticar Docker con OCIR

```powershell
# Obtener Auth Token desde Consola OCI:
#   Perfil → Auth Tokens → Generate Token

docker login <REGION>.ocir.io `
  -u <NAMESPACE>/<USERNAME> `
  --password-stdin
# Pegar el Auth Token cuando pida contraseña
```

## Paso 3: Crear infraestructura OCI

```powershell
# Necesitás el OCID de tu compartment
# Lo encontrás en Consola OCI → Identity → Compartments

bash oci/setup-oci-resources.sh <COMPARTMENT_OCID>
```

Esto crea: VCN, 2 subnets, NAT GW, Service GW, NSGs, Object Storage bucket, Vault + Key, Load Balancer.

## Paso 4: Guardar GROQ_API_KEY en OCI Vault

```powershell
# Seguir las instrucciones que imprime el script, o:
read -s GROQ_KEY
echo -n "$GROQ_KEY" | base64
# Copiar el base64 output

oci kms management secret create `
  --compartment-id <COMPARTMENT_OCID> `
  --key-id <KEY_ID> `
  --secret-name "aprendeya-agent-groq-key" `
  --description "Groq API Key" `
  --secret-content-content-type "BASE64" `
  --secret-content-name "groq_api_key" `
  --secret-content "<BASE64_DE_TU_KEY>"
```

## Paso 5: Pushear a GitHub (opcional, para CI/CD)

```powershell
# Si ya tenés remote configurado:
git push origin main
```

## Paso 6: Deploy manual

```powershell
bash oci/deploy.sh <COMPARTMENT_OCID>
```

Esto: build → push OCIR → crear/actualizar Container Instance → registrar LB → health check.

## Verificar

```powershell
curl -X POST http://<LB_IP>/ask `
  -H "Content-Type: application/json" `
  -d '{"question":"Qué es el NPS y cuál es la meta?"}'
```

## Troubleshooting

| Problema | Solución |
|----------|----------|
| `oci: command not found` | Instalar OCI CLI |
| `docker: command not found` | Iniciar Docker Desktop |
| Container no responde | `oci compute-container-instance container-instance get --container-instance-id <CI_ID>` |
| LB no pasa tráfico | Verificar NSG: container acepta tráfico desde 10.0.1.0/24 |
