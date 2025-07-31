import subprocess
import json
import sys

def run_curl(url, method='GET', data=None):
    """Executa comando curl e retorna resultado"""
    cmd = ['curl', '-s']  # -s para modo silencioso
    
    if method == 'POST':
        cmd.extend(['-X', 'POST'])
        if data:
            cmd.extend(['-H', 'Content-Type: application/json'])
            cmd.extend(['-d', json.dumps(data)])
    
    cmd.append(url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except FileNotFoundError:
        return False, "curl não encontrado. Instale curl no sistema."

def test_api_with_curl():
    """Testa a API usando curl"""
    print("🧪 Testando Device Command API com curl...")
    print("-" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # 1. Health Check
    print("1. 🏥 Testando Health Check...")
    success, response = run_curl(f"{base_url}/health")
    if success:
        print(f"   ✅ Sucesso!")
        print(f"   Response: {response}")
    else:
        print(f"   ❌ Erro: {response}")
        return
    print()
    
    # 2. Enviando comando
    print("2. 📤 Enviando comando para device-999...")
    command_data = {
        "device_id": "device-999",
        "command": "test_command"
    }
    success, response = run_curl(f"{base_url}/command", method='POST', data=command_data)
    if success:
        print(f"   ✅ Comando enviado!")
        print(f"   Response: {response}")
    else:
        print(f"   ❌ Erro: {response}")
    print()
    
    # 3. Device consultando comando
    print("3. 📱 Device-999 consultando comando...")
    success, response = run_curl(f"{base_url}/device/device-999/command")
    if success:
        print(f"   ✅ Consulta realizada!")
        print(f"   Response: {response}")
    else:
        print(f"   ❌ Erro: {response}")
    print()
    
    # 4. Listando comandos
    print("4. 📋 Listando todos comandos...")
    success, response = run_curl(f"{base_url}/commands")
    if success:
        print(f"   ✅ Lista obtida!")
        try:
            data = json.loads(response)
            print(f"   Total de comandos: {data.get('total', 0)}")
        except:
            print(f"   Response: {response[:200]}...")
    else:
        print(f"   ❌ Erro: {response}")
    print()
    
    print("🎉 Testes concluídos!")
    print("\n💡 Acesse http://localhost:5000/swagger/ para ver a documentação Swagger")

if __name__ == "__main__":
    test_api_with_curl() 