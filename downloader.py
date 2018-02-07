__author__ = 'rohanraja'


import youtube_dl
ydl_opts = {'quite':True}

def onProgress(val):
    print(val)

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.add_progress_hook(onProgress)
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])