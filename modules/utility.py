import os
import pytube
import moviepy.editor as mp
import moviepy.video.fx.all as vfx


def download(url: str) -> dict[str, str]:
    try:
        video = pytube.YouTube(url)
        video = video.streams.get_highest_resolution()

        video.download("./videos", filename="video.mp4")

        return {
            "status": "Success",
            "message": video.title
        }
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
    

def create_sub_clips(video: mp.VideoFileClip) -> list[mp.VideoClip]:
    ## THIS IS VIDEO SPECIFIC, CHANGE IF NEEDED ##

    end_snip = 25

    ## FOR DHAR MANN VIDEOS ##

    duration = video.duration - end_snip

    if duration <= 180:
        return [video]
    
    clip_count = int(duration / 120)
    clips = []

    for i in range(clip_count):
        clips.append(video.subclip(i * 120, (i + 1) * 120))

    if (clips[-1].duration < 30):
        clips[-1] = video.subclip((clip_count - 1) * 120, duration)

    return clips


def edit_video(video: mp.VideoClip or mp.VideoFileClip, part: int) -> mp.VideoClip:
    black = (
        mp.ImageClip("./images/black.png")
        .set_duration(video.duration)
    )
    text = (
        mp.TextClip(f"Part {part}", fontsize=125, color="white", font="Arial", stroke_color="black", stroke_width=2)
        .set_position(("center", 400))
        .set_duration(video.duration)
    )
    video = vfx.resize(video, width=1080, height=608)
    video = mp.CompositeVideoClip([black, text, video.set_position("center")])
    video = video.write_videofile(f"./videos/{part}.mp4", codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
    
    return video


def write_to_uploaded(url: str, part: int) -> None:
    with open("./content/uploaded.txt", "a") as f:
        f.write(f"{url} {part}\n")
