from models import init_db, DeviceCommand, License

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
    
    # Dados de teste - licenças por UUID
    test_licenses = [
        ("550e8400-e29b-41d4-a716-446655440000", "LIC-2024-001"),
        ("550e8400-e29b-41d4-a716-446655440001", "LIC-2024-002"),
        ("550e8400-e29b-41d4-a716-446655440002", "LIC-2024-003"),
        ("f47ac10b-58cc-4372-a567-0e02b2c3d479", "LIC-2024-004"),
        ("6ba7b810-9dad-11d1-80b4-00c04fd430c8", "LIC-2024-005")
    ]
    
    print("🎫 Adicionando licenças de teste...")
    for uuid, license_number in test_licenses:
        try:
            license_id = License.add_license(uuid, license_number)
            print(f"   ✅ Licença '{license_number}' adicionada para UUID {uuid} (ID: {license_id})")
        except ValueError as e:
            print(f"   ⚠️  UUID {uuid} já existe: {e}")
    
    print("\n🎉 Dados de teste adicionados com sucesso!")
    print("\n🧪 Como testar a API:")
    print("1. Acesse http://localhost:5000/swagger/ para ver a documentação")
    print("2. Teste as rotas:")
    print("   • GET /api/device/device-001/command - Pega comando para device-001")
    print("   • POST /api/command - Envia novo comando")
    print("   • GET /api/commands - Lista todos comandos")
    print("   • GET /api/license/{uuid} - Consulta número de licença por UUID")
    print("   • GET /api/health - Verifica se API está OK")
    
    print("\n📱 Exemplo de uso do device:")
    print("   curl http://localhost:5000/api/device/device-001/command")
    
    print("\n💻 Exemplo de envio de comando (frontend):")
    print('   curl -X POST http://localhost:5000/api/command \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"device_id": "device-005", "command": "restart"}\'')
    
    print("\n🎫 Exemplo de consulta de licença por UUID:")
    print("   curl http://localhost:5000/api/license/550e8400-e29b-41d4-a716-446655440000")

if __name__ == '__main__':
    populate_test_data() 