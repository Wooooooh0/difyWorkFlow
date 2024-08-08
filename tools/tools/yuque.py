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


class ExpressInquiry:
    def __init__(self, key :str, user_id:str, odd_numbers: str, number: str, company: str):
        self.key         = key
        self.id          = user_id
        self.odd_numbers = odd_numbers
        self.number      = number
        self.company     = company

    def md5_encrypt(self, input_string:str):
        # 使用 UTF-8 编码将字符串转换为字节流
        byte_string = input_string.encode('utf-8')
    
        # 创建 MD5 对象
        md5_hash = hashlib.md5()
    
        # 更新哈希对象的输入
        md5_hash.update(byte_string)
    
        # 获取十六进制的 MD5 值
        encrypted_string = md5_hash.hexdigest()

        byte_string1 = encrypted_string.encode('utf-8')

        encoded_bytes2 = base64.b64encode(byte_string1)

        encoded_string3 = encoded_bytes2.decode('utf-8')

        encoded_string4 = urllib.parse.quote(encoded_string3)
        
        return encoded_string4

    def start_express_inquiry(self):
        #SF1845502106788
        #SF3119652236473
        #130f0832-475d-4c81-a33c-cfd44be402c9
        if self.odd_numbers[0] == "S" and self.odd_numbers[1] == "F":
            if self.number is None:
                return "You are SF Express, please enter the last 4 digits of your phone number"
            if len(self.number) < 4 or len(self.number) > 4:
                return "You are SF Express, You entered a phone number with less than 4 digits"

            data = {
                "LogisticCode" : self.odd_numbers,
                "CustomerName": self.number, 
                "ShipperCode": "SF"
            }
        else :
            data = {
                "LogisticCode" : self.odd_numbers,
                "ShipperCode"  : self.company,
            }
        print(self.company)
        encrypt = self.md5_encrypt(str(data) + self.key)
        
        body = {
            "RequestData"  : str(data),
            "RequestType"  : "8001",
            "EBusinessID"  : self.id,
            "DataType"     : "2",
            "DataSign"     : encrypt
        }

        resp = requests.post("https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx", data = body)
        if resp.status_code != 200:
            return None
        return resp.text

class BaseusImgGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:

        if "yuque_id" not in self.runtime.credentials or not self.runtime.credentials.get("yuque_id"):
            return self.create_text_message("yuque_id required.")
        
        if "yuque_key" not in self.runtime.credentials or not self.runtime.credentials.get("yuque_key"):
            return self.create_text_message("yuque_key required.")
            
        tracking_number = tool_parameters.get("tracking_number", None)
        if not tracking_number:
            return self.create_text_message("Please input the tracking_number")
  
        yuque_key = self.runtime.credentials.get('yuque_key', None)      
        if not yuque_key:
            return self.create_text_message("Please input yuque key")
        
        yuque_id = self.runtime.credentials.get('yuque_id', None)      
        if not yuque_id:
            return self.create_text_message("Please input yuque id")
        
        number = tool_parameters.get("number", None)
        
        express_company = tool_parameters.get("express_company", "SF")
        if not tracking_number:
            return self.create_text_message("Please input the express_company")
        
        express = ExpressInquiry(yuque_key, yuque_id, tracking_number, number, express_company)        
        
        resp = express.start_express_inquiry()
        if resp is None:
            return self.create_text_message("Express query failed")

        return self.create_text_message(f"{resp}")
        













