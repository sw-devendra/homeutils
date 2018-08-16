# Rearrangephotos Utility
Have you been taking backup of your photos locally for years which has resulted in GBs of unorganized photos?
This script can be used to rearrange your local photos (only JPGs) in simple year/month folder struture.

The script searches the JPG files recursively in given source directory, and copies them to a new year/month folder structure in given target directory.

## Requirements
* [Python 2.7](https://www.python.org/downloads/release/python-2715/)
  * The script may work with Python 3 too, but I have not tested it.
* [exifread](https://pypi.org/project/ExifRead)
```
pip install exifread
```

## usage
```
python rearrangephotos.py [-h] [--unknown_date_folder [UNKNOWN_DATE_FOLDER]]
                          [--remove_original]
                          source_folder target_folder

Rearrange pictures in year/month folder structure

positional arguments:
  source_folder         Source folder path. Images will be searched
                        recursively under this folder.
  target_folder         Target folder path. Year/month folder structure will
                        be created under this folder

optional arguments:
  -h, --help            show this help message and exit
  --unknown_date_folder [UNKNOWN_DATE_FOLDER], -u [UNKNOWN_DATE_FOLDER]
                        Folder name in which images with unknown dates should
                        be stored. Default name is unknowDate
  --remove_original     The original images are removed if this flag is used.
                        WARNING: It is recommended not to use this flag if you
                        cannot afford losing your photos. Though a file is
                        copied to target folder before it is removed, there is
                        no gaurantee that copying went perfectly. If you
                        really want to remove original files, the safer way
                        could be to run this script two times. First without
                        using this option and ensuring if the files were
                        really copied well. After that run the script with
                        this flag.
```
* Tested on following OSs
  * Ubuntu 16.04
  * Windows 7, 32 bit

## Example

```
python rearrangephotos.py "/media/devendra/my-hard-disk" /home/devendra/photos-datewise
```

## Disclaimer
* The script has not be tested significantly. It seems to work well on Ubuntu and windows for basic usecase but still please use it at your own risk.
* Though I may not have time to do major changes but please feel free to report minor issues
* There is very less error handling. So you may see errors in unusual scenarios. At least please ensure that 
  * Both source and target folders are accessible.
  * Source and target directories do not overlap with each other
  * Target folder has enough space left
  
## QnA
* __Q. What will happen to original photos?__
  * __A.__ By default, the orginal photos are just read, not deleted. However you can delete original photos using --remove_original command line option

__Disclaimer: Do it only if you understrand the script very well. I have used this option after I had already taken one copy of the photos. I have not analyzed all the scenarios when this option may behave adversely__

* __Q. What if there are duplicate photos in the hard disc?__
  * __A.__ A photo is considered exactly same as the target photo when the name of file, size of the file and date of photo taken match. In that case, the photo will be copied only once. It means that if your source folder struture has same photo at two locations, only one copy will go to the target folder and second (and subsequent) copy will be ignored.
* __Q. How about other types of picture files like PNGs?__
  * __A.__ Not supported. Personally, I noted that most of camera devices store photos in JPG format, so this should not be an issue for most of the people.
* __Q. How about videos?__
  * __A.__ Not supported. I am not sure if I can extract date of shooting video from the video file. I will check that later.

  
