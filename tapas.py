# DEC vueltas 69 grados 360-40 = 320 1 vuelta 4.9275 grados. 1/4 de vuelta 1.2319 grados.
# RA vueltas 116 grados 360-42 = 338 1 vuelta 2.9138 grados. 1/4 de vuelta 0.7845 grados.
# Measure almost twice

import requests
import json
import time
import os

#Funtions
def verify_file(file_path):
    if os.path.isfile(file_path):
        print("The file  exists.")
    else:
        print("The file does not exists.")

#Initialization of variable values
login_url = 'http://nova.astrometry.net/api/login'
upload_url = 'http://nova.astrometry.net/api/upload'
api_key = "Your_API_Key"
delay = 10 #10 seconds is the same values that nova uses for the website submit
aim_to_ra = 270.89307777777777777778 #your RA goal
aim_to_dec = 33.02916666666666666667 #your DEC goal

#To make the login request
response = requests.post(login_url, data={'request-json': json.dumps({"apikey": api_key})})
print('Response to the login request')
print(response.text)
#Analyze the response JSON
response_json = json.loads(response.text)
#Extract the value of the 'session' field
session_value = response_json['session']

#Options for saving the file in nova.astronomy.net ToDo give not freezed options.
request_json = {
    "publicly_visible": "n",
    "allow_modifications": "d",
    "session": session_value,
    "allow_commercial_use": "d"
}

#ToDo take for the place you run the program
file_path = 'Your_path_file.fit'
verify_file(file_path)

#Create multipart/form-data request data
multipart_data = [
    ('request-json', (None, json.dumps(request_json), 'text/plain')),
    ('file', (open(file_path, 'rb'))),
]
#Send the POST request with the multipart/form-data data
response = requests.post(upload_url, files=multipart_data)
print('Response to the file upload')
print(response.text)

#Preparing to check the status of the job.
response = json.loads(response.text)
submission_id = response['subid']
status_url = f'http://nova.astrometry.net/api/submissions/{submission_id}'

# Check the status of the job every 10 (delay = 10) seconds until it is finished.
not_done = True
while not_done:
    response = requests.get(status_url)
    status_json = json.loads(response.text)
    #Check the status of the request.
    if 'jobs' in status_json:
        jobs = status_json['jobs']
        if len(jobs) > 0:
            job_id = jobs[0]
            print(f"Job code: {job_id}")
            #Check the status of the job
            job_url = f'http://nova.astrometry.net/api/jobs/{job_id}'
            while not_done:
                job_response = requests.get(job_url)
                job_status_json = json.loads(job_response.text)
                if 'status' in job_status_json:
                    job_status = job_status_json['status']
                    if job_status == 'success':
                        print("The job has completed successfully.")
                        not_done = False
                        delay = 0
                        #Retrieve job information.
                        info_url = f'http://nova.astrometry.net/api/jobs/{job_id}/info/'
                        info_response = requests.post(info_url)
                        #print(info_response.text) #all data in raw format
                        info_response_json = json.loads(info_response.text)
                        info_calibration = info_response_json['calibration']
                        #print(f"Calibration: {info_calibration}")
                        ra = info_calibration['ra']
                        dec = info_calibration['dec']
                        print(f"RA: {ra}, DEC: {dec}")
                        print(f"RA deviation: {ra-aim_to_ra}, DEC deviation: {dec-aim_to_dec}")
                        print(f"RA turn over: {(ra-aim_to_ra)/338*116}, DEC turn over: {(dec-aim_to_dec)/320*69}") #the numbers comes from my mount
                        if 'objects_in_field' in info_response_json:
                            objects_in_field = info_response_json['objects_in_field']
                            if len(objects_in_field) > 0:
                                job_objects = objects_in_field
                                print(f"Objects in the field: {job_objects}")
                        break
                    elif job_status == 'failure':
                        print("The job has failed")
                        not_done = False
                        delay = 0
                        break
                    elif job_status == 'Processing':#p mayuscula?
                        print("The job is in progress.")
                    else:
                        print("Unknown status of the job.")
                else:
                    print("The 'status' field was not found in the job response.")
                #Delay until the next verification of the job's status
                time.sleep(delay)
        else:
            print("The request has not started processing yet.")
    else:
        print("The 'jobs' field was not found in the response.")
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
#Salida estandar de informaciń¡ón
#{"objects_in_field": [], "machine_tags": [], "tags": [], "status": "success", "original_filename": "Light_ASIImg_0.5sec_Bin1_20.2C_gain252_2023-05-28_002959_frame0010.fit", "calibration": {"ra": 284.4193862490942, "dec": 33.08656471549371, "radius": 0.2805384046831555, "pixscale": 0.45845702014834766, "orientation": 90.76687401482185, "parity": 1.0}}

