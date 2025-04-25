# rss-reader
Python console script, accepts a url to a rss feed and prints out formatted information from that feed.
Option to print in json formatting instead, code can be easily altered to save the json string to a file instead.

Usable arguments:
source - mandatory for the script to work, has to be valid url to a rss feed
--json - optional, if used the script returns a formatted json string instead
--limit - optional, needs to be an integer, limits the number of <item>s parsed, if provided the script only returns the latest (number provided) items from the feed

If limit isn't provided or the provided limit is larger than amount of items in the feed, the script returns all items from the feed.
