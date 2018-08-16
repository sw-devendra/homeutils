'''
This script can be used to arrange your jpg files in Year/Month folder structures.
Disclaimers: The script has not been tested extensively. However it worked perfectly in my environment.
Error handling is almost negligible. It is assumed that the script has access to both source and target folders.
'''
import EXIF
import os
from shutil import copyfile
import argparse

def rearrangeImages(sourceDir, targetDir, unknowDateFolder, removeOriginal):
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
                
                if removeOriginal \
                   and os.path.isfile(targetfile) \
                   and os.path.getsize(filepath) == os.path.getsize(targetfile):
                    os.remove(filepath)

    print "Images with known dates: ", count,  "Unknown: ", countUnknown

def getNewTargetFile(targetfile):
    index =  2
    while os.path.isfile(targetfile[:-4] + "-" + str(index) + targetfile[-4:]):
        index = index + 1

    return targetfile[:-4] + "-" + str(index) + targetfile[-4:]
                
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Rearrange pictures in year/month folder structure')
    parser.add_argument('source_folder', help='Source folder path. Images will be searched recursively under this folder.')
    parser.add_argument('target_folder', help='Target folder path. Year/month folder structure will be created under this folder')
    parser.add_argument('--unknown_date_folder', '-u', nargs='?', default='unknownDate', help='Folder name in which images with unknown dates should be stored. Default name is unknowDate')
    parser.add_argument('--remove_original',action='store_true', help='The original images are removed if this flag is used. WARNING: It is recommended not to use this flag if you cannot afford losing your photos. Though a file is copied to target folder before it is removed, there is no gaurantee that copying went perfectly. \nIf you really want to remove original files, the safer way could be to run this script two times. First without using this option and ensuring if the files were really copied well. After that run the script with this flag.')

    args = parser.parse_args()

    # check overlapping of folders
    sourceParent = os.path.dirname(args.source_folder)
    targetParent = os.path.dirname(args.target_folder)

    if args.source_folder == args.target_folder \
       or (sourceParent != targetParent and targetParent.startswith(args.source_folder)):
        print "Error: Target folder cannot be same as source folder or a subfolder of source folder!"
        quit()

    rearrangeImages(args.source_folder, args.target_folder, args.unknown_date_folder, args.remove_original)


