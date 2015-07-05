#!/usr/bin/python
#
# buildhtmlfromnotes.py
#
# Goal of this is to generate HTML from  notes scrawled in a
# text file with the best ratio of cool output formatting to
# easy unstructured notetaking.

"""
Generates W3C-friendly HTML document from notes text file.
"""

# Import system modules

import jinja2
import os
import cgi

# Import custom modules

import getimageinfo
import videos
import youtubers
import pagecomments
#import webapp2

def load_templates(template_name):
    """
    Load the templates for jinja2 rendering
    """
    templat_dir = os.path.join(os.path.dirname(__file__),'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templat_dir),
                                   autoescape = True)
    return jinja_env.get_template(template_name)

# This reads the notes text file and turns the title, image, and section text
# into a list of lists (notes_list) that will be HTMLified later.
# this_sect is used to parse each section, with a structure:
# [title string, image info as a list, section text string]

def read_notes_into_list(notesfilename, max_width):
    """
    Reads a plaintext file and breaks it into concepts (separated by blank
    lines) and returns these as a list
    """
    notes_list = []
    this_sect = []
    j = 0
    with open(notesfilename, 'r') as openedfile:
# TODO: Add a double-line removal or handler to prevent breakage
        lastline = ''
        for line in openedfile:
            if line in ['\n', '\r\n'] and line != lastline:
                this_sect[1] = parse_image_text(this_sect[1], max_width)
                notes_list.append(this_sect)
                this_sect = []
                j = 0
            elif j == 3:
                this_sect[2] += ' ' + line.rstrip()
            else:
                this_sect.append(line.rstrip())
                j += 1
            lastline = line
        this_sect[1] = parse_image_text(this_sect[1], max_width)
        notes_list.append(this_sect)
    return notes_list

# Image text line in the notes file could be messy, this parses it and returns
# a 2 element list of [image file string, image alt text]
# this is simple now but could be robustified to handle weird input

def parse_image_text(imagetext, max_width):
    """
    Parses the messy image text and returns complete image tag
    """
    image_filenalt = [imagetext[:imagetext.find(' ')],
                        imagetext[imagetext.find(' ')+1:]]
    tagged_image = tag_image(image_filenalt[0], image_filenalt[1], max_width)
    return tagged_image

# Deliver appropriate HTML IMG tag string from a filename and the alt tag text
# It will automagically determine the pixel size

def tag_image(file_name, alt_string, max_width):
    """
    Returns an HTML image tag constructed from passed image filename, alt text,
    and the image's size (after auto-resizing to fit max_width)
    """
    image_tag = '<img src="' + file_name
    image_tag += '" alt=' + alt_string
    try:
        with open(file_name, "r") as myfile:
            size = getimageinfo.getImageInfo(myfile.read())
    except:
        size = ['', 100, 100]
        print "File error loading " + file_name
    resized = list(size)
    if resized[1] > max_width:
        resized[2] = max_width * resized[2] / resized[1]
        resized[1] = max_width
    image_tag += ' style="width:' + str(resized[1])
    image_tag += 'px;height:' + str(resized[2]) + 'px">'
    return image_tag

# From the concepts list, Generate all HTML into a big string

def generate_all_html(concepts_list, template):
    """
    Outputs a string of HTML build from inputted concepts_list
    """
    text_left = False
    for concept in concepts_list:
        if concept[2].find("**") != -1:
            concept[2] += '</ul>'
        concept.append(text_left)
        text_left = not text_left
    all_html = template.render(concepts_list=concepts_list)
    all_html = all_html.replace(': **', ''':
    </div>
    <div class="bulletlist">
      <ul>
        <li>''')
    all_html = all_html.replace('**', '''
        <li>''')
    all_html = all_html.replace('<pre>', '<pre class="codesample">')
    return all_html

# Push HTML into a file

def write_html_to_file(all_html, output_file):
    """
    simply outputs a string of HTML to the specified output file
    """
    with open(output_file, 'w') as openedfile:
        openedfile.write(all_html)
    print "HTML generated to" + output_file

# Generate youtube videos page

def make_youtubers():
    """
    Generates youtube videos page if youre on the internet
    """
    vid1 = videos.Video("https://www.youtube.com/watch?v=W45DRy7M1no")
    vid2 = videos.Video("https://www.youtube.com/watch?v=J---aiyznGQ")
    vid3 = videos.Video("https://www.youtube.com/watch?v=dMH0bHeiRNg")
    vid4 = videos.Video("https://www.youtube.com/watch?v=txqiwrbYGrs")
    vidlist = [vid1, vid2, vid3, vid4]
    youtubers.write_movies_page(vidlist)

# Page builder

class Page(object):
    ''' Reads the specified notes file and outputs it as a new HTML file'''

    def __init__(self, all_html):
        self.all_html = all_html

    def Build(self, all_html):
        template = load_templates("classnoteslayout.html")
        concepts_list = read_notes_into_list("notes.txt", 400)
        all_html = generate_all_html(concepts_list, template)
        self.all_html = all_html
        return self.all_html

# Main function if this is a standalone

def main():
    write_html_to_file(Page.Build(),"classnotesbuilt.html")
#TODO the javascript for youtubers doesnt work without internet.  
# Thanks SoutheWest Airlines for helping me find that bug
    make_youtubers()

# Do main if this is a standalone

if __name__ == "__main__":
    main()
