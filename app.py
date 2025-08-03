
from flask import Flask
from flask_restx import Api, Resource, fields
from models import init_db, DeviceCommand, License

# Inicializar Flask app
app = Flask(__name__)

# Configurar Flask-RESTX com Swagger
api = Api(
    app, 
    version='1.0', 
    title='Device Command API',
    description='API simples para gerenciar comandos de dispositivos',
    doc='/swagger/'  # Swagger UI estará em /swagger/
)

# Namespace para organizar as rotas
ns = api.namespace('api', description='Operações de comando para dispositivos')

# Modelos para documentação Swagger
command_model = api.model('Command', {
    'device_id': fields.String(required=True, description='ID do dispositivo'),
    'command': fields.String(required=True, description='Comando a ser executado')
})

command_response = api.model('CommandResponse', {
    'id': fields.Integer(description='ID do comando'),
    'command': fields.String(description='Comando a ser executado'),
    'created_at': fields.String(description='Data de criação')
})

# Inicializar banco de dados
init_db()

@ns.route('/device/<string:device_id>/command')
class DeviceCommandResource(Resource):
    @api.doc('get_device_commands')
    def get(self, device_id):
        """
        Lista todos os comandos de um dispositivo específico
        
        Retorna o histórico completo de comandos para o dispositivo.
        """
        try:
            commands = DeviceCommand.get_commands_by_device(device_id)
            
            return {
                'status': 'success',
                'data': commands,
                'total': len(commands)
            }
                
        except Exception as e:
            api.abort(500, f'Erro interno: {str(e)}')

@ns.route('/device/<string:device_id>/pending')
class DevicePendingCommandResource(Resource):
    @api.doc('get_pending_command')
    def get(self, device_id):
        """
        Consulta se existe comando pendente para o device
        
        Esta é a rota que cada device deve consultar periodicamente.
        Retorna o próximo comando pendente e o marca como executado.
        """
        try:
            command = DeviceCommand.get_pending_command(device_id)
            
            if command:
                return {
                    'status': 'success',
                    'data': command,
                    'message': 'Comando encontrado'
                }
            else:
                return {
                    'status': 'success', 
                    'data': None,
                    'message': 'Nenhum comando pendente'
                }
                
        except Exception as e:
            api.abort(500, f'Erro interno: {str(e)}')

@ns.route('/command')
class CommandResource(Resource):
    @api.doc('send_command')
    @api.expect(command_model, validate=True)
    def post(self):
        """
        Envia comando para um device (usado pelo frontend)
        
        O frontend usa esta rota para enviar comandos para dispositivos específicos.
        """
        try:
            data = api.payload
            device_id = data['device_id']
            command = data['command']
            
            # Adiciona comando à fila do device
            command_id = DeviceCommand.add_command(device_id, command)
            
            return {
                'status': 'success',
                'message': f'Comando enviado para device {device_id}',
                'command_id': command_id
            }
            
        except Exception as e:
            api.abort(500, f'Erro ao enviar comando: {str(e)}')

@ns.route('/commands')
class AllCommandsResource(Resource):
    @api.doc('get_all_commands')
    def get(self):
        """
        Lista todos os comandos (para debug/admin)
        """
        try:
            commands = DeviceCommand.get_all_commands()
            return {
                'status': 'success',
                'data': commands,
                'total': len(commands)
            }
        except Exception as e:
            api.abort(500, f'Erro ao buscar comandos: {str(e)}')

@ns.route('/license/<string:uuid>')
class LicenseResource(Resource):
    @api.doc('get_license_by_uuid')
    def get(self, uuid):
        """
        Consulta número de licença por UUID
        
        Retorna o número de licença associado ao UUID fornecido.
        """
        try:
            license_data = License.get_license_by_uuid(uuid)
            
            if license_data:
                return {
                    'status': 'success',
                    'data': license_data,
                    'message': 'Licença encontrada'
                }
            else:
                return {
                    'status': 'error',
                    'data': None,
                    'message': 'Licença não encontrada para este UUID'
                }, 404
                
        except Exception as e:
            api.abort(500, f'Erro interno: {str(e)}')

@ns.route('/health')
class HealthResource(Resource):
    @api.doc('health_check')
    def get(self):
        """Verifica se a API está funcionando"""
        return {
            'status': 'success',
            'message': 'API funcionando normalmente',
            'version': '1.0'
        }

if __name__ == '__main__':
    print(">>> Iniciando Device Command API...")
    print(">>> Swagger UI disponivel em: http://localhost:5000/swagger/")
    print(">>> Rotas principais:")
    print("   GET  /api/device/{device_id}/command - Lista historico de comandos do device")
    print("   GET  /api/device/{device_id}/pending - Device consulta comandos pendentes")
    print("   POST /api/command - Frontend envia comandos")
    print("   GET  /api/commands - Lista todos comandos (admin)")
    print("   GET  /api/license/{uuid} - Consulta numero de licenca por UUID")
    print("   GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 