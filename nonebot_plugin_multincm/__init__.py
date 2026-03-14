import asyncio

from nonebot import get_driver
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")
require("nonebot_plugin_localstore")
require("nonebot_plugin_htmlrender")

from . import interaction as interaction
from .config import ConfigModel, config
from .const import SONG_CACHE_DIR
from .data_source import login, registered_searcher
from .interaction import load_commands

if config.clean_cache_on_startup:
    import shutil

    if SONG_CACHE_DIR.exists():
        shutil.rmtree(SONG_CACHE_DIR)

driver = get_driver()


@driver.on_startup
async def _():
    asyncio.create_task(login())


load_commands()

search_commands_help = "\n".join(
    [
        f"- **{cmds[0]} [{(c := s.child_calling)}名 / {c} ID]** - 搜索{c} (若输ID则直发)\n"
        f"  别名：{'、'.join(f'**{x}**' for x in cmds[1:])}"
        for s, cmds in registered_searcher.items()
    ],
)
auto_resolve_tip = (
    "> 💡 提示：Bot 会自动解析你发送的网易云链接\n" if config.auto_resolve else ""
)

__version__ = "1.3.1.post1"

__plugin_meta__ = PluginMetadata(
    name="网易云点歌",
    description="MultiNCM，网易云多选点歌",
    usage=(
        "## 🔍 搜索指令\n\n"
        f"{search_commands_help}"
        "\n\n"
        "## ▶️ 操作指令\n\n"
        "- **解析 [回复 卡片/链接]** - 获取音乐信息发卡片\n"
        "  别名：**resolve**、**parse**\n"
        "- **直链 [回复 卡片/链接]** - 获取音乐下载链接\n"
        "  别名：**direct**\n"
        "- **下载歌曲 [回复 卡片/链接]** - 下载并上传到群文件\n"
        "  别名：**下载**、**download_song**\n"
        "- **歌词 [回复 卡片/链接]** - 获取歌词并发图片\n"
        "  别名：**lrc**、**lyric**\n"
        "\n"
        f"{auto_resolve_tip}"
        "> 💡 提示：点击卡片跳转官网，未回复则自动解析近期发出的卡片"
    ),
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-multincm",
    type="application",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_waiter",
    ),
    extra={
        "author": "LgCookie",
        "version": __version__,
        "menu_type": "功能",
    },
)
