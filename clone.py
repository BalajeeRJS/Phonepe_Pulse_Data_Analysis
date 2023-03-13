import requests
import os
import subprocess

#CLONING TH PHONEPE--PULSE GITHUB REPOSITORY

response = requests.get('https://api.github.com/repos/PhonePe/pulse')
repo = response.json()
clone_url = repo['clone_url']
print (clone_url)

#DIRECTING THE REPOSITORY TO THE LOCAL DIRECTORY

repo_name = "pulse"
clone_dir = os.path.join(os.getcwd(), repo_name)
#print(clone_dir)
#print("done")
subprocess.run(["git", "clone", clone_url, clone_dir], check=True)