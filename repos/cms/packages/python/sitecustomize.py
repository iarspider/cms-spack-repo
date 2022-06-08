from os import environ
if 'PYTHON3PATH' in environ:
   import os,site
   for p in environ['PYTHON3PATH'].split(os.pathsep):
       site.addsitedir(p)
