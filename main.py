import json
import moviepy as mp

from time import sleep
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

            edit_video(clip, clip_num)
            failed = upload_video(
                f"./videos/{clip_num}.mp4",
                description=f"{description['text']} | {description['tags']}",
                username=auth["username"],
                password=auth["password"],
                cookies="./content/cookies.txt"
            )

            fails = 1
            while len(failed) > 0:
                time_to_wait = "1 hour" if fails >= 5 else "1 minute"

                print(f"Failed to upload {fails} times. Retrying in {time_to_wait}.\n")

                if time_to_wait == "1 hour":
                    sleep(3600) # 1 hour
                else:
                    sleep(60) # 1 minute

                failed = upload_video(
                    f"./videos/{clip_num}.mp4",
                    description=f"{description['text']} | {description['tags']}",
                    username=auth["username"],
                    password=auth["password"],
                    cookies="./content/cookies.txt"
                )
                fails += 1
                
            write_to_uploaded(url, clip_num)

        uploaded_videos += 1
        
        print(f"Uploaded ({uploaded_videos}/{total_videos - errored_videos})'{dwnload['message']}'\nSleeping for 6 hours...\n")
        sleep(21600) # 6 hours


if __name__ == "__main__":
    main()
