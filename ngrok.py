import subprocess
import importlib
import requests

try:
    # Attempt to import pyngrok to check for its existence
    import pyngrok
except ImportError:
    
    subprocess.check_call(["pip", "install", "pyngrok"])
    importlib.reload(pyngrok)

from pyngrok import ngrok
from pyngrok import conf
import sys

# Change these to your own settings
auth_token = "2TpKk6ZAicA3r8wwQmi0nIOyyRd_2QPuXXL2HV597GW8tSNhc"
protocol = "tcp"
portn = "25565"
region = "ap"

pyngrok_config = conf.PyngrokConfig(log_event_callback=None, max_logs=10)
conf.set_default(pyngrok_config)

ngrok.conf.get_default().region = region
ngrok.set_auth_token(auth_token)

ngrok_process = ngrok.get_ngrok_process()

def start_tunnel():
    
    print("Starting ngrok tunnel process", flush=True)
    
    try:
        tunnel = ngrok.connect(portn, protocol, name="minecraft",)
        print("Public URL:", tunnel.public_url, flush=True)
        server = True 
        send_url(tunnel.public_url, server)
        print("Press Ctrl+C to quit", flush=True)
        ngrok_process.proc.wait()
        
    except KeyboardInterrupt:
        print("Shutting down server", flush=True)
        server = False 
        send_url(tunnel.public_url, server)
        ngrok.kill()
        sys.exit()

def send_url(url, status):
    webhook = "https://discord.com/api/webhooks/1191375256598884352/Rge1OnIA8eCRQx8a3jwzmOZTyj3OEGbFTsg2XI1-TFNIij4uctDkRgHjeQGuf6y4fv09"
    public_url = url
    status = status
    
    if status == True:
        msg = ":green_circle: Server is UP! Address:" +public_url 
    else:                                           # Change this to your server status
        msg = ":red_circle: Server was SHUT DOWN!" 
        
    headers = {
    'Accept': 'application/json',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    }

    json_data = {
        'content': msg,
    }
    response = requests.post(webhook, headers=headers, json=json_data)
    print(response.status_code)  # Print the response status code


start_tunnel()