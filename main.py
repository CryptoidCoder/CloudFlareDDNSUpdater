# Cloudflare DDNs Updater

import os
import requests

from dotenv import load_dotenv
load_dotenv()

# Get Variables From .env file
cloudflare_zone_id = os.getenv("zone_id")
complete_cloudflare_record_name = os.getenv("record_name").lower()+ f'.devices.{os.getenv("zone_name")}'
cloudflare_record_name = os.getenv("record_name").lower()+".devices"
cloudflare_api_key = os.getenv("cloudflare_Global_API_key")
cloudflare_api_token = os.getenv("cloudflare_API_token")
cloudflare_account_email = os.getenv("cloudflare_email")


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

def get_current_ip(): # Get current Public IP
    url = 'https://ifconfig.me/ip' #address of website that will return public IP
    try: #try and get json data from that website, else return error
        current_public_ip = requests.get(url).text
        if current_public_ip != None or current_public_ip != ' ':
            return current_public_ip
        else:
            return f"Unable To Get IP From {url}"
    except:
        return f"Unable To Get IP From {url}"
    
def get_cloudflare_ip(type): #get IP from cloudflare DNS
    if type == 'A': #change cloudflare_record_type depending on type listed A/AAAA (IPv4/IPv6)
        cloudflare_record_type = "A"
    elif type == 'AAAA':
        cloudflare_record_type = "AAAA"
    else:
        cloudflare_record_type = "A"

    # URL for web request
    url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone_id}/dns_records?name={complete_cloudflare_record_name}&type={cloudflare_record_type}"

    # headers for web request (Auth + Content Type)
    headers = {
        "X-Auth-Email": cloudflare_account_email,
        "X-Auth-Key": cloudflare_api_key,
        "Content-Type": "application/json"
        }
    
    request = requests.get(url, headers = headers) #make web request

    # find the json data that states "content" - which holds the IP
    for item in request.json()['result']:
        try:
            cloudflare_ip = item['content']
        except:
            pass
        try:
            cloudflare_ip_dns_id = item['id']
        except:
            pass
    
    return cloudflare_ip, cloudflare_ip_dns_id

def update_cloudflare_ip(type): #update DNS value to current Public IP
    if type == 'A': #change cloudflare_record_type depending on type listed A/AAAA (IPv4/IPv6)
        cloudflare_record_type = "A"
    elif type == 'AAAA':
        cloudflare_record_type = "AAAA"
    else:
        cloudflare_record_type = "A"

    current_ip = get_current_ip() #get current IP using get_current_IP() function
    cloudflare_ip, cloudflare_dns_id = get_cloudflare_ip(cloudflare_record_type) #get DNS ID & cloudflare IP from Cloudfalre DNS

    # URL for web request
    url = f"https://api.cloudflare.com/client/v4/zones/{cloudflare_zone_id}/dns_records/{cloudflare_dns_id}"

    #headers for web request (Auth + Content Type)
    headers = {
        "X-Auth-Email": cloudflare_account_email,
        "X-Auth-Key": cloudflare_api_key,
        "Content-Type": "application/json"
        }

    # data for web request (IPv4/IPv6 Record type, record name, new IP)
    data={
        "type":cloudflare_record_type,
        "name":cloudflare_record_name,
        "content":current_ip,
        "proxied":bool('true'),
        "ttl":120
        }
    
    request = requests.put(url, headers=headers, json= data) #Make web request
    return request.json()


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


# Main:

cloudflare_ip, cloudflare_dns_id = get_cloudflare_ip('A')
if cloudflare_ip != get_current_ip(): #if IP has changed
    update_cloudflare_ip('A')
    print(f"Updated 'A' IP: {get_cloudflare_ip('A')[0]}")
