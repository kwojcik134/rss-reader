from argparse import ArgumentParser
from typing import List, Optional
import requests
import xml.etree.ElementTree as et
import json as js
import sys

class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.
    """

    root = et.fromstring(xml)

    # Getting the channel items
    channel = root.find('channel')
    channel_dict = {}
    channel_dict['title'] = channel.find('title').text
    channel_dict['link'] = channel.find('link').text
    if channel.find('lastBuildDate') is not None:
        channel_dict['lastBuildDate'] = channel.find('lastBuildDate').text
    if channel.find('language') is not None:
        channel_dict['language'] = channel.find('language').text
    if channel.find('pubDate') is not None:
        channel_dict['pubDate'] = channel.find('pubDate').text
    if channel.find('category') is not None:
        channel_dict['category'] = [category.text for category in channel.findall('category')]
    if channel.find('managingEditor') is not None:
        channel_dict['managingEditor'] = channel.find('managingEditor').text
    if channel.find('description') is not None:
        channel_dict['description'] = channel.find('description').text



    # Getting items table
    items = [item for item in channel.findall('item')]

    if not limit or limit > len(items):
        limit = len(items)

    items_table = []
    for i in range(limit):
        item_dict = {}
        if items[i].find('title') is not None:
            item_dict['title'] = items[i].find('title').text
        if items[i].find('author') is not None:
            item_dict['author'] = items[i].find('author').text
        if items[i].find('pubDate') is not None:
            item_dict['pubDate'] = items[i].find('pubDate').text
        if items[i].find('link') is not None:
            item_dict['link'] = items[i].find('link').text
        if items[i].find('category') is not None:
            item_dict['category'] = [category.text for category in items[i].findall('category')]
        if items[i].find('description') is not None:
            item_dict['description'] = items[i].find('description').text
        items_table.append(item_dict)
    channel_dict['items'] = items_table

    strings = []

    #JSON version
    if json:
        json_string = js.dumps(channel_dict, indent = 2).encode('utf-8').decode(sys.stdout.encoding, errors='replace')
        strings = [json_string]

    #Console print version
    elif not json:
        strings.append(f"Feed: {channel_dict['title']}")
        strings.append(f"Link: {channel_dict['link']}")
        if 'lastBuildDate' in channel_dict.keys():
            strings.append(f"Last Build Date: {channel_dict['lastBuildDate']}")
        if 'pubDate' in channel_dict.keys():
            strings.append(f"Publish Date: {channel_dict['pubDate']}")
        if 'language' in channel_dict.keys():
            strings.append(f"Language: {channel_dict['language']}")
        if 'category' in channel_dict.keys():
            strings.append(f"Categories: {', '.join(channel_dict['category'])}")
        if 'managingEditor' in channel_dict.keys():
            strings.append(f"Editor: {channel_dict['managingEditor']}")
        if 'description' in channel_dict.keys():
            strings.append(f"Description: {channel_dict['description']}")
        for item in items_table:
            strings.append('\n')
            for line in items_unpacker(item):
                strings.append(line)

    return strings

def items_unpacker(item_dict):
    """
    Returns list of strings from an item dictionary
    """
    lines = []
    if 'title' in item_dict.keys():
        lines.append(f"Title: {item_dict['title']}")
    if 'author' in item_dict.keys():
        lines.append(f"Author: {item_dict['author']}")
    if 'pubDate' in item_dict.keys():
        lines.append(f"Published: {item_dict['pubDate']}")
    if 'link' in item_dict.keys():
        lines.append(f"Link: {item_dict['link']}")
    if 'category' in item_dict.keys():
        lines.append(f"Categories: {', '.join(item_dict['category'])}")
    if 'description' in item_dict.keys():
        lines.append(f"\n{item_dict['description']}")
    return lines

def main():
    """
    CLI
    """
    parser = ArgumentParser(
        prog='rss_reader',
        description='Pure Python command-line RSS reader.',
    )
    parser.add_argument('source', help='RSS URL', type=str, nargs='?')
    parser.add_argument(
        '--json', help='Print result as JSON in stdout', action='store_true'
    )
    parser.add_argument(
        '--limit', help='Limit news topics if this parameter provided', type=int
    )
    xml = None
    args = parser.parse_args()

    if not (args.limit is None or args.limit.isinstance(int)):
        print('Limit needs to be an integer.')

    try:
        xml = requests.get(args.source).text
    except Exception as e:
        print(e)

    if xml is not None:
        try:
            print('\n'.join(rss_parser(xml, args.limit, args.json)))
            return 0
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
