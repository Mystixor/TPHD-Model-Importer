# TPHD-Model-Importer
This Python 3 (!!!) tool (fork) creates basic GMX files (TPHD 3d models) from Collada (.dae) files.

WARNING!

It is important to note, that the GMX format does not support seams on a model for UV maps, so whenever you have loose parts on your UV map they need to be loose parts in the actual mesh as well!


Instructions:

"python -m pip install numpy" (Only on the first time, if you did not have Numpy installed yet)

"python buildGMX.py your-csv-file.csv"
