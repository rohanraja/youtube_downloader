import glob
import sys
from processUrl import convertMp3





path = sys.argv[1]
files = glob.glob("%s/*"%path)

for i in range(1, len(sys.argv)):
    f = sys.argv[i].replace("\\", "")
    convertMp3.apply_async(args=[f], queue="convertmp3")
    print(f)

# for f in files:
#     checkMusicFile.apply_async(args=[f], queue="checkMusic")
#     print f

