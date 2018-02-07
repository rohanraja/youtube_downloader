import youtube_dl
import os

def isMusic(url):
    ydl_options = {
    }

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
        print(info["categories"])
        if "Music" in info["categories"]:
            return True

    return False

hdd = "/Volumes/Fireice/Users/rohanraja/Downloads/youdl"
# hdd = "/Volumes/Seagate Backup Plus Drive"
folder = "youMusicTmp"

def moveMusicFile(fileName):
    youId = fileName.split("-")[-1].split(".")[0]
    youRL = "https://www.youtube.com/watch?v=%s" % youId
    if isMusic(youRL):
        cmd = "mv \"%s\" \"%s/%s\"" % (fileName, hdd, folder)
        print("RUNNING CMD: %s" % cmd)
        os.system(cmd)


if __name__ == "__main__":
    moveMusicFile("/Volumes/Fireice/Users/rohanraja/Downloads/youdl/youvideos/Coldplay Official_Coldplay - Every Teardrop Is a Waterfall-fyMhvkC3A84.mp4")
