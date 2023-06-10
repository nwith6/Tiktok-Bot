# Tiktok Bot
This is a tiktok bot that automatically uploads every video that is found under in the `video_list` key `config.json`.

This bot uses a modified version of wkaisertexas's tiktok-uploader found [here](https://github.com/wkaisertexas/tiktok-uploader), functions made by me, moviepy, and pytube.

This bot will download the youtube video, crop it to a black image, split it into 2 minute parts and upload it to tiktok. The bot uses `sleep()` to avoid tiktok moderation, although it can be rate limited it does get a fair few videos out before it is rate limited. After it's rate limited it will wait 1-1.5 hours between attempts until it is finally able to post.

The bot after uploading each part of a video back to back will sleep for 24 hours before attempting to trim another video and upload the trimmed parts.

# Setting up for yourself
1. Install the requirements by running `pip install -r requirements.txt`.
2. Using the [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/cclelndahbckbenkjhflpdbgdldlbecc) extension paste your tiktok cookies (after logging into your tiktok account) inside `./content/cookies.txt/`.
3. In `./content/config.json/` fill out all the details and add youtube links in `video_list`.
4. Open `./modules/utility.py/` and on line 28 change `end_snip` to your desired value. This snips the end of the video to usually remove a youtubers outro.
5. Download [ImageMagick](https://imagemagick.org/script/download.php#windows) and navigate to your moviepy installation found in site-packages, find `config_defaults.py` and set `IMAGEMAGICK_BINARY`'s value to the location of your `ImageMagick` installation. (e.g - "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe").
6. Run the bot and have fun! :)

# Contact
If you need any help you can cantact me on discord @ nathan#2400