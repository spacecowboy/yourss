# yourss
Convert any youtube rss feed into a podcast feed with mp3 instead of youtube videos

## Example: Local setup
1. Clone this repo and setup enviornment
```
git clone https://github.com/spacecowboy/yourss
virtualenv env -p python3 && source env/bin/activate
pip install -r requirements.txt
```
2. If you need to generate a site, go through the hugo quickstart guide https://gohugo.io/getting-started/quick-start/
    - Note the location where you put the new site. This will be --out parmeter (e.g. /var/www/quickstart/public)
3. If you need a hosting solution for your website to get a baseurl, Hugo has some documentation on this https://gohugo.io/hosting-and-deployment/hosting-on-github/
4. Run the command to download the mp3 files and generate the HTML files
```
./bin/yourss --baseurl="<from step 5>" --rss="https://www.youtube.com/feeds/videos.xml?channel_id=UCyoQK-mZXr2ws4C0nXGCH1w" --out="<from step 2>"
```
6. Everything has been moved to the out directory, so you just have to deploy those changes to whatever your hosting solution is. The RSS feed for the channel will be hosted at `baseurl/index.xml`

## Example usage:

```
docker run --rm --name triforce -v /path/to/site:/result yourss "http://triforce.cowboyprogrammer.org" "https://www.youtube.com/feeds/videos.xml?channel_id=UCgXiTWrFg05fTPfw1YLb5Ug"
```

## How to get channel IDs for channel usernames
Some channels have usernames instead of IDs. You can find the channel id by subscribing to that channel, going to https://www.youtube.com/subscription_manager, exporting the feed and finding the channel inside the feed.