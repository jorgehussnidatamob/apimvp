import sqlite3
from datetime import datetime

DB_NAME = 'device_commands.db'

def init_db():
    """Inicializa o banco de dados simplificado"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela única para comandos por device
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            command TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            executed_at TIMESTAMP NULL
        )
    ''')
    
    conn.commit()
    conn.close()

class DeviceCommand:
    @staticmethod
    def add_command(device_id, command):
        """Adiciona comando para um device"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO device_commands (device_id, command)
            VALUES (?, ?)
        ''', (device_id, command))
        
        conn.commit()
        command_id = cursor.lastrowid
        conn.close()
        
        return command_id
    
    @staticmethod
    def get_pending_command(device_id):
        """Busca próximo comando pendente para o device"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, command, created_at
            FROM device_commands
            WHERE device_id = ? AND status = 'pending'
            ORDER BY created_at ASC
            LIMIT 1
        ''', (device_id,))
        
        result = cursor.fetchone()
        
        if result:
            # Marca como executado
            cursor.execute('''
                UPDATE device_commands 
                SET status = 'executed', executed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (result[0],))
            
            conn.commit()
            
            command = {
                'id': result[0],
                'command': result[1],
                'created_at': result[2]
            }
        else:
            command = None
            
        conn.close()
        return command
    
    @staticmethod
    def get_all_commands():
        """Retorna todos os comandos (para debug/admin)"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, device_id, command, status, created_at, executed_at
            FROM device_commands
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'device_id': row[1],
            'command': row[2],
            'status': row[3],
            'created_at': row[4],
            'executed_at': row[5]
        } for row in results]
    
    @staticmethod
    def get_commands_by_device(device_id):
        """Retorna todos os comandos de um dispositivo específico"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, device_id, command, status, created_at, executed_at
            FROM device_commands
            WHERE device_id = ?
            ORDER BY created_at DESC
        ''', (device_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': row[0],
            'device_id': row[1],
            'command': row[2],
            'status': row[3],
            'created_at': row[4],
            'executed_at': row[5]
        } for row in results] 