import requests
import colorama
from requests.auth import HTTPBasicAuth
from colorama import Fore, Back, Style, init

def update_noip(ip=None):
    from serverpanelcreds import USERNAME, PASSWORD, HOSTNAME
    url = "http://dynupdate.no-ip.com/nic/update"
    params = {"hostname": HOSTNAME}
    if ip:
        params["myip"] = ip

    response = requests.get(url, params=params, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 200:
        print(Fore.YELLOW + "   - NoIP updated successfully.")
    else:
        print(Fore.RED + Style.BRIGHT + "   - Failed to update NoIP.")