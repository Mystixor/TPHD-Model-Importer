# TPHD-Model-Importer
This Python 3 (!!!) tool creates basic GMX files (TPHD 3d models) from CSV files (it is a common format for BFRES imports, I might add support for more in the future).

WARNING!

It is important to note, that the GMX format does not support seams on a model for UV maps, so whenever you have loose parts on your UV map they need to be loose parts on the actual mesh as well!


Instructions:

"python buildGMX.py your-csv-file.csv"
