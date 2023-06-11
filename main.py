import json
import moviepy as mp

from time import sleep
from random import randint
from modules.utility import *
from modules.tiktok_uploader.upload import upload_video


def main():
    errored_videos = 0
    uploaded_videos = 0
    completed_videos = 0
    auth = json.load(open("./content/config.json", "r"))["auth"]
    video_list = json.load(open("./content/config.json", "r"))["video_list"]
    description = json.load(open("./content/config.json", "r"))["description"]
    total_videos = len(video_list)

    for url in video_list:
        print(f"Downloading {completed_videos + 1}/{total_videos - errored_videos}")
        dwnload = download(url)

        if dwnload["status"] == "Error":
            print(f"Error: {dwnload['message']}\n")
            errored_videos += 1
            continue
        
        print(f"Downloaded '{dwnload['message']}'\n")
        completed_videos += 1

        print(f"Uploading {uploaded_videos + 1}/{total_videos - errored_videos}\n")
        clips = create_sub_clips(mp.VideoFileClip(f"./videos/video.mp4"))

        for clip in clips:
            fails = 0
            clip_num = clips.index(clip) + 1
            args = [
                f"./videos/{clip_num}.mp4",
                f"{description['text']} | {description['tags']}",
                auth["username"],
                auth["password"],
                "./content/cookies.txt"
            ]

            edit_video(clip, clip_num)
            failed = upload_video(args[0], description=args[1], username=args[2], password=args[3], cookies=args[4])

            fails = 1
            while len(failed) > 0:
                time_to_wait = "1-1.5 hours" if fails >= 5 else "1-2 minutes"

                print(f"Failed to upload {fails} times. Retrying in {time_to_wait}.\n")

                if fails >= 5:
                    sleep(randint(3600, 5400)) # 1-1.5 hours
                else:
                    sleep(randint(60, 120)) # 1-2 minutes

                failed = upload_video(args[0], description=args[1], username=args[2], password=args[3], cookies=args[4])
                fails += 1
                
            write_to_uploaded(url, clip_num)

        uploaded_videos += 1
        
        print(f"Uploaded ({uploaded_videos}/{total_videos - errored_videos})'{dwnload['message']}'\nSleeping for 24 hours...\n")
        sleep(86400) # 24 hours


if __name__ == "__main__":
    main()
