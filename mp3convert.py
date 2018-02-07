import os 

def GetFileName(inFile):
    return inFile.split("/")[-1].split(".")[-2]

ffBin = "/Volumes/Fireice/Users/rraja/Downloads/Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_08.12.2016/ffmpeg"
def convertToMp3(inFile, outFolder):
    fileName = GetFileName(inFile)
    cmd = "%s -n -i \"%s\" \"%s/%s.mp3\"" % (ffBin, inFile, outFolder, fileName)
    os.system(cmd)


outFol = "/Volumes/Fireice/Users/rohanraja/Downloads/youdl/yoump3"

if __name__ == "__main__":
    convertToMp3("/Volumes/Fireice/Users/rohanraja/Downloads/youdl/youMusic/Coldplay Official_Coldplay - Every Teardrop Is a Waterfall-fyMhvkC3A84.mp4", outFol)

