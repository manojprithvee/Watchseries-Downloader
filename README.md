# Watchseries-Downloader

This command Line tool will help download Series from thewatchseries.to

#features
  - Download all the episold in a series with ease.
  - Resume is also enables by default.
  - Cross platform windows and linux.
  - Add new series you want to download using `-new` parameter.
  - Can download single episold as well.
  - Can limit download speed using `-l`.
  - Can download from reverse and forward.
  - Can use just.py to download from justanimedubbed.tv it is in beta version .

#Dependencies
  - Python 2.7.X
  - lxml python module
  - requests python module
  - wget inbuilt for windows but linux users must install.

# Steps for running
###Step 1:
Run command `git clone https://github.com/manojprithvee/Watchseries-Downloader.git`

###Step 2: 
 - Add all the episolde u want to keep track as in test.json use examples in the test.json.
 - The first parameter is name of the series as in thewatchseries.to url.
 - Second is starting season number.
 - Thrid is starting episolde number.
 - Fourth is final season number u want to download.
 - Fifth is final episolde number u want to download.

###Step 3:
Use can also add using -new command line paramenter.
eg:
`python watchseries_downloader.py -new`
 - You can also use this to download single episolde.

###Step 4:
Run `python watchseries_downloader.py`.
or 
Run `python watchseries_downloader.py -l 250` to limit download speed to 250kbps.
