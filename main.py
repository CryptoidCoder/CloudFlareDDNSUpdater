# Cloudflare DDNs Updater

import os
import requests

from dotenv import load_dotenv
load_dotenv()



# Functions:
def addnewline(filename,text): #append text to a new line on a file
    # Open the file in append & read mode ('a+')
    with open(filename, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text)
        file_object.close()

def current_ip(): # Get current Public IP
    url = 'https://ifconfig.me/ip'
    try:
        current_public_ip = requests.get(url).text
    except:
        print(f"Unable To Get IP From {url}")

def test_api():
    url= 'https://api.cloudflare.com/client/v4/user/tokens/verify'
    api_token = os.getenv("cloudflare_API_token")

    request = requests.get(url, headers = {"Authorization": f"Bearer #{api_token}", "Content-Type":"application/json" })
    request = request.text

    try:
        first_string, id = request.split('"id":"')
        id, second_string = id.split('","status"')
    except:
        id = 'None'

    try:
        first_string, response_text = request.split(',"message":"')
        response_text, second_string = response_text.split('","type')
    except:
        response_text = 'None'

    try:
        first_string, response_code = request.split('"code":')
        response_code, second_string = response_code.split(',"message":')
    except:
        response_code = 'None'

    try:
        first_string, response_status = request.split('"status":"')
        response_status, second_string = response_status.split('"},"success"')
    except:
        response_status = 'None'

    return id, response_text, response_code, response_status, request

id, response_text, response_code, response_status, request = test_api()


# Get Current cloudflare DNS IP

# if different:
    # Update Cloudflare DNS With public IP


#setup:
this_file_path = os.path.dirname(os.path.realpath(__file__))
env_file_path = this_file_path + '\.env'

if not os.path.exists(env_file_path): #if ENV file doesn't exist, run setup
    print("Not Already Setup... Setting Up...")
    cloudflare_zone_name = input("What Is your Cloudflare Zone Name? E.g. example.com ")
    cloudflare_zone_id = input("What Is your Cloudflare Zone ID? ")
    device_name = input("What Is Your Device Name? E.g. CryptoidCoders_Laptop ")
    cloudflare_API_token = input("What Is Your CloudFlare API Token? ")
    cloudflare_global_API_key = input("What Is Your Globla CloudFlare API Key? ")
    cloudflare_email = input("What Is Your CloudFlare Email? ")
    addnewline(env_file_path, f"zone_name='{cloudflare_zone_name}'")
    addnewline(env_file_path, f"zone_id='{cloudflare_zone_id}'")
    addnewline(env_file_path, f"record_name='{device_name}'")
    addnewline(env_file_path, f"cloudflare_api_token='{cloudflare_API_token}'")
    addnewline(env_file_path, f"cloudflare_global_api_key='{cloudflare_global_API_key}'")
    addnewline(env_file_path, f"cloudflare_email='{cloudflare_email}'")
else:
    print("Already Setup.")


#main:

if id != 'None' and response_text != 'None' and response_code != 'None' and response_status != 'None':
    print("API Token works")
else:
    print("API Token Doesn't Work")