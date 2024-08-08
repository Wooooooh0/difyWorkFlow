# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time
import urllib.parse
from base64 import b64decode
from datetime import datetime
from typing import Any, Union
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import requests
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class NewsHotGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:
        resp = requests.get("https://tenapi.cn/v2/toutiaohot")
        if resp.status_code != 200:
            return self.create_text_message("get not news fail") 
        
        resulf = json.loads(resp.text)
        message = [] 
        for data in resulf["data"]:
            message.append(self.create_text_message(data["name"]))
            message.append(self.create_link_message(link = data["url"]))
        return message
        













