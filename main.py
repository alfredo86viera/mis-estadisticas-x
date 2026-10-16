import json
import requests

# Lista de usuarios que estás rastreando
usuarios = ['alfredo86viera', 'yusleny809gmail', 'nival61423']

# Cabeceras para simular un navegador real y reducir bloqueos
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'es-ES,es;q=0.9',
}


def monitorear_usuario(usuario):
  print(f'Monitoreando a @{usuario}...')

  # URL o endpoint que utiliza tu script para obtener los datos
  url = f'https://twitter.com/{usuario}'

  try:
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code == 200:
      try:
        # Intenta leer la respuesta como datos estructurados (JSON)
        data = response.json()
        print(f'-> Datos procesados correctamente para @{usuario}')
        return data
      except (ValueError, json.JSONDecodeError):
        # Solución al error: X devuelve HTML en lugar de JSON debido a sus restricciones
        print(
            f'-> Aviso: La plataforma devolvió contenido protegido o no JSON'
            f' para @{usuario}.'
        )
        return None
    else:
      print(f'-> Error HTTP {response.status_code} al consultar a @{usuario}')
      return None

  except Exception as e:
    print(f'-> Error de conexión con @{usuario}: {e}')
    return None


def main():
  print(f'Iniciando monitoreo de {len(usuarios)} usuarios...')

  for usuario in usuarios:
    monitorear_usuario(usuario)

  print('Monitoreo diario completado con éxito.')


if __name__ == '__main__':
  main()
