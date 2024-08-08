# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time
from base64 import b64decode

from datetime import datetime
from typing import Any, Union
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

image_body = {
    "data" : ["sdxl","","","auto",1,1024,1024],
    "event_data": None,
    "fn_index": 1,
    "trigger_id": 6,
    "session_hash": None
}

class BaseusImg:
    def __init__(self, url: str, prompt:str, style:str, 
            NegativePrompt:str, num_image:int, width:int, high:int):
        
        self.url = url
        self.prompt = prompt
        self.style = style
        self.NegativePrompt = NegativePrompt
        self.num_image  = num_image
        self.width = width
        self.high = high
        
    #"data" : [self.text, self.steps]
    def set_signature(self, data: str):
        timestamp = int(time.time())
        session_str = str(data) + str(timestamp)
        md5 = hashlib.md5()
        md5.update(session_str.encode('utf-8'))
        self.signature = md5.hexdigest()[:11]
        return self.signature

    def text_to_image(self, image_body):
        body = image_body

        body["data"][1] = self.prompt
        if self.NegativePrompt is None:
            body["data"][2] = ""
        else:
            body["data"][2] = self.NegativePrompt
        
        body["data"][3] = self.style
        body["data"][4] = self.num_image
        body["data"][5] = self.width
        body["data"][6] = self.high

        body["session_hash"] = self.set_signature(body["data"])

        body_run = {
            "data":[0],
            "event_data": None,
            "fn_index": 2,
            "trigger_id": 28,
            "session_hash": body["session_hash"]
        }

        response = requests.request("POST", url = self.url + "/run/predict", data = json.dumps(body_run))
        if response.status_code != 200:
            return None
        
        response = requests.request("POST", url = self.url + "/queue/join?", data = json.dumps(body))
        if response.status_code != 200:
            return None

        resp = json.loads(response.text)
        return resp

    def download_image_data(self, url):
         response = requests.get(url)
         if response.status_code == 200:
             return response.content
         return None

    def get_result(self):
        resp_url = []
        response = requests.get(self.url + "/queue/data", params =  {'session_hash': self.signature}, stream = True)
        for line in response.iter_lines():
            if line:
                resp = str(line.decode('utf-8'))
                if ('process_completed' in resp):
                    resp_result = json.loads(resp[6:])
                    for image in resp_result['output']["data"][0]:
                        #image_data = self.download_image_data(image['image']["url"])
                        resp_url.append(image['image']["url"])
                    return resp_url
        return None

class BaseusImgGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:
        """
        invoke tools
        """
        if "img_base_url" not in self.runtime.credentials or not self.runtime.credentials.get("img_base_url"):
            return self.create_text_message("img_base_urlis required.")
            
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            return self.create_text_message("Please input prompt")
  
        style = tool_parameters.get("style", "auto")

        NegativePrompt = tool_parameters.get("NegativePrompt", "")

        image_url = self.runtime.credentials.get('img_base_url', None)      
        if not image_url:
            return self.create_text_message("Please input image_url")

        num_image = int(tool_parameters.get("num_image", "1"))
        print("num_image", num_image)
        width = int(tool_parameters.get("width", "1024"))
        
        high = int(tool_parameters.get("high", "1024"))
        
        baseus = BaseusImg(image_url, prompt, style, NegativePrompt, num_image, width, high)        
        
        resp = baseus.text_to_image(image_body)
        if resp is None:
            return self.create_text_message("image error ")
        
        resp_data = baseus.get_result()
        if resp_data is None:
            return self.create_text_message("image error ")
        resulf = [] 
        for data in resp_data:
            resulf.append(self.create_image_message(image = data))

        if resulf is None:
            return self.create_text_message("image error ")
        
        return resulf













