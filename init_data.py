from models import init_db, DeviceCommand

def populate_test_data():
    """Popula o banco com dados de teste para a API simplificada"""
    print("🔄 Inicializando banco de dados...")
    init_db()
    
    # Dados de teste - comandos para diferentes devices
    test_commands = [
        ("device-001", "reboot"),
        ("device-001", "update_firmware"),
        ("device-002", "restart_service"),
        ("device-003", "clear_cache"),
        ("device-002", "backup_config"),
        ("device-001", "check_status"),
        ("device-004", "sync_data")
    ]
    
    print("📝 Adicionando comandos de teste...")
    for device_id, command in test_commands:
        command_id = DeviceCommand.add_command(device_id, command)
        print(f"   ✅ Comando '{command}' adicionado para {device_id} (ID: {command_id})")
    
    print("\n🎉 Dados de teste adicionados com sucesso!")
    print("\n🧪 Como testar a API:")
    print("1. Acesse http://localhost:5000/swagger/ para ver a documentação")
    print("2. Teste as rotas:")
    print("   • GET /api/device/device-001/command - Pega comando para device-001")
    print("   • POST /api/command - Envia novo comando")
    print("   • GET /api/commands - Lista todos comandos")
    print("   • GET /api/health - Verifica se API está OK")
    
    print("\n📱 Exemplo de uso do device:")
    print("   curl http://localhost:5000/api/device/device-001/command")
    
    print("\n💻 Exemplo de envio de comando (frontend):")
    print('   curl -X POST http://localhost:5000/api/command \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"device_id": "device-005", "command": "restart"}\'')

if __name__ == '__main__':
    populate_test_data() 