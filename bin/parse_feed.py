#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Usage: parse_feed.py <work-folder> <episodes_folder> <base-url> <youtube-rss-url>
'''
import sys
import shutil
import os
from collections import defaultdict
import feedparser as fp
import youtube_dl
from templates import HUGO_CONFIG, ENTRY


def main(url, episodes_folder, baseurl, work_folder, skip_download=False):
    r = defaultdict(str)

    feed = fp.parse(url)

    if feed.bozo:
        print(f"RSS feed URL {url} returns invalid XML")
        raise ValueError(feed.bozo_exception)

    f = feed["feed"]

    # Write main config
    actual_config = HUGO_CONFIG.format(baseurl=baseurl,
                                       title=f.get("title", ""),
                                       author=f.get("author", ""),
                                       yturl=f.get("link", ""))

    with open(os.path.join(work_folder, "site/config.toml"), "wb") as CONFIG:
        CONFIG.write(actual_config.encode('utf-8'))

    # shared options for youtube-dl
    #--extract-audio --audio-format mp3 --audio-quality 192k
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [],
        'skip_download': skip_download,
        'forcejson': skip_download,
    }

    if not os.path.isdir(episodes_folder):
        os.makedirs(episodes_folder)

    # Write individual entries
    for e in feed.entries:
        postfile = os.path.join(work_folder,
                                    "site/content/episode/{id}.md".format(id=e["yt_videoid"]))
        if not skip_download:
            target_filename = os.path.join(episodes_folder,
                                        "{}.mp3".format(e["yt_videoid"]))
           
            if os.path.isfile(target_filename):
                print("Already downloaded: {}".format(e.get("title", e["yt_videoid"])))
                
            else:
                global CURRENT_FILE
                CURRENT_FILE = None

                def hook(d):
                    global CURRENT_FILE
                    if d['status'] == 'finished':
                        # Called after youtube download, not after re-encode, hence the filename change
                        CURRENT_FILE = os.path.splitext(d['filename'])[0] + ".mp3"

                ydl_opts['progress_hooks'] = [hook]

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # List of urls
                    ydl.download([e["link"]])

                print("Moving '{}' to '{}'".format(CURRENT_FILE, target_filename))
                shutil.move(CURRENT_FILE, target_filename)

            target_size = os.stat(target_filename).st_size
            # Duration = size / bitrate (which is kbits per second)
            # this will not be accurate to the second
            _total_secs = int(target_size / 1024 / (192 / 8))
            _total_mins = int(_total_secs // 60)

            secs = round(_total_secs % 60)
            mins = round(_total_mins % 60)
            hours = round(_total_mins // 60)

            duration = "{:02d}:{:02d}:{:02d}".format(int(hours), int(mins), int(secs))

            file_link = f"episode/{os.path.split(target_filename)[1]}"    
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                json = ydl.extract_info(e["link"])
                for forma in json.get("formats"):
                    if forma.get("ext") == "m4a":
                        duration = json.get("duration") / 60
                        target_size = forma.get("filesize")
                        file_link = forma.get("url")
                        break

        print("Generating post:", postfile)
        print("RSS URL for post: ", file_link)

        try:
            thumbnail = e["media_thumbnail"][0]["url"]
        except:
            thumbnail = ""

        episode_dir = os.path.join(work_folder, "site/content/episode")
        if not os.path.isdir(episode_dir):
            os.makedirs(episode_dir)

        with open(postfile, "w") as EPISODE:
            print(ENTRY.format(thumbnail=thumbnail,
                               published=e.get("published", ""),
                               title=e.get("title", ""),
                               author=e.get("author", ""),
                               summary=e.get("summary", ""),
                               total_bytes=int(target_size),
                               duration=duration,
                               podcast=file_link),
                               file=EPISODE)

if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        exit("Incorrect number of arguments" + __doc__)
    print(sys.argv[1:])
    main(sys.argv[4], episodes_folder=sys.argv[2], baseurl=sys.argv[3], work_folder=sys.argv[1], skip_download=bool(sys.argv[5]))
