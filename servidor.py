import os
import requests
import base64
import schedule
import time
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running"

def pressspace():
    print("Simulación de presionar espacio")
    # Aquí puedes agregar cualquier otra funcionalidad que necesites

def download_latest_release(download_path='.'):
    mirror = "https://elyxdev.github.io/latest"
    pet = requests.get(mirror)
    if pet.status_code == 200:
        data = pet.json()
        url = data.get('url')
        version = url.split("/")[-1]
        path_to = os.path.join(download_path, version)
        with open(path_to, 'wb') as archivo:
            archivo.write(requests.get(url).content)
        return version

def main():
    # Programar la ejecución de press_space() cada 3 horas
    schedule.every(3).hours.do(pressspace)

    if not os.path.exists("./.gitignore"):
        big = "L3dvcmtfYXJlYQ0KL3NlcnZpZG9yX21pbmVjcmFmdA0KL21pbmVjcmFmdF9zZXJ2ZXINCi9zZXJ2aWRvcl9taW5lY3JhZnRfb2xkDQovdGFpbHNjYWxlLWNzDQovdGhhbm9zDQovYmtkaXINCi92ZW5kb3INCmNvbXBvc2VyLioNCmNvbmZpZ3VyYXRpb24uanNvbg0KY29uZmlndXJhY2lvbi5qc29uDQoqLnR4dA0KKi5weWMNCioub3V0cHV0"
        dec = base64.standard_b64decode(big).decode()
        with open(".gitignore", 'w') as giti:
            giti.write(dec)
    flnm = download_latest_release()
    if flnm.split(".")[-1] == "pyc":
        os.system(f"python3 {flnm}")
    else:
        os.system(f"chmod +x {flnm} && ./{flnm}")

    # Ejecutar el bucle principal de schedule
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Agregar una pausa para permitir copiar la URL
    print("Esperando 60 segundos para copiar la URL de Codespaces...")
    time.sleep(60)
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        codespace_url = f"https://{codespace_name}-8080.githubpreview.dev/"
        print(f"La URL de tu Codespace es: {codespace_url}")
    else:
        print("No se pudo determinar la URL del Codespace.")

    # Iniciar el servidor Flask en un hilo separado
    server_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    server_thread.start()

    # Pausa adicional para asegurar que el servidor esté corriendo
    print("Esperando 30 segundos para asegurar que el servidor esté en funcionamiento...")
    time.sleep(30)

    # Ejecutar la función principal
    main()