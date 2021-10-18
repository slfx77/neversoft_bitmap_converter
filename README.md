# Requirements

- python3
- pyqt5 - can be installed with `pip install PyQt5`
- pypng - Included

# Usage Instructions

This program can be running `py main.py` in the directory it is extracted to. Then, simply select the folder containing the RLE / BMR files you wish to extract the textures from, and the folder to output the images to. Images will be output as PNGs.

# Known bugs

- The program is single threaded and will freeze while extraction is ongoing.
- The Dreamcast version of Spider-Man uses a different format for RLE files that this tool does not support.

# Credits

This program contains code from the following other projects:

- [RLE-GIMP-Plugin](https://github.com/Daniel-McCarthy/RLE-GIMP-Plugin), a GIMP Plugin the support Neversoft RLE / BMR files
