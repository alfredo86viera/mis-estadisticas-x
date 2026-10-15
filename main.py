import os
import csv
from datetime import datetime
import requests

INPUT_FILE = "usuarios.txt"
OUTPUT_FILE = "historial_estadisticas.csv"

def obtener_datos_publicos(username):
    url = f"https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={username}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                user_info = data[0]
                return {
                    "fecha": datetime.utcnow().strftime("%Y-%m-%d"),
                    "username": username,
                    "followers": user_info.get("followers_count", 0),
                    "following": user_info.get("friends_count", 0),
                    "statuses": user_info.get("statuses_count", 0)
                }
    except Exception as e:
        print(f"Error con {username}: {e}")
    return None

def main():
    if not os.path.exists(INPUT_FILE):
        print("No se encontró el archivo de usuarios.")
        return

    with open(INPUT_FILE, "r") as f:
        usuarios = [line.strip() for line in f if line.strip()]

    resultados = []
    print(f"Monitoreando {len(usuarios)} usuarios...")

    for user in usuarios:
        datos = obtener_datos_publicos(user)
        if datos:
            resultados.append(datos)

    file_exists = os.path.exists(OUTPUT_FILE)
    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["fecha", "username", "followers", "following", "statuses"])
        if not file_exists:
            writer.writeheader()
        for row in resultados:
            writer.writerow(row)
    
    print("Monitoreo diario completado con éxito.")

if __name__ == "__main__":
    main()
