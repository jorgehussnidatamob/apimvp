#!/usr/bin/env python3
"""
Script para executar a API de forma resiliente
Monitora o health check e reinicia automaticamente se necessário
"""

import subprocess
import time
import requests
import sys
import signal
import threading
from datetime import datetime

class APIRunner:
    def __init__(self):
        self.api_process = None
        self.running = True
        self.health_url = "http://localhost:5000/api/health"
        # Comando para ativar ambiente e executar API
        if sys.platform == "win32":
            self.start_command = ["cmd", "/c", "conda activate api && python app.py"]
        else:
            self.start_command = ["bash", "-c", "conda activate api && python app.py"]
        self.check_interval = 10  # segundos
        self.startup_wait = 15    # segundos para aguardar após iniciar (aumentado)
        self.max_retries = 3      # tentativas antes de reiniciar
        
    def log(self, message):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def start_api(self):
        """Inicia o processo da API"""
        try:
            self.log("🚀 Iniciando API...")
            self.log(f"🔧 Comando: {' '.join(self.start_command)}")
            
            self.api_process = subprocess.Popen(
                self.start_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,  # Necessário para comando conda no Windows
                cwd=None,    # Usa diretório atual
                env=None     # Usa ambiente atual
            )
            
            self.log(f"⏳ Aguardando {self.startup_wait}s para inicialização...")
            
            # Verifica o processo periodicamente durante a inicialização
            for i in range(self.startup_wait):
                time.sleep(1)
                
                # Se o processo morreu, captura a saída
                if self.api_process.poll() is not None:
                    stdout, stderr = self.api_process.communicate()
                    self.log("❌ Processo da API encerrou durante inicialização")
                    if stdout:
                        self.log(f"📤 STDOUT: {stdout.decode('utf-8', errors='ignore')[:500]}")
                    if stderr:
                        self.log(f"📥 STDERR: {stderr.decode('utf-8', errors='ignore')[:500]}")
                    return False
                
                # A cada 5 segundos, tenta health check
                if i > 5 and i % 5 == 0:
                    if self.check_health():
                        self.log(f"✅ API iniciada com sucesso (PID: {self.api_process.pid})")
                        return True
            
            # Verificação final
            if self.api_process.poll() is None:
                # Processo ainda rodando, verifica health
                if self.check_health():
                    self.log(f"✅ API iniciada com sucesso (PID: {self.api_process.pid})")
                    return True
                else:
                    self.log("⚠️  API iniciada mas não está respondendo ao health check")
                    return False
            else:
                # Processo morreu
                stdout, stderr = self.api_process.communicate()
                self.log("❌ API falhou ao iniciar - processo encerrou")
                if stdout:
                    self.log(f"📤 STDOUT: {stdout.decode('utf-8', errors='ignore')[:500]}")
                if stderr:
                    self.log(f"📥 STDERR: {stderr.decode('utf-8', errors='ignore')[:500]}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao iniciar API: {e}")
            return False
    
    def stop_api(self):
        """Para o processo da API"""
        if self.api_process and self.api_process.poll() is None:
            try:
                self.log("🛑 Parando API...")
                
                if sys.platform == "win32":
                    # Windows
                    self.api_process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    # Linux/Mac
                    self.api_process.terminate()
                
                # Aguarda até 5 segundos para terminar graciosamente
                try:
                    self.api_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.log("⚠️  Forçando encerramento da API...")
                    self.api_process.kill()
                    self.api_process.wait()
                
                self.log("✅ API parada")
                
            except Exception as e:
                self.log(f"❌ Erro ao parar API: {e}")
    
    def check_health(self):
        """Verifica se a API está saudável"""
        try:
            response = requests.get(self.health_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return True
                else:
                    self.log(f"⚠️  Health check retornou status: {data.get('status')}")
                    return False
            else:
                self.log(f"⚠️  Health check retornou código: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️  Falha no health check: {e}")
            return False
        except Exception as e:
            self.log(f"❌ Erro inesperado no health check: {e}")
            return False
    
    def monitor_loop(self):
        """Loop principal de monitoramento"""
        consecutive_failures = 0
        
        while self.running:
            try:
                # Faz health check
                if self.check_health():
                    if consecutive_failures > 0:
                        self.log("✅ API recuperada")
                    else:
                        self.log("🟢 API saudável")
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    self.log(f"⚠️  Health check falhou ({consecutive_failures}/{self.max_retries})")
                
                # Se temos nosso próprio processo, verifica se ainda está rodando
                if self.api_process is not None and self.api_process.poll() is not None:
                    self.log("❌ Processo da API gerenciado foi encerrado")
                    consecutive_failures = self.max_retries  # Força restart
                
                # Se falhou muitas vezes consecutivas, tenta reiniciar
                if consecutive_failures >= self.max_retries:
                    if self.api_process is not None:
                        # API gerenciada pelo runner
                        self.log("🔄 Reiniciando API gerenciada devido a falhas...")
                        self.stop_api()
                        
                        if self.start_api():
                            consecutive_failures = 0
                        else:
                            self.log("❌ Falha ao reiniciar API, tentando novamente em 30s...")
                            time.sleep(30)
                            continue
                    else:
                        # API externa - apenas alerta
                        self.log("⚠️  API externa não está respondendo! Continuando monitoramento...")
                        consecutive_failures = 0  # Reset para evitar spam
                        time.sleep(60)  # Aguarda mais tempo para APIs externas
                        continue
                
                # Aguarda antes da próxima verificação
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("🛑 Recebido sinal de parada...")
                self.running = False
                break
            except Exception as e:
                self.log(f"❌ Erro no loop de monitoramento: {e}")
                time.sleep(10)
    
    def signal_handler(self, signum, frame):
        """Handler para sinais do sistema"""
        self.log("🛑 Recebido sinal de encerramento...")
        self.running = False
    
    def run(self):
        """Executa o runner resiliente"""
        # Configura handlers de sinal
        signal.signal(signal.SIGINT, self.signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.log("🎯 Iniciando API Runner Resiliente")
        self.log(f"📋 Configurações:")
        self.log(f"   • Health Check URL: {self.health_url}")
        self.log(f"   • Intervalo de verificação: {self.check_interval}s")
        self.log(f"   • Máx. tentativas antes de restart: {self.max_retries}")
        self.log(f"   • Tempo de startup: {self.startup_wait}s")
        
        try:
            # Verifica se a API já está rodando
            if self.check_health():
                self.log("✅ API já está rodando e saudável")
                self.log("🔍 Iniciando monitoramento da API existente...")
            else:
                # Tenta iniciar API
                if not self.start_api():
                    self.log("❌ Falha ao iniciar API pela primeira vez")
                    return False
            
            # Inicia loop de monitoramento
            self.monitor_loop()
            
        finally:
            # Cleanup apenas se iniciamos o processo
            if self.api_process:
                self.stop_api()
            else:
                self.log("ℹ️  API externa não foi encerrada pelo runner")
            self.log("👋 API Runner encerrado")
        
        return True

def main():
    """Função principal"""
    print("🤖 API Runner Resiliente v1.0")
    print("=" * 50)
    
    runner = APIRunner()
    
    try:
        success = runner.run()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())