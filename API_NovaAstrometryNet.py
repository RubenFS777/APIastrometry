import requests
import json
import time
import os

def verificar_archivo(ruta_archivo):
    if os.path.isfile(ruta_archivo):
        print("El archivo existe.")
    else:
        print("El archivo no existe.")



login_url = 'http://nova.astrometry.net/api/login'
upload_url = 'http://nova.astrometry.net/api/upload'
api_key = "put_your_key_here"
delay = 10
# Realizar la solicitud de inicio de sesión
R = requests.post(login_url, data={'request-json': json.dumps({"apikey": api_key})})
print('Respuesta a la petición de inicio de sesión')
print(R.text)

# Analizar la respuesta JSON
response_json = json.loads(R.text)
# Extraer el valor del campo 'session'
session_value = response_json['session']

# Datos de la solicitud de carga de archivo
request_json = {
    "publicly_visible": "n",
    "allow_modifications": "d",
    "session": session_value,
    "allow_commercial_use": "d"
}

file_path = 'put_your_file_here'
# Ejemplo de uso
verificar_archivo(file_path)

# Crear los datos de la solicitud multipart/form-data
multipart_data = [
    ('request-json', (None, json.dumps(request_json), 'text/plain')),
    ('file', (open(file_path, 'rb'))),
]
print('Intento de envio de fichero')
# Enviar la solicitud POST con los datos multipart/form-data
response = requests.post(upload_url, files=multipart_data)

# Imprimir la respuesta
print('Respuesta al envío de fichero')
print(response.text)  #no está preparado para caidas del sistema

# Preparándose para el estado del trabajo
response = json.loads(response.text)
submission_id = response['subid']
status_url = f'http://nova.astrometry.net/api/submissions/{submission_id}'

# Verificar el estado del trabajo cada 10 segundos hasta que esté terminado
not_done = True
while not_done:
    response = requests.get(status_url)
    status_json = json.loads(response.text)
    # Verificar el estado de la solicitud
    if 'jobs' in status_json:
        jobs = status_json['jobs']
        if len(jobs) > 0:
            job_id = jobs[0]
            print(f"Código de trabajo: {job_id}")
            # Verificar el estado del trabajo
            job_url = f'http://nova.astrometry.net/api/jobs/{job_id}'
            while not_done:
                job_response = requests.get(job_url)
                job_status_json = json.loads(job_response.text)
                if 'status' in job_status_json:
                    job_status = job_status_json['status']
                    if job_status == 'success':
                        print("El trabajo ha terminado exitosamente")
                        not_done = False
                        delay = 0
                        #Obtener información del trabajo
                        info_url = f'http://nova.astrometry.net/api/jobs/{job_id}/info/'
                        response = requests.post(info_url)
                        print(response.text)
                        break
                    elif job_status == 'failure':
                        print("El trabajo ha fallado")
                        not_done = False
                        delay = 0
                        break
                    elif job_status == 'Processing':#p mayuscula?
                        print("El trabajo está en proceso")
                    else:
                        print("Estado desconocido del trabajo")
                else:
                    print("No se encontró el campo 'status' en la respuesta del trabajo")
                # Esperar 10 segundos antes de la siguiente verificación
                time.sleep(delay)
        else:
            print("La solicitud aún no ha comenzado a procesarse")
    else:
        print("No se encontró el campo 'jobs' en la respuesta")
    # Esperar 10 segundos antes de la siguiente verificación
    time.sleep(delay)

#<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
#<html><head>
#<title>503 Service Unavailable</title>
#</head><body>
#<h1>Service Unavailable</h1>
#<p>The server is temporarily unable to service your
#request due to maintenance downtime or capacity
#problems. Please try again later.</p>
#<hr>
#<address>Apache/2.4.41 (Ubuntu) Server at nova.astrometry.net Port 80</address>
#</body></html>
