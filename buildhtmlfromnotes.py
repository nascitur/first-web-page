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

# This reads the notes text file and turns the title, image, and section text
# into a list of lists (notes_list) that will be HTMLified later.
# this_sect is used to parse each section, with a structure:
# [title string, image info as a list, section text string]

def read_notes_into_list(notesfilename):
    notes_list = []
    this_sect = []
    i = 0
    j = 0
    with open(notesfilename, 'r') as f:
        for line in f:
            if line in ['\n', '\r\n']:
                this_sect[1] = parse_image_text(this_sect[1])
                notes_list.append(this_sect)
                print this_sect
                this_sect = []
                i += 1
                j = 0
            elif j == 3:
                this_sect[2] += ' ' + line.rstrip()
            else:
                this_sect.append(line.rstrip())
                j += 1
        this_sect[1] = parse_image_text(this_sect[1])
        notes_list.append(this_sect)
    return notes_list


# Image text line could be messy, this parses it and returns a 2 element list
# of [image file string, image alt text]
# this is simple now but could be robustified to handle weird input

def parse_image_text(imagetext):
    image_fileandalt = [imagetext[:imagetext.find(' ')],
                        imagetext[imagetext.find(' ')+1:]]
    return image_fileandalt


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
    print read_notes_into_list("testnotes.txt")
    print read_notes_into_list("notes.txt")

# Do main

if __name__ == "__main__": 
    main()