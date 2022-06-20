import zipfile
import shutil

# with zipfile.ZipFile('files.zip', 'w', compression=zipfile.ZIP_DEFLATED) as my_zip:
#     my_zip.write('test.txt')
#     my_zip.write('thumbnail.png')

# with zipfile.ZipFile('files.zip', 'r') as my_zip:
#     print(my_zip.namelist())
#     my_zip.extractall('files')

shutil.make_archive('another', 'zip', 'files')
shutil.unpack_archive('another.zip', 'another')
