import os

ending = '.ogg'
root = 'C:/Users/Mykhaylo Severinov/Desktop/Classes/German/IPA'

for file in os.scandir(root):
    filename, ext = os.path.splitext(file.name)
    if ending == ext:
        convcmd = 'ffmpeg -i '+filename+ending+' '+filename+'.mp3'
        os.system(convcmd)
        
        startloc = os.path.normpath(root+'/'+filename+ending)
        endloc = os.path.normpath(root + '/Converted/'+filename+ending)
        if not os.path.exists(endloc):
              os.rename(startloc, endloc)
        else:
            print(filename, 'has already been converted.')
         
