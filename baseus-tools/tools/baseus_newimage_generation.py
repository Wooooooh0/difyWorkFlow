
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

from core.tools.entities.common_entities import I18nObject
from core.tools.entities.tool_entities import ToolInvokeMessage, ToolParameter, ToolParameterOption
from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.tool.builtin_tool import BuiltinTool
from core.file.upload_file_parser import UploadFileParser

class BaseusNewImg:
    def __init__(self, image_url: str) -> None:
        self.baseusurl = image_url

    def set_signature(self):
        timestamp = int(time.time())
        session_str = str(timestamp)
        md5 = hashlib.md5()
        md5.update(session_str.encode('utf-8'))
        return md5.hexdigest()
        
    def post_imge(self, data):
        self.image_name = self.set_signature() + ".png"
        files = {
            'files': (self.image_name, data, 'multipart/form-data', {'Content-Disposition': 'form-data; name="files"; filename={image_name}'})
        }

        self.params = {'upload_id': self.image_name[:8]}

        resp = requests.post(self.baseusurl + "/upload", params = self.params, files = files)
        if resp.status_code == 200:
            self.temp_image = resp.text.strip('[]').strip('""')
            return resp.text
        return None
    
    def get_result(self):
        response = requests.get(self.baseusurl + "/upload_progress",  params = self.params, stream=True)
        if response.status_code != 200:
            print("upload_progress response", response.text)
            return None
        return response

    def post_imge_task(self, data):
        resp = self.post_imge(data)
        if resp == None:
            return None

        response = self.get_result()
        if response == None:
            return None
        
        for line in response.iter_lines():
            if line:
                resp = str(line.decode('utf-8'))
                if ('done' in resp):
                    print("upload_progress done", resp)
                    return resp
        return None
    
    def get_image_task(self):
        response_image = requests.get(self.baseusurl +  "/file=" + self.temp_image)
        if response_image.status_code != 200:
            return None
        
        Content_Length = int(response_image.headers['Content-Length'])
 
        session_hash = self.set_signature()[:8]
        body = {
            "data" : [{
                "path" : self.temp_image, 
                "url"  : self.baseusurl + "/file=" + self.temp_image,
                "orig_name": self.image_name,
                "size": Content_Length,
                "mime_type":""
            }],
            "event_data":  None, 
            "fn_index":     1, 
            "trigger_id":   9, 
            "session_hash": session_hash
        }

        resp = requests.post(self.baseusurl + "/queue/join", data = json.dumps(body), headers = {"Content-Type":"application/json; charset=utf-8"})
        if resp.status_code != 200:
            return None
        
        response = requests.get(self.baseusurl + "/queue/data", params =  {'session_hash': session_hash}, stream = True)
        for line in response.iter_lines():
            if line:
                resp = str(line.decode('utf-8'))
                if ('process_completed' in resp):
                    format_json = resp[6:]
                    resp_json = json.loads(format_json)
                    key = resp_json['output']['data'][0][1]
                    image_url = key['path']
                    return self.baseusurl + "/file=" + image_url
        return None

    def download_imge(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None


class BaseusNewImageGeneratorTool(BuiltinTool):
    def _invoke(self, 
            user_id: str, 
            tool_parameters: dict[str, Any]
        ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        image_url = self.runtime.credentials.get("newimage_base_url", None)
        if not image_url:
            raise ToolProviderCredentialValidationError('Please input api image url')
                
        # 获取image_id，image_id的定义可以在get_runtime_parameters中找到
        image_id = tool_parameters.get('files', '')
        if not image_id:
            return self.create_text_message('Please input image files')
        
        base = BaseusNewImg(image_url)
        image_data = base.download_imge(image_id[0]['url'])
        if image_data == None:
            return self.create_text_message('image_data None')
        
        resp = base.post_imge_task(image_data)
        if resp == None:
            return self.create_text_message('image_data None')
        
        image_new_url = base.get_image_task()
        if image_new_url == None:
            return self.create_text_message('image_new_url None')
        
        image_new_data = base.download_imge(image_new_url)
        if image_new_data == None:
            return self.create_text_message('image_new_data None')

        return [ self.create_blob_message(blob = image_new_data,
                                         meta={'mime_type': 'image/png'}),               self.create_link_message(link = image_id[0]['url'])]













