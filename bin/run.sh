#!/bin/bash -eu

echo "Baseurl: $1"
echo "Processing URL: $2..."

python3 "$(dirname $0)"/parse_feed.py "/result/episode" "$1" "$2"

echo "Building site..."

(cd site && hugo)

echo "Moving site..."

cp -r site/public/* /result/

echo "Done"
