Super simple app to copy a google photo album to a local folder.


## Setup ##

https://console.cloud.google.com/apis/credentials

* Create google cloud project
* Create desktop oauth client id
* Download credentials.json
* Setup python environment, dependencies however you wish.
* Follow next section, tuned for your needs.


## My setup ##

I sync a "Wallpapers" album on my mac to use as a screensaver.
Since this is for me, I use the defaults which are effectively

    GPHOTOSYNC_ALBUM_TITLE=Wallpapers
    GPHOTOSYNC_DEST_FOLDER=~/Pictures/gphotosync

I've set up the project in a pyenv. This is my crontab set to run hourly 
to pull down any new photos added to that album.

    0 * * * * cd /Users/jasond/src/github.com/dirkraft/gphotosync && PYENV_VERSION=gphotosync /Users/jasond/.pyenv/shims/python main.py > /tmp/gphotosync.log

https://console.cloud.google.com/apis/credentials?project=gphotosync-1637339236673