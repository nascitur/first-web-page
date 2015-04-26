#!/usr/bin/python
#
# buildhtmlfromnotes.py 
#
# Goal of this is to generate HTML from  notes scrawled in a 
# text file with the best ratio of cool output formatting to 
# easy unstructured notetaking.

# Import necessary modules

import mmap
import os
import xml.etree.ElementTree as ET
import getimageinfo


def read_section_into_list(notes_lines):
    pass

def read_notes_into_list(notesfilename):
    notes_list = []
    this_sect = []
    i = 0
    j = 0
    with open(notesfilename, 'r') as f:
        for line in f:
            if line in ['\n', '\r\n']:
                notes_list.append(this_sect)
                print this_sect
                this_sect = []
                i += 1
                j = 0
            elif j == 0:
                this_sect.append(line.rstrip())
                print "Got title for", i
                j += 1
            elif j == 1:
                this_sect.append(line.rstrip())
                print "Got image for", i
                j += 1
            elif j == 2:
                this_sect.append(line.rstrip())
                j += 1
            elif j == 3:
                this_sect[2] += line
    return notes_list
#        notes_data = f.read()

#   while notes_data != ''
#        notes


# Deliver appropriate HTML IMG tag string from a filename and the alt tag text
# It will automagically determine the pixel size

def tag_image(file_name, alt_string):
    image_tag = '<img src="' + file_name
    image_tag += '" alt="' + alt_string
    with open(file_name, "r") as myfile:
        size = getimageinfo.getImageInfo(myfile.read())
    image_tag += '" style="width:' + str(size[1])
    image_tag += 'px;height:' + str(size[2]) + 'px">'
    return image_tag



# Main function

def main():
    funky = []
    funky.append("funk")
    funky.append("more funk")
    funky.append("most funk")
    print funky
    print read_notes_into_list("testnotes.txt")

# Do main

if __name__ == "__main__": 
    main()