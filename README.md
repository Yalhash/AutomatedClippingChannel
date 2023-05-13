A bot that scrapes Twitch.tv to download and edit clips from designated channels. It uses Selenium, and the chrome web driver (but any webdriver could theoretically be used) to download the clips, and ffmpeg to compile them into a video 10 minutes long. It will not download repeated clips, and downloads the most popular out of the channels given in the channels.csv provided. It also will only download content from the game specified in the game.txt file


TODO:
- Need to create a full test suite
- Issue with download for some reason, maybe issue when collecting metadata: 
    "EXCEPT: Invalid URL '': No schema supplied. Perhaps you meant http://?"
- FFMPEG is failing to do anything...
- The subtitles look bad, and font never worked
- known\_files, used for disambiguating filenames, needs to be updated somewhere, for now it is just passed around.
