# Imports
from base64 import b64encode
from json import dumps
from os import remove
from os import system as bash
from shutil import copy as sh_copy
from threading import Thread

import requests

# Constants
NEWLINE: str = '\n'

# Classes
class ChooseInput:
  def __init__(self, prompt: str, options: list[str]):
    self.prompt = prompt
    self.options = options

  def ask(self):
    return int(input(f'{self.prompt}\n{NEWLINE.join([f"{i} | {v}" for i, v in enumerate(self.options)])}\n'))

# Functions
def img_to_b64(location: str) -> str:
  with open(str(location), 'rb') as image:
      string: bytes = b64encode(image.read())
      return string.decode('utf-8')

def b64_url_encode(b64: str) -> str:
  return b64.replace('=', '%3D').replace('/', '%2F').replace('+', '%2B')

# Get image
img_path: str = input('Image name: ')
img_type: str = img_path.split('.')[-1]
full_img_path: str = 'res/' + img_path
image: str = f'data:image/{img_type};base64,' + b64_url_encode(img_to_b64(full_img_path))

# Take user input
total_repetitions: int = int(input('Repetitions: '))

print()

username = input('Username: ')
if len(username) == 0:
  username = 'shadow wizard marble gang'

trackname = input('Track name: ')

# Precomputed data tables
track_json = {
  'bricks': {
    '0': {
      'type': 'Ball',
      'rotation': 0.0,
      'row': 0,
      'col': 0
    },
    '140': {
      'type': 'Exit',
      'rotation': 0.0,
      'row': 14,
      'col': 0
    },
    'foo': {
      'type': 'Boost',
      'rotation': 2.0,
      'row': 0,
      'col': 9,
    }
  },
  'pairs': []
}

# for r in range(15):
#   for c in range(10):
#     if (r == 14 or r == 0) and c == 0:
#       continue
    
#     track_json['bricks'][str(r) + str(c)] = {
#       'type': 'Boost',
#       'rotation': r / 15 + c / 10,
#       'row': r,
#       'col': c
#     }

data = {
  'track[json]': dumps(track_json),
  'track[length]': 9999,
  'track[duration]': 69420000,
  'track[imagedata]': image, # This is a string
  'track[username]': username.upper(),
  'track[trackname]': trackname.upper()
}

headers = {
  'POST': '/tracks HTTP/1.1',
  'Host': 'www.marblerun.at',
  'Accept': 'application/json',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.marblerun.at/tracks/new',
  'Origin': 'https://www.marblerun.at',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'X-Requested-With': 'XMLHttpRequest',
  'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# Post loop
bash('clear')

session = requests.Session()
latest_status_code: int = 0
failures: int = 0
jobs = total_repetitions

def send_request(url: str, data, headers):
  global failures
  global jobs
  global latest_status_code
  
  with session.post(url, data=data, headers=headers) as r:
    latest_status_code = r.status_code
    
    if r.status_code != 200:
      failures += 1
    
    jobs -= 1

for r in range(total_repetitions):
  print(f'{latest_status_code if latest_status_code != 0 else "-"}\t\t{r + 1}/{total_repetitions}')
  Thread(target=send_request, args=('https://www.marblerun.at/tracks', data, headers)).start()

# Post-post output
while jobs > 0:
  pass

print(f"\n {failures}/{total_repetitions} failures")
