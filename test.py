import os
from classes import Paths
sets_to_create = {'Weekly Vocab': True, 'Verbs': False, 'Custom': False}

paths = Paths('Week 1', sets_to_create)

##

for obj in os.scandir(paths.audio_folder):
    filename, ext = os.path.splitext(obj.name)
    if '.ogg' == ext:
        drchangecmd = 'CD '+paths.audio_folder
        convcmd = 'ffmpeg -i '+filename+'.ogg'+' '+filename+'.mp3'
        os.system(drchangecmd+' && '+convcmd)
        
        startloc = os.path.normpath(paths.audio_folder+'/'+filename+'.mp3')
        endloc = os.path.normpath(paths.converted_folder+'/'+filename+'.mp3')
        os.rename(startloc, endloc)



