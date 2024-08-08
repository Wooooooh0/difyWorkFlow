from base64 import b64decode
from datetime import datetime
from typing import Any, Union
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import json
import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

class ToutiaoNewsHotGeneratorTool(BuiltinTool):
    def _invoke(
            self,
            user_id: str,
            tool_parameters: dict[str, Any],
    ) -> ToolInvokeMessage:
        """
        This function invokes the NewsHotGeneratorTool to fetch and process
        trending news data from an external API.

        Args:
        - user_id (str): The user identifier.
        - tool_parameters (dict): Additional parameters for the tool (not used here).

        Returns:
        - ToolInvokeMessage: A message containing trending news items and their links.
        """
        # Send a GET request to fetch trending news data
        resp = requests.get("https://api-hot.efefee.cn/toutiao?cache=true")
        print(resp)

        # Check if the request was successful (status code 200)
        if resp.status_code != 200:
            return self.create_text_message("get not news fail")

        # Parse the JSON respons
        data = resp.json()   # 将回应转化为json格式

        result = data.get('data')  # 获取"data"部分的数据
        print(result)

        # Prepare a list to store messages
        message = []

        # Iterate through each news item in the response
        for data in result:
            # Create a text message for the news item name
            message.append(self.create_text_message(data["title"]))
            # Create a link message for the news item URL
            message.append(self.create_link_message(link=data["url"]))  

        # Return the list of messages
        return message
