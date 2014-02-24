from distutils.core import setup
import py2app

NAME = 'Coinbase Menubar'
SCRIPT = 'menubar.py'
VERSION = '0.1'
ID = 'coinbase_menubar'

DATA_FILES = [
    ('images', ['images/bitcoin.png', ]),
]

plist = dict(
     CFBundleName                = NAME,
     CFBundleShortVersionString  = ' '.join([NAME, VERSION]),
     CFBundleGetInfoString       = NAME,
     CFBundleExecutable          = NAME,
     CFBundleIdentifier          = 'com.yourdn.%s' % ID,
     LSUIElement                 = '1', #makes it not appear in cmd-tab task list etc.
)


app_data = dict(script=SCRIPT, plist=plist)

setup(
   app = [app_data],
   data_files = DATA_FILES,
   options = {
       'py2app':{
           'iconfile':'images/bitcoin.icns',
           'resources':[
               ],
           'excludes':[
               ]
           }
       }
)