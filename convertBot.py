import os
import subprocess
import sys
Conv_SampleRate = 44100
Conv_SampleBitDeapth = 16
Conv_SampleClipProc = 0.99
Conv_SamplePaths = ['C:\Users\Mikef\Google Drive\Audio Pool\Samples', 'C:\Users\Mikef\Desktop\Audio Pool\Sample Packs'] 

def getFiles(filePath):
    filecount = getFileCount(filePath)
    currentFile = 0;
    Prev_Scanned = []
    if os.path.exists('scanned.ini') :
        f = open('scanned.ini', 'r+')
        Prev_Scanned = f.read().splitlines()
        f.close()
        
    for dirName, subdirList, fileList in os.walk(filePath):
        for fname in fileList:
            currentFile = currentFile + 1
            currentPerc = 100 * float(currentFile)/float(filecount)
            print '\r',   
            out = "Checking File %i/%i (%i%%)" % (currentFile, filecount, currentPerc)
            #print out,
            print out
            if fname.endswith(".wav") or fname.endswith(".mp3"):
                fullPath = os.path.join(dirName, fname)
                if fullPath not in Prev_Scanned: 
                    addToScanned(fullPath)
                    #Check If we have already converted the file
                    checkFile = getNewFile(fullPath)
                    if os.path.exists(checkFile) :
                        #print "Skipping %s, Already Converted" % (fname)
                        continue
                    else : 
                        bitRate = getRate(fullPath).strip()
                        bitDepth = getBit(fullPath).strip()
                        bitType = getType(fullPath).strip()
                        if bitRate != "44100" or bitDepth != '16' or bitType != 'wav':
                            print convertFile(fullPath)   
def getNewFile(filename):
    NewFilename = ''
    if(filename.endswith(".mp3")):
         NewFilename = filename.replace('.mp3', '_conv.wav')
    if(filename.endswith(".wav")):
         NewFilename = filename.replace('.wav', '_conv.wav')
    return NewFilename
          
def getRate(file):
    return runCommand('sox --i -r "%s"' % (file))

def getBit(file):
    return runCommand('sox --i -p "%s"' % (file))

def getType(file):
    return runCommand('sox --i -t "%s"' % (file))

def convertFile(file):
    newFileName = getNewFile(file)
    print ""
    print "------------------------------------------------------------------------------------------------"
    print "Converting File: %s" % (file)
    print "New File: %s" % (newFileName)
    return runCommand('sox  -v %s "%s" -r %s -b %s "%s"' % (str(Conv_SampleClipProc), file, str(Conv_SampleRate), str(Conv_SampleBitDeapth), newFileName))
    print "------------------------------------------------------------------------------------------------"

def runCommand(Command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=startupinfo)
    return proc.stdout.read()

def getFileCount(dir):
    files = 0
    for dirName, subdirList, fileList in os.walk(dir):
        for fname in fileList:
            files = files + 1
    return files

def addToScanned(path):
    with open("scanned.ini", "a") as myfile:
        myfile.write("%s%s" % (path, '\r'))

for path in Conv_SamplePaths:
    print "Processing Path %s" % (path)
    getFiles(path)




