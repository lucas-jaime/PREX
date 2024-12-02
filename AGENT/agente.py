# import os
# import platform
# import psutil
# import requests

# def collect_system_info():
#     return {
#         "processor": platform.processor(),  # Información sobre el procesador. 
#         "processes": [p.info for p in psutil.process_iter(['pid', 'name'])], # Listado de procesos corriendo
#         "users": [u.name for u in psutil.users()], # Usuarios con una sesión abierta en el sistema
#         "os_name": platform.system(), # Nombre del sistema operativo
#         "os_version": platform.version() # Versión del sistema operativo
#     }

# def send_data(api_url, data):
#     response = requests.post(api_url, json=data)
#     if response.status_code == 200:
#         print("Data sent successfully")
#     else:
#         print("Failed to send data:", response.text)

# if __name__ == "__main__":
#     api_url = "http://<API_SERVER>/collect"
#     data = collect_system_info()
#     send_data(api_url, data)

import os
import platform
import psutil
import requests

API_URL = os.getenv("API_URL", "http://localhost:5000/collect")

def gather_data():
    data = {
        "os_name": platform.system(), # Nombre del sistema operativo
        "os_version": platform.version(), # Versión del sistema operativo
        "processor": platform.processor(), # Información sobre el procesador
        "processes": [{"pid": p.pid, "name": p.name()} for p in psutil.process_iter(attrs=["pid", "name"])], # Listado de procesos corriendo
        "users": [u.name for u in psutil.users()] # Usuarios con una sesión abierta en el sistema
    }
    return data

def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        print("Datos enviados:", response.json())
    except Exception as e:
        print("Error al enviar datos:", e)

if __name__ == "__main__":
    data = gather_data()
    send_data(data)


