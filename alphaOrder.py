import argparse
import os
import sys

# create the comand line arguments
parser = argparse.ArgumentParser(description="Sort a file")
parser.add_argument("--input", "-i", dest="inFile", required=True, type=argparse.FileType("r"), help="The file with the new line sepearted list")
parser.add_argument("--case", "-c", dest="case", required=False, action="store_false", help="Sort ABav to ABab or AaBa")

# parse them
args = parser.parse_args()
inFile = args.inFile
caseSensetive = args.case
args = None # help GC

# check to see if we can output to a file
if os.path.exists(inFile.name+".sorted"):
  print "Error: output file allready exists"
  sys.exit(-1)

# let the user know all is good
print "starting to sort {file}".format(file=inFile.name)

# read the file into memory
userList = list()
for line in inFile:
  line = line.replace("\n", "")
  if line == "":
    continue
  userList.append(line)
inFile.close()

# sort
if caseSensetive:
  userList.sort()
else:
  print "Using case sensetive sort"
  userList.sort(key=lambda x: x.lower())

# ouput to file
outFile = file(inFile.name+".sorted", mode="w")
for line in userList:
  outFile.write(line+"\n")
outFile.close()

print "Finished sorting\nSee {file}".format(file=outFile.name)

