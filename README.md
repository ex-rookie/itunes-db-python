# itunes-db-python
Parse the Library.xml from itunes to extract Track/Album/Artist data and insert to SQLite DB

Instructions:
$ git clone https://github.com/experienced-rookie/itunes-db-python
$ cd itunes-db-python
$ python3 tracks.py
Enter file name: 

(Default is Library.xml)

"trackdb.sqlite" should be generated

Copy the Library XML file from iTunes directory to your project directory.

The new iTunes versions do not have XML file by default, so the below fix can be used to generate one:
http://osxdaily.com/2018/05/23/itunes-library-xml-file-missing-fix/
