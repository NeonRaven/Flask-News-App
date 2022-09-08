import base64
import json

import requests

"""
api = 'http://127.0.0.1:5000/test/'
api = 'http://127.0.0.1:5000/new_story/'
image_file = '1.jpg'

with open(image_file, "rb") as f:
    im_bytes = f.read()
im_b64 = base64.b64encode(im_bytes).decode("utf8")

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

payload = json.dumps({"image": im_b64, "other_key": "value"})
print(payload)
response = requests.post(api, data=payload, headers=headers)



try:
    data = response.json()
    print(data)
except requests.exceptions.RequestException:
    print(response.text)
    
"""
import os
import requests
path_img = '2.jpg'
url = 'http://127.0.0.1:5000/new_story/'
with open(path_img, 'rb') as img:
  name_img= os.path.basename(path_img)

  print(name_img)
  print(img)
  files= {'file': (name_img,img,'multipart/form-data',{'Expires': '0'}) }
  with requests.Session() as s:
    r = s.post(url,files=files)
    print(r.status_code)
