import requests

r = requests.get('http://192.168.10.139:3000/platinum')

print(r.status_code)

print(r.json)
