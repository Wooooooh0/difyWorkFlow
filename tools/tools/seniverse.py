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


class weather:
    def __init__(self, key :str, area :str):
        self.key = key
        self.area = area

    def query_history(self):
        resp = requests.get("https://tenapi.cn/v2/history")
        if resp.status_code != 200:
            return None
        return resp.text
    
    def now_weather(self):
        key = "key=" + self.key
        location = "&location=" + self.area
        language = "&language=zh-Hans"
        unit     = "&unit=c"
        day     = "&days=7"
        start    = "&start=0"

        message = []

        resp = requests.get("https://api.seniverse.com/v3/weather/now.json", params = f"{key}{location}{language}{unit}")
        if resp.status_code != 200:
            return None

        message.append(resp.text)

        resp1 = requests.get("https://api.seniverse.com/v3/life/driving_restriction.json", params = f"{key}{location}")
        if resp1.status_code != 200:
            return None

        message.append(resp1.text)
        
        resp2 = requests.get("https://api.seniverse.com/v3/life/suggestion.json", params = f"{key}{location}{language}{day}")
        if resp2.status_code != 200:
            return None
        message.append(resp2.text)

        resp3 = requests.get("https://api.seniverse.com/v3/life/chinese_calendar.json", params = f"{key}{start}{day}")
        if resp3.status_code != 200:
            return None
        
        message.append(resp3.text)
        
        resp4 = requests.get("https://api.seniverse.com/v3/weather/daily.json", params = f"{key}{location}{language}{unit}{start}{day}")
        if resp4.status_code != 200:
            return None
        
        message.append(resp4.text)

        return message

class BaseusImgGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:

        if "seniverse_key" not in self.runtime.credentials or not self.runtime.credentials.get("seniverse_key"):
            return self.create_text_message("seniverse_ky required.")
            
        area = tool_parameters.get("area", "")
        if not area:
            return self.create_text_message("Please input area")
  
        seniverse_key = self.runtime.credentials.get('seniverse_key', None)      
        if not seniverse_key:
            return self.create_text_message("Please input seniverse key")
        
        wea  = weather(seniverse_key, area)
        
        message = []

        message.append(self.create_text_message(wea.query_history()))

        resp = wea.now_weather()
        if resp is None:
            return self.create_text_message("get weather error")
        
        for data in resp:
            message.append(self.create_text_message(data))

        return message












