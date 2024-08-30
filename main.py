import requests
import json
import os

# Cargar las variables de entorno desde el archivo .env manualmente
def load_env():
    env_vars = {}
    env_path = os.path.join(ruta, '.env')  # Ruta al archivo .env

    if os.path.exists(env_path):
        with open(env_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    else:
        print(f"El archivo .env no se encontró en la ruta: {env_path}")
    
    return env_vars

# Configuración de la aplicación
def get_config():
    env_vars = load_env()
    return {
        'client_id': env_vars.get('CLIENT_ID'),
        'client_secret': env_vars.get('CLIENT_SECRET'),
        'redirect_uri': env_vars.get('REDIRECT_URI'),
        'authorization_code': env_vars.get('AUTHORIZATION_CODE'),
        'token_file': os.path.join(ruta, 'tokens.json')
    }

# Función para guardar tokens en un archivo
def save_tokens(token_file, tokens):
    with open(token_file, 'w') as file:
        json.dump(tokens, file)

# Función para cargar tokens desde un archivo
def load_tokens(token_file):
    if os.path.exists(token_file):
        with open(token_file, 'r') as file:
            return json.load(file)
    return None

# Función para obtener un nuevo token usando el código de autorización
def get_new_tokens(config):
    token_url = 'https://id.twitch.tv/oauth2/token'
    response = requests.post(token_url, {
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': config['authorization_code'],
        'grant_type': 'authorization_code',
        'redirect_uri': config['redirect_uri']
    })

    if response.status_code == 200:
        tokens = response.json()
        save_tokens(config['token_file'], tokens)
        return tokens['access_token']
    else:
        print("Error al obtener el token de acceso:", response.json())
        return None

# Función para renovar el token de acceso usando el refresh token
def refresh_access_token(config, refresh_token):
    token_url = 'https://id.twitch.tv/oauth2/token'
    response = requests.post(token_url, {
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    })

    if response.status_code == 200:
        new_tokens = response.json()
        save_tokens(config['token_file'], new_tokens)
        return new_tokens['access_token']
    else:
        print("Error al renovar el token de acceso:", response.json())
        return None

# Función para obtener el token de acceso, renovándolo si es necesario
def get_access_token(config):
    tokens = load_tokens(config['token_file'])
    if tokens:
        # Intentar renovar el token de acceso usando el refresh token
        return refresh_access_token(config, tokens['refresh_token'])
    else:
        # Si no hay tokens, obtener uno nuevo usando el authorization_code
        return get_new_tokens(config)

# Función para obtener el ID del usuario autenticado
def get_authenticated_user_id(headers):
    url = 'https://api.twitch.tv/helix/users'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info['data'][0]['id']
    else:
        print("Error al obtener el ID del usuario autenticado:", response.json())
        return None

# Función para obtener la lista de suscriptores y sus imágenes de perfil
def get_subscribers(headers, broadcaster_id):
    url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={broadcaster_id}'
    all_subscribers = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            subscribers_data = data['data']
            
            # Obtener la imagen de perfil de cada suscriptor
            for subscriber in subscribers_data:
                user_id = subscriber['user_id']
                user_info_url = f'https://api.twitch.tv/helix/users?id={user_id}'
                user_info_response = requests.get(user_info_url, headers=headers)
                
                if user_info_response.status_code == 200:
                    user_info = user_info_response.json()
                    if 'data' in user_info and len(user_info['data']) > 0:
                        profile_image_url = user_info['data'][0].get('profile_image_url')
                        subscriber['profile_image_url'] = profile_image_url
                else:
                    print(f"Error al obtener la información del usuario {user_id}: ", user_info_response.json())

            all_subscribers.extend(subscribers_data)
            
            # Si hay un cursor de paginación, se actualiza la URL para la próxima solicitud
            cursor = data.get('pagination', {}).get('cursor')
            if cursor:
                url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={broadcaster_id}&after={cursor}'
            else:
                url = None
        else:
            print("Error al obtener la lista de suscriptores:", response.json())
            return None
    return all_subscribers

# Función para guardar los suscriptores en un archivo JSON
def save_subscribers_to_json(subscribers, json_filename):
    with open(os.path.join(ruta, json_filename), mode='w', encoding='utf-8') as file:
        json.dump(subscribers, file, indent=4, ensure_ascii=False)
    print(f"La lista de suscriptores se ha guardado en '{os.path.join(ruta, json_filename)}'.")

# Función principal para ejecutar la petición y guardar los datos en JSON
def peticion():
    load_env()
    config = get_config()

    access_token = get_access_token(config)
    if not access_token:
        return

    headers = {
        'Client-ID': config['client_id'],
        'Authorization': f'Bearer {access_token}'
    }

    # Obtener el ID del usuario autenticado
    broadcaster_id = get_authenticated_user_id(headers)
    if not broadcaster_id:
        return

    subscribers = get_subscribers(headers, broadcaster_id)
    if not subscribers:
        return

    json_filename = 'suscriptores.json'
    save_subscribers_to_json(subscribers, json_filename)
    return subscribers

if __name__ == '__main__':
    global ruta
    ruta = r"C:\Users\Patricio\Documents\Clases Video\Directos\personalizacion\SubsTwitch2"
    peticion()
