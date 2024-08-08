# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time

from datetime import datetime
from typing import Any, Union
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class baseusAudio:
    def __init__(self, url:str):
        self.url = url
    
    def post_predict(self):
        self.session_hash = self.set_signature()[:10]    
        body = {
                "data":[1],
                "event_data":None,
                "fn_index":0,
                "trigger_id":24,
                "session_hash": self.session_hash
        }
        
        resp = requests.request("POST", self.url + "/run/predict", data = json.dumps(body), headers = {"Content-Type":"application/json; charset=utf-8"})
        if resp.status_code != 200:
            return None
        data = json.loads(resp.text)
        self.path = data['data'][2]['value']['path']
        return self.path

    def post_audio(self, prompt, language):
        body = {
            "data" : [prompt, language,
                {
                    "path": self.path,
                    "url" : None,
                    "size": None,
                    "orig_name":"female.wav",
                    "mime_type":None
                },
                None, False, False, False, True
            ],
            "event_data": None,
            "fn_index": 1,
            "trigger_id": 14,
            "session_hash": self.session_hash
        }

        resp = requests.post(self.url + "/queue/join", data = json.dumps(body), headers = {"Content-Type":"application/json; charset=utf-8"})
        if resp.status_code != 200:
            return None

        response = requests.get(self.url + "/queue/data", params =  {'session_hash': self.session_hash}, stream = True)
        print(response.url)
        for line in response.iter_lines():
            if line:
                resp = str(line.decode('utf-8'))
                if ('process_completed' in resp):
                    format_json  = resp[6:]
                    resp_json    = json.loads(format_json)
                    audio_mp4    = self.url + "/file=" + resp_json["output"]["data"][0]["video"]["path"]
                    audio_output = self.url + "/file=" + resp_json["output"]["data"][1]["path"]
                    audio_female = self.url + "/file=" + resp_json["output"]["data"][3]["path"]
                    return [audio_mp4, audio_output, audio_female]
        return None
    
    def set_signature(self):
        timestamp = int(time.time())
        session_str = str(timestamp)
        md5 = hashlib.md5()
        md5.update(session_str.encode('utf-8'))
        return md5.hexdigest()
    
    def get_audio(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
                
class BaseusAudioGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        if "audio_base_url" not in self.runtime.credentials or not self.runtime.credentials.get("audio_base_url"):
            return self.create_text_message("img_base_urlis required.")
            
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            return self.create_text_message("Please input prompt")
  
        language = tool_parameters.get("language", "")
        if not language:
            return self.create_text_message("Please input language")

        print(self.runtime.credentials.get("audio_base_url"), prompt, language)

        audio = baseusAudio(self.runtime.credentials.get("audio_base_url"))

        code = audio.post_predict()
        if code == None:
            return self.create_text_message("post dest error")

        result = audio.post_audio(prompt, language)
        if result == None:
            return self.create_text_message("pos audio error")
        
        audio_result = []

        for path in result:
            audio_result.append(self.create_link_message(link = path))

        return  audio_result












