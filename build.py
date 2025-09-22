#!/usr/bin/python

import os,re,sys,time
if (sys.version_info < (3, 0)):
    raise Exception("Python 3 required")
import urllib.request
import shutil
import tempfile
import zipfile

ORIGINAL_FILE_NAME = "eloquence_original.nvda-addon"
FILE_NAME = "eloquence.nvda-addon"

def updateZip(zipname, filename, filedata):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename            
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    #print(f"os.rename({tmpname}, {zipname})")
    # For some really weird reason the following command not always works in certain conditions
    # So replacing it with an external call
    #os.rename(tmpname, zipname)
    os.system(f"rename {tmpname} {zipname}")
    time.sleep(1)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(filedata, filename)


def addDirectory(zipname, sourceDir, destRoot):
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(sourceDir):
            for name in files:
                src_path = os.path.join(root, name)
                rel_path = os.path.relpath(src_path, sourceDir)
                archive_name = os.path.join(destRoot, rel_path).replace(os.sep, "/")
                zf.write(src_path, archive_name)


if not os.path.exists(ORIGINAL_FILE_NAME):
    print("Downloading...")
    with urllib.request.urlopen('https://github.com/pumper42nickel/eloquence_threshold/releases/download/v0.20210417.01/eloquence.nvda-addon') as response:
        with open(ORIGINAL_FILE_NAME, "wb") as f:
            shutil.copyfileobj(response, f)
print("Patching...")
shutil.copyfile(ORIGINAL_FILE_NAME, FILE_NAME)
updateZip(FILE_NAME, "synthDrivers/eloquence.py", "eloquence.py")
updateZip(FILE_NAME, "synthDrivers/_eloquence.py", "_eloquence.py")
updateZip(FILE_NAME, "synthDrivers/phoneme_catalog.py", "phoneme_catalog.py")
updateZip(FILE_NAME, "synthDrivers/voice_catalog.py", "voice_catalog.py")
updateZip(FILE_NAME, "synthDrivers/language_profiles.py", "language_profiles.py")
updateZip(FILE_NAME, "manifest.ini", "manifest.ini")
if os.path.isdir("eloquence_x64"):
    print("Embedding 64-bit Eloquence payload...")
    addDirectory(FILE_NAME, "eloquence_x64", os.path.join("synthDrivers", "eloquence", "x64"))
if os.path.isdir("eloquence_data"):
    addDirectory(FILE_NAME, "eloquence_data", os.path.join("synthDrivers", "eloquence_data"))
print(f"Created {FILE_NAME}")
