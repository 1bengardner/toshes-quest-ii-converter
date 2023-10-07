# Save Converter for Toshe's Quest II

ℹ Just looking for the standalone converter download? Get it from https://github.com/1bengardner/toshes-quest-ii-converter/releases.

## Description

Use this converter to upgrade your old saved games (.tq) to work with the latest version of Toshe's Quest II.

Adapted from [toshes-quest-ii/source/converter.py](https://github.com/1bengardner/toshes-quest-ii/blob/master/source/converter.py) to be used as a source for a standalone executable.

## Requirements

1. To build an executable from [Converter.py](Converter.py), you will need [py2exe](https://www.py2exe.org/). You may need to familiarize yourself with it. A good place to start is the [tutorial](https://www.py2exe.org/index.cgi/Tutorial).
1. For the converter to run properly after being built, you will need to download the [Toshe's Quest II game source](https://github.com/1bengardner/toshes-quest-ii/tree/master/source). This is so that when the resulting `Converter.exe` is run, it is able to unpickle the data in your character into their original types.

## Building

Use py2exe to turn the converter script into an executable, with the help of a setup script.

Be sure to include in your setup script `sys.path.insert(0, "<path-to-game-source-directory>")`.

<details>

<summary>Sample py2exe setup script...</summary>

The following script will build an executable from `Converter.py`.

Adapted from https://www.pygame.org/wiki/Pygame2exe.

```python
try:
    from distutils.core import setup
    import py2exe
    import glob, fnmatch
    import sys, os, shutil
    import operator
    sys.path.insert(0, "<path-to-game-source-directory>")
except ImportError, message:
    raise SystemExit,  "Unable to load module. %s" % message

class BuildExe:
    def __init__(self):
        #Name of starting .py
        self.script = "<path-to>/Converter.py"

        #Name of program
        self.project_name = "Save converter for Toshe's Quest II"

        #Version of program
        self.project_version = "1.0.0"

        #Auhor of program
        self.author_name = "Ben Gardner"
        self.copyright = "(c) 2023 Ben Gardner"

        #Icon file
        self.icon_file = "<path-to>/<your-icon.ico>"
        
        #DLL Excludes
        self.exclude_dll = ['w9xpopen.exe']

        #Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = None

        #Dist directory
        self.dist_dir ='dist'

    def run(self):
        if os.path.isdir(self.dist_dir): #Erase previous destination dir
            shutil.rmtree(self.dist_dir)
        
        setup(
            version = self.project_version,
            name = self.project_name,
            author = self.author_name,

            # targets to build
            console = [{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options = {'py2exe': {
                'bundle_files': 1,
                'dll_excludes': self.exclude_dll,
            }},
            zipfile = self.zipfile_name,
            dist_dir = self.dist_dir
            )
        
        if os.path.isdir('build'): #Clean up build dir
            shutil.rmtree('build')

if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run() #Run generation
    raw_input("Press any key to continue") #Pause to let user see that things ends
```

</details>

## Running

Place the resulting `Converter.exe` in the same directory as your [Toshe's Quest II.exe](https://github.com/1bengardner/toshes-quest-ii/releases). Run it and follow the instructions to convert an old file and restore compatibility with the latest version of the game.
