import json
import requests

req = requests.get('https://api.github.com/users/iAMD1ver/repos')

iAMD1ver = json.loads(req.text)


for i in range(len(iAMD1ver)):
    print(iAMD1ver[i]['name'])

with open('req.json', 'w', encoding='utf-8') as f:
    json.dump(iAMD1ver, f)