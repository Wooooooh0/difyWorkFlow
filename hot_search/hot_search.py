from typing import Any

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.hot_search.tools.zhihu_hot import ZhiHuNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.genshin_hot import GenshinNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.weibo_hot import WeiboNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.bilibili_hot import BilibiliNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.douyin_hot import DouyinNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.ThreeSixKr_hot import ThreeSixKrNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.baidu_hot import BaiduNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.sspai_hot import SspaiNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.ithome_hot import IthomeNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.thepaper_hot import ThepaperNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.toutiao_hot import ToutiaoNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.tieba_hot import TiebaNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.juejin_hot import JuejinNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.qqnews_hot import QqNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.doubanmovie_hot import DoubanmovieHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.starrail_hot import StarrailNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.lol_hot import LOLNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.netease_hot import NeteaseNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.weread_hot import WereadNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.doubangroup_hot import DoubangroupHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.ngabbs_hot import NGAbbsNewsHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.hellogithub_hot import HelloGithubHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.jianshu_hot import JianshuHotGeneratorTool
from core.tools.provider.builtin.hot_search.tools.zhihudaily_hot import ZhiHuDailyHotGeneratorTool

from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController

class NewsHotGeneratorTool(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            ZhiHuNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            GenshinNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            WeiboNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            BilibiliNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            DouyinNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            ThreeSixKrNewsHotNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            BaiduNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            SspaiNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            IthomeNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            ThepaperNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            ToutiaoNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            TiebaNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            JuejinNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            QqNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            DoubanmovieHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            StarrailNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            LOLNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            NeteaseNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            WereadNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            DoubangroupHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            NGAbbsNewsHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            HelloGithubHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            JianshuHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
            ZhiHuDailyHotGeneratorTool().invoke(
                user_id='',
                tool_parameters={},
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
