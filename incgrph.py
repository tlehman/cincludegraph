# incgrph.py by Tobi Lehman
# date: Mon Aug 22 16:11:27 PDT 2011
# 
# Generate a digraph that visually represents C/C++ source file dependencies
import os
import argparse
# define some constants

parser = argparse.ArgumentParser(prog='incgrph.py', add_help=False)

# the path argument will supply the place the program should start
parser.add_argument('csrcpath', type=str, help='the path to the C/C++ source code')

# install the option to output the digraph to image
parser.add_argument('-i', dest='imgout', action='store_const', 
                    const=1, default=0, help='output to image')

# parse the command-line arguments
args = parser.parse_args()

# get contents of csrcpath directory
# get filenames from csrcpath
filenames = filter(lambda f: os.path.isfile(os.path.join(args.csrcpath, f)), 
                   os.listdir(args.csrcpath))    # NOTE for later: filter out based on list of acceptable 
                                                 # extensions like c, cpp, cxx, cu ... etc.

# the directed edges of the output graph
edges=set()

for filename in filenames:
    f = open(os.path.join(args.csrcpath, filename))
    lines = f.readlines()
    # isolate the lines in f that have "include" statements, use them to define edges
    # example:  
    #      foo.cpp   has   '#include "bar.h"'    defines    "foo.cpp" -> "bar.h"
    for line in lines:
        incstr = "#include"         # NOTE for later: make this a regular expression
        n = line.find(incstr)
        # if the file contains an "#include" statement, add the edge to the edge set
        if n != -1:
            # remove include statement from line
            line = line[len(incstr):]
            # remove comments from line
            if line.find("//") != -1:
                line = line[0:line.find("//")]
            elif line.find("/*") != -1:
                line = line[0:line.find("/*")]
            # remove tabs, spaces and newlines
            line = line.replace("\t", "").replace(" ","").replace("\n","")
            # construct directed edge
            s = '"' + filename + '" -> '+ line
            edges.add(s)

# get the directory name
digraph_name = args.csrcpath.split("/").pop()  
# remove all of the unsavory characters (e.g. ".", " ", ...)
digraph_name = digraph_name.replace(".","_").replace(" ","_")

# output the digraph in DOT format
#   for more information on DOT, see: http://www.graphviz.org/doc/info/lang.html 
#   and for a less formal intro, see: http://en.wikipedia.org/wiki/DOT_language
print("digraph %s {" % digraph_name)
for edge in edges:
    print(" "*4 + edge)
print("}")

