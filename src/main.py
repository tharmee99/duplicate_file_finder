# from os import listdir, getcwd
# from os.path import isfile, join

import os
import sys
import hashlib
import json

class DuplicateFileFinder():

    def __init__(self,dirName):
        self.dirName = dirName

        self.fileList = []
        self.uniqueFiles = []
        self.duplicateFiles = {}
        self.totalDuplicateFiles = 0

        self.finalDuplicateFiles = {}

        self.exportDir = os.path.join( os.getcwd(), 'export' )

    def getMd5Hash(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def getListOfFiles(self, directoryName = None):

        if directoryName is None:
            directoryName = self.dirName

        dirList = os.listdir(directoryName)

        for f in dirList:
            full_path = os.path.join(directoryName, f)

            if os.path.isdir(full_path):
                self.getListOfFiles(directoryName = full_path)
            else:
                self.fileList.append(full_path)

    def compareFileSize(self):

        for f in self.fileList:
            fileSize = os.path.getsize(f)
            fileGood = True
            compareFile = None

            for g in self.uniqueFiles:
                if (f == g[0]):
                    continue
                elif (fileSize != g[1]):
                    continue
                else:
                    fileGood = False
                    compareFile = g
                    break

            if fileGood:
                self.uniqueFiles.append((f,fileSize))
            else:
                if compareFile[0] in self.duplicateFiles:
                    self.duplicateFiles[compareFile[0]].append((f,fileSize))
                    # self.totalDuplicateFiles += 1
                else:
                    self.duplicateFiles[compareFile[0]] = [compareFile , (f,fileSize)]
                    # self.totalDuplicateFiles += 2

    def compareFileHash(self):

        for f in self.duplicateFiles:
            uniqueHashList = []

            for g in self.duplicateFiles[f]:

                fileHash = self.getMd5Hash(g[0])
                fileGood = True
                compareFile = None

                for h in uniqueHashList:
                    if (g[0] == h[0]):
                        continue
                    elif (fileHash != h[1]):
                        continue
                    else:
                        fileGood = False
                        compareFile = h
                        break
                
                if fileGood:
                    uniqueHashList.append((g[0], fileHash))
                else:
                    if compareFile[0] in self.finalDuplicateFiles:
                        self.finalDuplicateFiles[compareFile[0]].append((g[0],fileHash))
                        self.totalDuplicateFiles += 1
                    else:
                        self.finalDuplicateFiles[compareFile[0]] = [compareFile , (g[0],fileHash)]
                        self.totalDuplicateFiles += 2

    def exportDuplicateFileList(self, exportFileName):
        
        if not os.path.exists(self.exportDir):
                os.makedirs(self.exportDir)

        exportFile = os.path.join(self.exportDir, exportFileName)

        with open(exportFile, 'w+') as fp:
            json.dump(self.finalDuplicateFiles, fp)

if __name__ == '__main__':
    
    dirName = ""
    fileName = "out.json"
    state = True

    if(len(sys.argv) == 1):
        print("No directory Specified.")
        state = False
    elif(len(sys.argv) == 2):
        dirName = sys.argv[1]
    elif(len(sys.argv) == 3):
        dirName = sys.argv[1]
        fileName = sys.argv[2]

    if state:
        duplicateFilefinder = DuplicateFileFinder(dirName)
        duplicateFilefinder.getListOfFiles()
        duplicateFilefinder.compareFileSize()

        duplicateFilefinder.compareFileHash()
        duplicateFilefinder.exportDuplicateFileList(fileName)
        print('number of duplicates: {}'.format(duplicateFilefinder.totalDuplicateFiles))
        print(duplicateFilefinder.finalDuplicateFiles)

