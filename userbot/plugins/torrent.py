# torrent module for catuserbot
from asyncio import sleep
from ..core.logger import logging
from userbot import catub
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)
plugin_category = "misc"


@catub.cat_cmd(
    pattern="fromurl(?: |$)(.*)",
    command=("fromurl", plugin_category),
    info={
        "header": "To get random quotes on given topic.",
        "description": "Downloads the file into your userbot server storage",
        "usage": "{tr}fromurl URL",
    },
)
async def aurl_download(event):
    "Add url Into Queue."
    uri = [event.pattern_match.group(1)]
    try:
        from .torrentutils import aria2, check_metadata, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    try:  # Add URL Into Queue
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        return await edit_delete(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    catevent = await edit_or_reply(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=catevent, previous=None)
    t_file = aria2.get_download(gid)
    if t_file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=catevent, previous=None)


@catub.cat_cmd(
    pattern="amag(?: |$)(.*)",
    command=("amag", plugin_category),
    info={
        "header": "Add Magnet URI Into Queue",
        "description": "Downloads the file into your userbot server storage.",
        "usage": "{tr}amag <URL of torrent file>",
    },
)
async def magnet_download(event):
    "Add Magnet URI Into Queue"
    magnet_uri = event.pattern_match.group(1)
    try:
        from .torrentutils import aria2, check_metadata, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        return await edit_delete(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    catevent = await edit_or_reply(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=catevent, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=catevent, previous=None)


@catub.cat_cmd(
    pattern="ator(?: |$)(.*)",
    command=("ator", plugin_category),
    info={
        "header": "Add Torrent Into Queue",
        "description": "First download tor file using {tr}download cmd and then use that path for this cmd. This cmd will Download the file into your userbot server storage.",
        "usage": "{tr}ator <path to torrent file>",
    },
)
async def torrent_download(event):
    "Add Torrent Into Queue"
    torrent_file_path = event.pattern_match.group(1)
    try:
        from .torrentutils import aria2, check_progress_for_dl
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await edit_delete(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    catevent = await edit_or_reply(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=catevent, previous=None)


@catub.cat_cmd(
    pattern="aclear$",
    command=("aclear", plugin_category),
    info={
        "header": "Clear the aria Queue.",
        "description": "Clears the download queue, deleting all on-going downloads.",
        "usage": "{tr}aclear",
    },
)
async def remove_all(event):
    "Clear the aria Queue."
    try:
        from .torrentutils import aria2, subprocess_run
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge()
    except Exception as e:
        event = await edit_or_reply(event, f"**Error :**\n`{str(e)}`")
        await sleep(5)
    if not removed:  # If API returns False Try to Remove Through System Call.
        subprocess_run("aria2p remove-all")
    await edit_or_reply(event,"`Clearing on-going downloads... `")
    await sleep(2.5)
    await edit_or_reply(event,"`Successfully cleared all downloads.`")


@catub.cat_cmd(
    pattern="apause$",
    command=("apause", plugin_category),
    info={
        "header": "Pause ALL Currently Running Downloads.",
        "description": "Pause on-going downloads.",
        "usage": "{tr}apause <topic>",
        "examples": "{tr}apause love",
    },
)
async def pause_all(event):
    "Pause ALL Currently Running Downloads."
    try:
        from .torrentutils import aria2
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    catevent = await edit_or_reply(event, "`Pausing downloads...`")
    aria2.pause_all(force=True)
    await sleep(2.5)
    await catevent.edit("`Successfully paused on-going downloads.`")


@catub.cat_cmd(
    pattern="aresume$",
    command=("aresume", plugin_category),
    info={
        "header": "TResume ALL Currently Running Downloads..",
        "description": "Resumes on-going downloads.",
        "usage": "{tr}aresume",
    },
)
async def resume_all(event):
    "Resume ALL Currently Running Downloads."
    try:
        from .torrentutils import aria2
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    catevent = await edit_or_reply(event, "`Resuming downloads...`")
    aria2.resume_all()
    await sleep(1)
    await edit_delete(catevent, "`Downloads resumed.`")


@catub.cat_cmd(
    pattern="ashow$",
    command=("ashow", plugin_category),
    info={
        "header": "Shows current aria progress.",
        "description": "Shows progress of the on-going downloads.",
        "usage": "{tr}ashow",
    },
)
async def show_all(event):
    "Shows current aria progress of queue"
    try:
        from .torrentutils import aria2
    except:
        return await edit_delete(
            event,
            "`You also need to have torrentutils file ask in `@catuserbot_support `to get it`",
        )
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = (
            msg
            + "**File: **`"
            + str(download.name)
            + "`\n**Speed : **"
            + str(download.download_speed_string())
            + "\n**Progress : **"
            + str(download.progress_string())
            + "\n**Total Size : **"
            + str(download.total_length_string())
            + "\n**Status : **"
            + str(download.status)
            + "\n**ETA : **"
            + str(download.eta_string())
            + "\n\n"
        )
    await edit_or_reply(event, "**On-going Downloads: **\n" + msg)
