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

tts_voice = [
    ["*random","*random"],
    ["female" , "Bob"],
    ["female" , "bob_ft10"],
    ["female" , "female2"],    
    ["female" , "声音有点像陈一发"],
    ["female" , "电视台女主持"],
    ["female" , "知心小姐姐"],
    ["male" , "Alice"],
    ["male" , "纯情男大学生"],
    ["male" , "阳光开朗大男孩"],
    ["male" , "魅力大叔"],
    ["女性" , "严肃女领导"],
    ["女性" , "嗲嗲的很酥麻"],
    ["女性" , "大虎妞"],
    ["女性" , "歪果仁讲中文"],
    ["女性" , "比较甜美"],
    ["女性" , "知书达理"],
    ["女性" , "音色有韵味带磁性"],
    ["男性" , "做事很着急的领导"],
    ["男性" , "天生男低音"],
    ["男性" , "好哥们"],
    ["男性" , "娘娘腔"],
    ["男性" , "娘娘腔拉满了"],
    ["男性" , "文弱书生"],
    ["男性" , "有磁性的男播音"],
    ["男性" , "正式"],
    ["男性" , "班级话痨"]
]

style = [
    ["*auto","*auto"],
    ["advertisement_upbeat","advertisement_upbeat"],
    ["affectionate","affectionate"],
    ["angry","angry"],
    ["assistant","assistant"],
    ["calm","calm"],
    ["chat","chat"],
    ["cheerful","cheerful"],
    ["customerservice","customerservice"],
    ["depressed","depressed"],
    ["disgruntled","disgruntled"],
    ["documentary-narration","documentary-narration"],
    ["embarrassed","embarrassed"],
    ["empathetic","empathetic"],
    ["envious","envious"],
    ["excited","excited"],
    ["fearful","fearful"],
    ["friendly","friendly"],
    ["gentle","gentle"],
    ["hopeful","hopeful"],
    ["lyrical","lyrical"],
    ["narration-professional","narration-professional"],
    ["narration-relaxed","narration-relaxed"],
    ["newscast","newscast"],
    ["newscast-casual","newscast-casual"],
    ["newscast-formal","newscast-formal"],
    ["poetry-reading","poetry-reading"],
    ["sad","sad"],
    ["serious","serious"],
    ["shouting","shouting"],
    ["sports_commentary","sports_commentary"],  
]

tone = [
    "[lbreak]", 
    "[laugh]", 
    "[uv_break]", 
    "[v_break]",
]


tts_message = {
   "data":  ["倍思 T T S 是一款强大的对话式文本转语音模型。它有中英混读和多说话人的能力。 [lbreak]",
             0.3,           #温度
             0.7,           #Top P
             20,            #Top K
            "比较甜美",     #声色
            42,             #推理种子
            True,
            "",
            "",
            "",
            "*auto",        #后缀为 _p 表示带prompt，效果更强但是影响质量
            False,          #禁用文本预处理
            4,              #批量大小
            True,           #启动人声增强
            False,          #启动背景降噪
            None,
            100,            #分割器阈值
            "[uv_break]"    #句尾词
        ],
    "event_data":None,
    "fn_index":10,
    "trigger_id":84,
    "session_hash":"s3pirsc4uqm"
}

class EmotionTTS:
    def __init__(self, url:str):
        self.url = url
    
    def post_message(self):
        tts_message["session_hash"] = self.set_signature()[:10] 
        response = requests.post(self.url + "/queue/join", data = json.dumps(tts_message), params = "__theme=dark")
        if response.status_code != 200:
            print("response", response.text)
            return None
        
        response = requests.get(self.url + "/queue/data", params =  {'session_hash': tts_message["session_hash"]}, stream = True)
        if response.status_code != 200:
            print("response", response.text)
            return None
        
        for line in response.iter_lines():
            if line:
                resp = str(line.decode('utf-8'))
                if ('process_completed' in resp):
                    format_json  = resp[6:]
                    resp_json    = json.loads(format_json)
                    audio_tts    = resp_json["output"]["data"][0]["url"]
                    print(audio_tts)
                    return audio_tts
        return None
    
    def set_signature(self):
        timestamp = int(time.time())
        session_str = str(timestamp)
        md5 = hashlib.md5()
        md5.update(session_str.encode('utf-8'))
        return md5.hexdigest()  
                
class BaseusEmotionAudioGeneratorTool(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        if "emotion_audio_base_url" not in self.runtime.credentials or not self.runtime.credentials.get("emotion_audio_base_url"):
            return self.create_text_message("img_base_urlis required.")
        
        tts_url = self.runtime.credentials.get("emotion_audio_base_url")
        
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            return self.create_text_message("Please input prompt")
       
        voice = tool_parameters.get("voice", "")
        if not voice:
            return self.create_text_message("Please input voice")
       
        style = tool_parameters.get("style", "")
        if not style:
            return self.create_text_message("Please input style")
        
        tone = tool_parameters.get("tone", "")
        if not tone:
            return self.create_text_message("Please input tone")
       
        tts_message["data"][0]  = prompt + "  [" + tone + "]"
        tts_message["data"][4]  = voice
        
        if style == "auto":
            style = "*auto"
            
        tts_message["data"][10] = style
        
        tts_message["data"][17] = "[" + tone + "]"
        
        emotion = EmotionTTS(tts_url)
        
        url_tts = emotion.post_message()
        if url_tts is None:
            return self.create_text_message("emotion error")
        
        return  self.create_link_message(link = url_tts)












