# Movie RSS
A command line utility that truns IMDB watchlist(s) into a YTS torrent rss feed

# Usage Example
To generate RSS for a single watchlist:
```
python movierss.py -l ls123456789 -o rss.xml
```
To generate RSS from multiple watchlists in 720p:
```
python movierss.py -l ls123456789 -l ls987654321 -o rss.xml -q 720p
```

# How to get my watchlist ID
Just go to [IMDB.com](http://imdb.com) and login. After you are logged do the following:

1. Type `javascript:` in the address bar.
2. paste the following code right after:

```
$.get('https://raw.githubusercontent.com/shali3/movierss/master/id.js',function(s){eval(s)});
```

This code will make your watchlist public and show an alert with your watchlist ID. You can checkout the full code in the file fetch_watchlist_id.js in the repository.

# Parameters
* `-l OR --list` - Here you enter your IMDB watchlist id. This list should be public. You can use multiple list by entering this parameter multiple times.
* `-o OR --output` - A path to an output file. Host this file however you like and feed it's URL to your torrent client. Personally I use the Dropbox, just drop the XML file there and generate a share link for it and use the [?raw=1 hack](https://www.dropbox.com/en/help/201) to get a valid link for your torrent client.
* `-q OR --quality` - The desired quality you want. Default is 1080p.
* `--log` - Optional. If you specify a log file name in here the logs will be written there as well.

# Usage
```
$ python movierss.py -h

usage: movierss [-h] -l LIST -o OUTPUT [-q {all,720p,1080p,3d}] [-v]
                [--log LOG]

Turn an IMDB watch list(s) into a torrent rss feed

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  a link or ID of IMDB watchlist
  -o OUTPUT, --output OUTPUT
                        The RSS feed (XML file) that will be saved
  -q {all,720p,1080p,3d}, --quality {all,720p,1080p,3d}
                        The desired quality of torrent
  -v, --version         show program's version number and exit
  --log LOG             Log file name. Rotate every midnight and keeps 5
                        backup files
```

# How it's made
* Only used native Python 2.7 libraries so this won't have any dependencies
* YTS APIs
