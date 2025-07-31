import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_api():
    """Teste simples da nova API"""
    print("🧪 Testando Device Command API...")
    print("-" * 50)
    
    try:
        # 1. Health Check
        print("1. 🏥 Testando Health Check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        # 2. Enviando comando para device
        print("2. 📤 Enviando comando para device-999...")
        command_data = {
            "device_id": "device-999",
            "command": "test_command"
        }
        response = requests.post(
            f"{BASE_URL}/command", 
            json=command_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        # 3. Device consultando comando
        print("3. 📱 Device-999 consultando comando...")
        response = requests.get(f"{BASE_URL}/device/device-999/command")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        # 4. Device consultando novamente (deve retornar vazio)
        print("4. 📱 Device-999 consultando novamente...")
        response = requests.get(f"{BASE_URL}/device/device-999/command")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        # 5. Listando todos comandos
        print("5. 📋 Listando todos comandos...")
        response = requests.get(f"{BASE_URL}/commands")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total de comandos: {data['total']}")
        print(f"   Últimos comandos:")
        for cmd in data['data'][:3]:  # Mostra apenas os 3 primeiros
            print(f"     - {cmd['device_id']}: {cmd['command']} ({cmd['status']})")
        print()
        
        print("✅ Todos os testes passaram!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando!")
        print("   Execute primeiro: python app.py")
    except Exception as e:
        print(f"❌ Erro durante teste: {str(e)}")

if __name__ == "__main__":
    test_api() 