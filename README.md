# 📱 Device Command API

API simples e funcional para gerenciar comandos de dispositivos com Swagger integrado.

## 🎯 Como Funciona

- **Devices consultam**: `GET /api/device/{device_id}/command` - Pega próximo comando pendente
- **Frontend envia**: `POST /api/command` - Envia novo comando para um device
- **Swagger UI**: `http://localhost:5000/swagger/` - Documentação interativa

## 🚀 Como Usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Inicializar dados de teste
```bash
python init_data.py
```

### 3. Rodar a API
```bash
python app.py
```

### 4. Acessar Swagger
Abra no navegador: `http://localhost:5000/swagger/`

### 5. Testar a API
```bash
python test_new_api.py
```

## 🔗 Rotas Principais

### Device consulta comando
```bash
GET /api/device/{device_id}/command
```
**Uso**: O device faz essa consulta periodicamente para verificar se tem comando pendente.

### Frontend envia comando
```bash
POST /api/command
Content-Type: application/json

{
    "device_id": "device-001", 
    "command": "reboot"
}
```

### Listar todos comandos (admin)
```bash
GET /api/commands
```

### Health Check
```bash
GET /api/health
```

## 📋 Exemplo de Uso

### 1. Device consultando comando:
```bash
curl http://localhost:5000/api/device/device-001/command
```

**Resposta com comando:**
```json
{
    "status": "success",
    "data": {
        "id": 1,
        "command": "reboot",
        "created_at": "2024-01-15 10:30:00"
    },
    "message": "Comando encontrado"
}
```

**Resposta sem comando:**
```json
{
    "status": "success", 
    "data": null,
    "message": "Nenhum comando pendente"
}
```

### 2. Frontend enviando comando:
```bash
curl -X POST http://localhost:5000/api/command \
     -H "Content-Type: application/json" \
     -d '{"device_id": "device-001", "command": "restart"}'
```

**Resposta:**
```json
{
    "status": "success",
    "message": "Comando enviado para device device-001",
    "command_id": 123
}
```

## 🗄️ Banco de Dados

Banco SQLite simples com uma tabela:

**device_commands**
- `id` - ID do comando
- `device_id` - ID do dispositivo  
- `command` - Comando a ser executado
- `status` - pending/executed
- `created_at` - Data de criação
- `executed_at` - Data de execução

## 📱 Integração do Device

O device deve fazer polling na API:

```python
import requests
import time

DEVICE_ID = "device-001"
API_URL = "http://localhost:5000/api"

while True:
    try:
        response = requests.get(f"{API_URL}/device/{DEVICE_ID}/command")
        data = response.json()
        
        if data['data']:  # Tem comando
            command = data['data']['command']
            print(f"Executando: {command}")
            # Aqui executa o comando...
            
        time.sleep(10)  # Consulta a cada 10 segundos
        
    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(30)  # Aguarda 30s em caso de erro
```

## 💻 Integração do Frontend

```javascript
// Enviar comando para device
async function sendCommand(deviceId, command) {
    const response = await fetch('/api/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            device_id: deviceId,
            command: command
        })
    });
    
    return response.json();
}

// Exemplo de uso
sendCommand('device-001', 'reboot')
    .then(result => console.log('Comando enviado:', result));
```

## 🧪 Testes

Execute os testes automatizados:
```bash
python test_new_api.py
```

## 🔧 Estrutura de Arquivos

```
simple-api/
├── app.py              # API principal com Swagger
├── models.py           # Modelos do banco de dados  
├── init_data.py        # Script para popular dados de teste
├── test_new_api.py     # Testes automatizados
├── requirements.txt    # Dependências
└── README.md          # Esta documentação
```

## ✅ Características

- ✅ **Simples**: Apenas 2 rotas principais
- ✅ **Swagger integrado**: Documentação automática
- ✅ **Polling eficiente**: Device consulta 1 rota
- ✅ **Frontend friendly**: JSON simples
- ✅ **Banco SQLite**: Sem configuração complexa
- ✅ **Status tracking**: Comandos marcados como executados
- ✅ **Error handling**: Tratamento de erros 