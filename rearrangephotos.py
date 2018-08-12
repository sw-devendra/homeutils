'''
This script can be used to arrange your jpg files in Year/Month folder structures.
Change following variables according to your env:
rootdir : The directory which should be searched recursively to find jpg files
targetDir : The directory where new folder structure should be created
unknowDateFolder : Optionally change the directory name to be created when a JPG has no date tag

Disclaimers: The script has not been tested extensively. However it worked perfectly in my environment.
Error handling is almost negligible. It is assumed that the script has access to both source and target folders.
Also it is assumed that
'''
import EXIF
import os
from shutil import copyfile

rootdir = '/media/devendra/FreeAgent Drive/Hard-Disk-Recovery/New folder'
targetDir = '/home/devendra/photos-datewise'
unknowDateFolder = 'unknownDate'

def rearrangeImages(sourceDir, targetDir):
    count = 0
    countUnknown  = 0
    for subdir, dirs, files in os.walk(sourceDir):
        for file in files:
            if file[-3:].lower() == 'jpg':
                filepath = os.path.join(subdir, file)
                targetFolder = ""
                dateTaken = ""
                targetfile = ""
                doCopy = True
                with open(filepath, 'rb') as fh:
                    tags = EXIF.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                    if "EXIF DateTimeOriginal" in tags:
                        dateTaken = tags["EXIF DateTimeOriginal"]
                        print filepath, dateTaken
                        dateStr = str(dateTaken).split(' ')[0]
                        year, month = extractYearMonth(dateStr)

                        targetFolder = year + '/' + month
                        count = count + 1
                    else:
                        print filepath, "Unknown Date"
                        targetFolder = unknowDateFolder
                        countUnknown = countUnknown + 1

                    targetFolder = targetDir + '/' + targetFolder
                    if not os.path.exists(targetFolder):
                        os.makedirs(targetFolder)

                    targetfile = targetFolder + '/' + file

                    if os.path.isfile(targetfile):
                        print targetfile, "exists already"
                        with open(targetfile, 'rb') as fexistingTarget:
                            tags = EXIF.process_file(fexistingTarget, stop_tag="EXIF DateTimeOriginal")
                            dateTakenTarget = ""
                            if "EXIF DateTimeOriginal" in tags:
                                dateTakenTarget = tags["EXIF DateTimeOriginal"]
                            
                            print "Files with same name:"
                            srcSileSize = os.path.getsize(filepath)
                            trgFileSize = os.path.getsize(targetfile)
                            print filepath, dateTaken, srcSileSize, "bytes"
                            print targetfile, dateTakenTarget, trgFileSize, "bytes"

                            # ToDo: Better way to compare OriginalDateTags?
                            if (str(dateTakenTarget) == str(dateTaken)) and (trgFileSize == srcSileSize):
                                # looks like exactly same image
                                print "Copying will be avoided.."
                                doCopy = False
                            else:
                                targetfile = getNewTargetFile(targetfile)
                                print "Changed target file to ", targetfile
                if doCopy:
                    copyfile(filepath, targetfile)

    print "Images with known dates: ", count,  "Unknown: ", countUnknown

def getNewTargetFile(targetfile):
    index =  2
    while os.path.isfile(targetfile + "-" + str(index)):
        index = index + 1

    return targetfile + "-" + str(index)
                
def extractYearMonth(datestr):
    # returns year, month from string
    # supports only few formats, can be improved as needed
    parts = []
    y = ""
    if ':' in datestr:
        parts = datestr.split(':')
    elif '/' in  datestr:
        parts = datestr.split('/')

    if len(parts) != 3:
            raise Exception("Unsupported Date format", datestr)

    if len(parts[0]) == 4:
        y = parts[0]
    else:
        y = parts[2]

    return (y, parts[1])

    

rearrangeImages(rootdir, targetDir)

