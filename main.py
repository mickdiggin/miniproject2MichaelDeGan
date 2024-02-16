import requests
import pandas as pd
import matplotlib.pyplot as plt
from login import *


#api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity)
api_url = 'https://api.api-ninjas.com/v1/caloriesburnedactivities'
response = requests.get(api_url, headers={'X-Api-Key': theKey})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

df = pd.read_json(response.text)
print(df)