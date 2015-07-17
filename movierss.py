__author__ = 'ShaLi'
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
import re
import urllib2
from collections import namedtuple

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

list_id_re = re.compile(ur'ls\d+')
movie_id_re = re.compile(ur'<link>.*?(tt\d+).*?</link>')
movie_name_re = re.compile(ur'<title>(.*?)</title>')
rss_item_re = re.compile(ur'<item>.*?</item>')
rss_header = '<?xml version="1.0" encoding="UTF-8"?>' \
             '<rss version="2.0">' \
             '<channel>' \
             '<title>YTS RSS</title>' \
             '<description>Most popular Torrents in the smallest file size RSS Feed</description>' \
             '<language>en-us</language>';
rss_footer = '</channel></rss>'
Movie = namedtuple('Movie', ['id', 'name'])


def imdb_list_id(string):
    value = list_id_re.findall(string)
    if len(value) == 0:
        msg = "%s is not an IMDB list" % string
        raise argparse.ArgumentTypeError(msg)
    return value[0]


def get_watchlist(list_id):
    logging.info('Getting list %s', l)
    res = urllib2.urlopen('http://rss.imdb.com/list/%s/' % list_id)
    rss_content = res.read()
    movie_ids = movie_id_re.findall(rss_content)
    names = movie_name_re.findall(rss_content)
    list_name = names.pop(0)  # remove the list name
    if len(names) == len(movie_ids):
        logging.info('Found %d movies in list %s [%s]', len(names), list_id, list_name)
    else:
        raise ValueError('Ids and names mismatch')

    movie_objects = []
    for id in movie_ids:
        movie_objects.append(Movie(id=id, name=names[len(movie_objects)]))

    return movie_objects


def get_movie_rss_items(movie, quality):
    logging.info('Getting YTS RSS for movie - %s', movie.name)
    res = urllib2.urlopen('https://yts.to/rss/%s/%s/all/0' % (movie.id, quality))
    rss_content = res.read()
    items = rss_item_re.findall(rss_content)
    logging.info('Found %d torrents for the movie %s', len(items), movie.name)
    return items


parser = argparse.ArgumentParser(prog='movierss', description='Turn an IMDB watch list(s) into a torrent rss feed')
parser.add_argument('-l', '--list', type=imdb_list_id, action='append',
                    required=True, help='a link or ID of IMDB watchlist')
parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                    required=True, help='The RSS feed (XML file) that will be saved')
parser.add_argument('-q', '--quality', choices=['all', '720p', '1080p', '3d'], default='1080p',
                    help='The desired quality of torrent')
parser.add_argument('-v', '--version', action='version', version='1.0.1')
parser.add_argument('--log', help='Log file name. Rotate every midnight and keeps 5 backup files')

args = parser.parse_args()

if args.log:
    logHandler = TimedRotatingFileHandler(args.log, when="midnight", backupCount=5)
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logHandler.setFormatter(logFormatter)
    logging.root.addHandler(logHandler)

movies = []
for l in args.list:
    movies.extend(get_watchlist(l))

movies = set(movies)
rss_items = []
for movie in movies:
    rss_items.extend(get_movie_rss_items(movie, args.quality))

args.output.write(rss_header + ''.join(rss_items) + rss_footer)
