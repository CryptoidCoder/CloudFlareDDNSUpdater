#load modules
import requests #for http requests

import os #for ENV intergration:

from dotenv import load_dotenv #for ENV intergration:
load_dotenv() #for ENV intergration:

def test_api(): #test API credentials are correct
    url= 'https://api.cloudflare.com/client/v4/user/tokens/verify'
    api_token = os.getenv("cloudflare_API_token")
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type":"application/json" 
        }

    request = requests.get(url, headers=headers)
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
print(f"ID: {id} \n Response (Text): {response_text} \n Response(Code): {response_code} \n Response(status): {response_status} \n Request: {request}")