import re

import requests
from bs4 import BeautifulSoup as bs
from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils.paste import pastetext

LOGS = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

plugin_category = "misc"


async def paste_links(magnets):
    urls = []
    for txt in magnets:
        response = await pastetext(txt, pastetype="d", extension="txt")
        if "url" in response:
            urls.append(response["url"])
        else:
            return None
    return urls


@catub.cat_cmd(
    pattern="tsearch(?:\s|$)([\s\S]*)",
    command=("tsearch", plugin_category),
    info={
        "header": "To search torrents.",
        "flags": {"-l": "for number of search results to check  ."},
        "usage": "{tr}tsearch <query>",
        "examples": ["{tr}tsearch avatar", "{tr}tsearch -l5 avatar"],
    },
)
async def tor_search(event):  # sourcery no-metrics
    """
    To search torrents
    """
    search_str = event.pattern_match.group(1)
    lim = re.findall(r"-l\d+", search_str)
    try:
        lim = lim[0]
        lim = lim.replace("-l", "")
        search_str = search_str.replace("-l" + lim, "")
        lim = int(lim)
        if lim < 1 or lim > 20:
            lim = 10
    except IndexError:
        lim = 10
    catevent = await edit_or_reply(
        event, f"`Searching torrents for " + search_str + ".....`"
    )
    if " " in search_str:
        search_str = search_str.replace(" ", "+")
        res = requests.get(
            "https://www.torrentdownloads.me/search/?new=1&s_cat=0&search="
            + search_str,
            headers,
        )
    else:
        res = requests.get(
            "https://www.torrentdownloads.me/search/?search=" + search_str, headers
        )
    source = bs(res.text, "lxml")
    urls = []
    magnets = []
    titles = []
    counter = 0
    lim = lim+2
    for div in source.find_all("div", {"class": "grey_bar3 back_none"}):
        try:
            title = div.p.a["title"]
            title = title[20:]
            titles.append(title)
            urls.append("https://www.torrentdownloads.me" + div.p.a["href"])
        except (KeyError, TypeError, AttributeError):
            pass
        except Exception as e:
            return await edit_delete(
                catevent, f"**Error while doing torrent search:**\n{str(e)}"
            )
        if counter == lim:
            break
        counter += 1
    if not urls:
        return await edit_delete(
            catevent, "__Either the query was restricted or not found..__"
        )
    for url in urls:
        res = requests.get(url, headers)
        source = bs(res.text, "lxml")
        for div in source.find_all("div", {"class": "grey_bar1 back_none"}):
            try:
                mg = div.p.a["href"]
                magnets.append(mg)
            except TypeError:
                pass
            except Exception as e:
                LOGS.info(str(e))
    if not magnets:
        return await edit_delete(catevent, "__Unable to fetch magnets.__")
    shorted_links = await paste_links(magnets)
    if shorted_links is None:
        return await edit_delete(catevent, "__Unable to fetch results.__")
    msg = f"**Torrent Search Query**\n`{search_str.replace('+', ' ')}`\n**Results**\n"
    counter = 0
    while counter != len(shorted_links):
        msg += f"⁍ [{titles[counter]}]({shorted_links[counter]})\n\n"
        counter += 1
    await catevent.edit(msg, link_preview=False)