#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: parse_feed.py <episodes_folder> <base-url> <youtube-rss-url>
'''
import sys
import shutil
import os
from collections import defaultdict
import feedparser as fp
import youtube_dl
from templates import HUGO_CONFIG, ENTRY


def main(url, episodes_folder, baseurl):
    r = defaultdict(str)

    feed = fp.parse(url)

    if feed.bozo:
        raise ValueError(feed.bozo_exception)

    f = feed["feed"]

    # Write main config
    with open("site/config.toml", "w") as CONFIG:
        print(HUGO_CONFIG.format(baseurl=baseurl,
                                 title=f.get("title", ""),
                                 author=f.get("author", ""),
                                 yturl=f.get("link", "")),
              file=CONFIG)

    # shared options for youtube-dl
    #--extract-audio --audio-format mp3 --audio-quality 192k
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': []
    }

    if not os.path.isdir(episodes_folder):
        os.makedirs(episodes_folder)

    # Write individual entries
    for e in feed.entries:
        target_filename = os.path.join(episodes_folder,
                                       "{}.mp3".format(e["yt_videoid"]))
        postfile = "site/content/episode/{id}.md".format(id=e["yt_videoid"])

        if os.path.isfile(target_filename): # and os.path.isfile(postfile):
            print("Already processed, skipping: {}".format(e.get("title", e["yt_videoid"])))
            continue

        global CURRENT_FILE, CURRENT_BYTES
        CURRENT_FILE = None
        CURRENT_BYTES = None

        def hook(d):
            global CURRENT_FILE, CURRENT_BYTES
            if d['status'] == 'finished':
                # Called after youtube download, not after re-encode, hence the filename change
                CURRENT_BYTES = d['total_bytes']
                CURRENT_FILE = os.path.splitext(d['filename'])[0] + ".mp3"

        ydl_opts['progress_hooks'] = [hook]

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # List of urls
            ydl.download([e["link"]])

        print("Moving '{}' to '{}'".format(CURRENT_FILE, target_filename))
        shutil.move(CURRENT_FILE, target_filename)

        # Duration = size / bitrate (which is kbits per second)
        # this will not be accurate to the second
        total_secs = CURRENT_BYTES / 1024 / (192 / 8)

        secs = round(total_secs % 60)
        mins = total_secs // 60
        hours = mins // 60

        duration = "{:.0f}:{:.0f}:{:.0f}".format(hours, mins, secs)

        try:
            thumbnail = e["media_thumbnail"][0]["url"]
        except:
            thumbnail = ""

        if not os.path.isdir("site/content/episode"):
            os.makedirs("site/content/episode")

        with open(postfile, "w") as EPISODE:
            print(ENTRY.format(thumbnail=thumbnail,
                               published=e.get("published", ""),
                               title=e.get("title", ""),
                               author=e.get("author", ""),
                               summary=e.get("summary", ""),
                               total_bytes=int(CURRENT_BYTES),
                               duration=duration,
                               podcast="episode/" + os.path.split(target_filename)[1]),
                  file=EPISODE)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        exit("Incorrect number of arguments" + __doc__)
    main(sys.argv[3], episodes_folder=sys.argv[1], baseurl=sys.argv[2])
