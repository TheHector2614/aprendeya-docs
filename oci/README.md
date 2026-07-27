# Despliegue en OCI — AprendeYa Agent

## Arquitectura

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Usuarios   │────▶│  Load Balancer   │────▶│  Container   │
│ (HTTP/8000) │     │  (opcional)      │     │  Instance    │
└─────────────┘     └──────────────────┘     ├──────────────┤
                                              │ FastAPI      │
                                              │ Agent RAG    │
                                              │ ChromaDB     │
                                              │ Groq LLM     │
                                              └──────┬───────┘
                                                     │
                     ┌───────────────────────────────┼──────────────┐
                     │  OCI Vault                    │              │
                     │  └─ GROQ_API_KEY (secreto)    │              │
                     │                               │              │
                     │  OCI Object Storage           │              │
                     │  └─ aprendeya-agent-docs/     │              │
                     │     ├── raw/ (documentos)      │              │
                     │     └── index/ (respaldo)      │              │
                     │                               │              │
                     │  OCIR (Container Registry)    │              │
                     │  └─ aprendeya-agent:latest    │              │
                     └───────────────────────────────┘──────────────┘
```

## Servicios OCI utilizados

| Servicio | Propósito |
|----------|-----------|
| **OCIR** | Almacenamiento de imágenes Docker |
| **Container Instances** | Ejecución del contenedor sin gestionar VMs |
| **Object Storage** | Backup de documentos raw y respaldo del índice |
| **Vault** | Almacenamiento seguro de GROQ_API_KEY |
| **VCN + NSG** | Red aislada con control de tráfico |
| **Virtual Cloud Network** | Subred pública para el contenedor |

## Prerrequisitos

1. OCI CLI instalado y configurado (`~/.oci/config`)
2. Docker instalado
3. Permisos para crear recursos en el compartment de OCI

## Despliegue paso a paso

### 1. Crear recursos de infraestructura (solo la primera vez)

```bash
oci os ns get  # obtiene el namespace de Object Storage

bash oci/setup-oci-resources.sh <COMPARTMENT_OCID> <REGION>
```

Esto crea: VCN, subred pública, NSG, bucket Object Storage, Vault + Key.

### 2. Almacenar la API key de Groq en OCI Vault

```bash
read -s GROQ_KEY
echo -n "$GROQ_KEY" | base64 > /tmp/secret.b64

oci kms management secret create \
  --compartment-id <COMPARTMENT_OCID> \
  --key-id <KEY_ID> \
  --secret-name "aprendeya-agent-groq-key" \
  --description "Groq API Key for AprendeYa Agent" \
  --secret-content-content-type "BASE64" \
  --secret-content-name "groq_api_key" \
  --secret-content "$(cat /tmp/secret.b64)"
```

### 3. Construir y subir la imagen

```bash
# Construir
docker build -t aprendeya-agent:latest .

# Taggear para OCIR
docker tag aprendeya-agent:latest \
  <REGION>.ocir.io/<NAMESPACE>/aprendeya-agent:latest

# Autenticarse en OCIR
docker login <REGION>.ocir.io \
  -u <OCI_USER_NAME> \
  --password-stdin  # ingresa el Auth Token

# Subir
docker push <REGION>.ocir.io/<NAMESPACE>/aprendeya-agent:latest
```

### 4. Desplegar

```bash
bash oci/deploy.sh <COMPARTMENT_OCID> <REGION>
```

### 5. Probar

```bash
curl -X POST http://<PUBLIC_IP>:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Cual es el tope diario para gastos de alimentacion?"}'
```

## CI/CD (GitHub Actions)

El pipeline en `.github/workflows/deploy.yml` automatiza:

1. Build de la imagen Docker
2. Push a OCIR
3. Recupera la API key de OCI Vault
4. Actualiza la Container Instance
5. Espera health check

### Secrets requeridos en GitHub

| Secret | Descripción |
|--------|-------------|
| `OCI_TENANCY_OCID` | OCID del tenancy |
| `OCI_USER_OCID` | OCID del usuario |
| `OCI_FINGERPRINT` | Huella de la clave API |
| `OCI_PRIVATE_KEY` | Llave privada (formato PEM) |
| `OCI_AUTH_TOKEN` | Token de autenticación para OCIR |
| `OCI_USER_NAME` | Nombre de usuario para OCIR |

### Variables requeridas en GitHub

| Variable | Descripción |
|----------|-------------|
| `OCI_COMPARTMENT_OCID` | OCID del compartment |
| `OCI_OBJECT_STORAGE_NS` | Namespace de Object Storage |
| `OCI_VAULT_SECRET_ID` | OCID del secreto en Vault |
| `OCI_CONTAINER_INSTANCE_ID` | OCID de la Container Instance |

## Costos estimados (siempre verificar en la consola OCI)

| Recurso | Aprox. mensual |
|---------|----------------|
| Container Instance (2 OCPU, 8 GB) | ~$30-50 USD |
| Object Storage (1 GB) | ~$0.03 USD |
| Vault | ~$1 USD |
| VCN + Load Balancer | ~$20 USD |
| **Total** | **~$51-71 USD/mes** |

## Notas

- La imagen incluye el modelo de embeddings precargado (~500 MB)
- El índice ChromaDB se construye durante el build de la imagen
- Para actualizar documentos, reconstruir la imagen con `python scripts/ingest.py` y redeploy
- El health check monitorea el endpoint `/health` cada 30s
