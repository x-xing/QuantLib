from os import listdir
from os.path import isfile, join

mypath = 'C:/Library/QuantLib-SWIG-1.13/Python/test/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
keyword = r'Size'

for file in files:
    with open(mypath + file, "r") as f:
        searchlines = f.readlines()
    for i, line in enumerate(searchlines):
        if keyword in line: 
            print('Keyword: %s found in file: %s at line: %d' % (keyword, file ,i))
            