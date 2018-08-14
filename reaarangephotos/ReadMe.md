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

## Usage
* Edit reaarangephotos.py and update following variable according to your environment. __Will improve the script later to support command line arguments__ 
```
sourceDir = 'path_to_source_directory' # JPG files will be searched recursively in this folder
targetDir = 'path_to_target_directory' # Year/month folder structre will be created here
```
* Run script
```
python reaarangephotos.py
```
* Tested on following OSs
  * Ubuntu 16.04
  * Windows 7, 32 bit


## Disclaimer
* The script has not be tested significantly. It seems to work well on Ubuntu and windows for basic usecase but still please use it at your own risk.
* Though I may not have time to do major changes but please feel free to report minor issues
* There is almost no error handling. So you may see error messages in unusual scenarios. At least please ensure that 
  * Both source and target folders are accessible.
  * Source and target directories do not overlap with each other
  * Target folder has enough space left
  
## QnA
* __Q. What will happen to original photos?__
  * __A.__ To be safe, the orginal photos are just read, not deleted. But it is possible to delete original photos by hacking the script little bit. Actually you can set following variable to true, if you want to remove original photos:
```
removeOriginal = True
```
__Disclaimer: Do it only if you understrand the script very well. I have used this option after I had already taken one copy of the photos. I have not analyzed all the scenarios when this option may behave adversely__

* __Q. What if there are duplicate photos in the hard disc?__
  * __A.__ A photo is considered exactly same as the target photo when the name of file, size of the file and date of photo taken match. In that case, the photo will be copied only once. It means that if your source folder struture has same photo at two locations, only one copy will go to the target folder and second (and subsequent) copy will be ignored.
* __Q. How about other types of picture files like PNGs?__
  * __A.__ Not supported. Personally, I noted that most of camera devices store photos in JPG format, so this should not be an issue for most of the people.
* __Q. How about videos?__
  * __A.__ Not supported. I do not know how I can extract date of shooting video from the video file.

  
