# Watchseries-Downloader

This command Line tool will help download Series from http://thewatchseries.to/

#features
  - Download all the episode in a series with ease.
  - Resume is also enables by default.
  - Cross platform windows and Linux.
  - Add new series you want to download using `-new` parameter.
  - Can download single episode as well.
  - Can limit download speed using `-l`.
  - Can download from reverse and forward.
  - Can use just.py to download from justanimedubbed.tv it is in beta version .

#Dependencies
  - Python 2.7.X
  - lxml python module
  - requests python module
  - wget inbuilt for windows but Linux users must install.

# Steps for running
###Step 1:
Run command `git clone https://github.com/manojprithvee/Watchseries-Downloader.git`

###Step 2:
Add all the episodes u want to keep track as in test.json use examples in the test.json example.
 - The first parameter is name of the series as in thewatchseries.to url if url is http://thewatchseries.to/serie/castle then `castle` is the first parameter.
 - Second is starting season number.
 - Third is starting episodes number.
 - Fourth is final season number u want to download.
 - Fifth is final episode number u want to download.

###Step 3:
Use can also add using -new command line parameter.
eg:
`python watchseries_downloader.py -new`
 - You can also use this to download single episode.

###Step 4:
Run `python watchseries_downloader.py`.
or
Run `python watchseries_downloader.py -l 250` to limit download speed to 250kbps.
