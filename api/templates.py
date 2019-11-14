#!/usr/bin/env python3
# -*- coding: utf-8 -*-

HUGO_CONFIG = \
u'''
baseurl = "{baseurl}"
languageCode = "en-us"
title = """{title}"""
metadataformat = "toml"
canonifyurls = true
# Define the number of posts per page
paginate = 15
footnotereturnlinkcontents = "↩"
theme = "hemingway"
copyright = """All content original copyright of {author}"""

[permalinks]
  post = "/:filename/"

[author]
  name = """{author}"""
  email = "dummy@dummy.dummy"

[params]
  author = """{author}"""
  # Format dates with Go's time formatting
  date_format = "2006-01-02"

[[params.social]]
  url = "{yturl}"
  fa_icon = "fa-youtube"

[[params.social]]
  url = "/index.xml"
  fa_icon = "fa-rss"

[blackfriday]
  smartypants	= true
  fractions = true
  smartDashes = true
  latexDashes = true
  plainIDAnchors = true

'''

ENTRY = \
u'''
+++
banner = "{thumbnail}"
categories = []
date = "{published}"
description = """{summary}"""
draft = false
images = []
menu = ""
tags = []
title = """{title}"""
author = "{author}"
podcast = "{podcast}"
podcast_bytes = "{total_bytes}"
podcast_duration = "{duration}"
+++

{summary}
'''
