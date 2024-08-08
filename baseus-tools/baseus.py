import json

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.spark.tools.spark_img_generation import spark_response
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController

class BaseusProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            if "img_base_url" not in credentials or not credentials.get("img_base_url"):
                raise ToolProviderCredentialValidationError("img_base_url is required.")
            if "audio_base_url" not in credentials or not credentials.get("audio_base_url"):
                raise ToolProviderCredentialValidationError("audio_base_url is required.")
            if "newimage_base_url" not in credentials or not credentials.get("newimage_base_url"):
                raise ToolProviderCredentialValidationError("newimage_base_url is required.")
            if "emotion_audio_base_url" not in credentials or not credentials.get("emotion_audio_base_url"):
                raise ToolProviderCredentialValidationError("emotion_audio_base_url is required.")
            
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
