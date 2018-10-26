import json
import os
import re
f=open('./temp/VideoDatabase',"r")
VideoDatabase=json.loads(f.readlines()[0])
path = './video/'
videoIDs = os.listdir(path)

for videoID in videoIDs:
    if not videoID.find('mp4') == -1:
        videoname = VideoDatabase[videoID.replace('.mp4','')]['videotitle']
        print(videoname)
        os.rename(os.path.join(path,videoID),os.path.join(path,videoname+".mp4"))
