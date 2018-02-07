import glob
import sys
from processUrl import checkMusicFile





path = sys.argv[1]
files = glob.glob("%s/*"%path)

for i in range(1, len(sys.argv)):
    f = sys.argv[i].replace("\\", "")
    checkMusicFile.apply_async(args=[f], queue="checkMusic")
    print(f)

# for f in files:
#     checkMusicFile.apply_async(args=[f], queue="checkMusic")
#     print f

