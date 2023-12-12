"""Shelly API Helper Class"""
import json
import sys
import requests

# https://shelly-api-docs.shelly.cloud/gen1/#shelly-plug-plugs
class Shelly():
    """Shelly Plug/PlugS API Cass"""
    def __init__(self, device, username=None, password=None):
        self.username = username
        self.password = password
        self.proto = "http"
        self.__url = self.proto + "://" + device

    def req_get(self, path):
        """api get request"""
        session = requests.Session()
        if self.username and self.password:
            session.auth = (self.username, self.password)
        try:
            response = session.get(self.__url + path, timeout=3)
            response.raise_for_status()
        except (requests.RequestException) as error:
            print(f"API Error {response.status_code} with reponse: {error}")
            sys.exit(1)
        return json.loads(response.text)

    def get_powermeter(self):
        """read power"""
        return self.req_get('/meter/0/power')

    def get_state(self):
        """return power state True/False"""
        shelly_state = self.req_get('/status')
        return shelly_state['relays'][0]['ison']

    def power_on(self, timer=None):
        """turn power on, if not always on"""
        if self.get_state():
            return None
        timer_param = f"&timer={timer}" if timer else ""
        return self.req_get("/relay/0?turn=on" + timer_param)

    def power_off(self):
        """turn power off, if not always off"""
        if not self.get_state():
            return None
        return self.req_get('/relay/0?turn=off')
