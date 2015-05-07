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

# Import necessary modules

import getimageinfo


# This reads the notes text file and turns the title, image, and section text
# into a list of lists (notes_list) that will be HTMLified later.
# this_sect is used to parse each section, with a structure:
# [title string, image info as a list, section text string]

def read_notes_into_list(notesfilename):
    """
    Reads a plaintext file and breaks it into concepts (separated by blank
    lines) and returns these as a list
    """
    notes_list = []
    this_sect = []
    j = 0
    with open(notesfilename, 'r') as openedfile:
        for line in openedfile:
            if line in ['\n', '\r\n']:
                this_sect[1] = parse_image_text(this_sect[1])
                notes_list.append(this_sect)
                this_sect = []
                j = 0
            elif j == 3:
                this_sect[2] += ' ' + line.rstrip()
            else:
                this_sect.append(line.rstrip())
                j += 1
        this_sect[1] = parse_image_text(this_sect[1])
        notes_list.append(this_sect)
    return notes_list


# Image text line in the notes file could be messy, this parses it and returns
# a 2 element list of [image file string, image alt text]
# this is simple now but could be robustified to handle weird input

def parse_image_text(imagetext):
    """
    The image line in the notes text file is messy, this parses it.
    """
    image_fileandalt = [imagetext[:imagetext.find(' ')],
                        imagetext[imagetext.find(' ')+1:]]
    return image_fileandalt


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

def generate_all_html(concepts_list):
    """
    Outputs a string of HTML build from inputted concepts_list
    """
    text_left = False
    all_html = '''
<!doctype html>

  <!-- classnotes.html -->

  <!-- I decided to try to use some cues from other pages, sort of an article flow or corporate About page style-->

<html>

<head>
  <meta charset="UTF-8" />
  <title>Class notes from the first lesson</title>
  <link rel="stylesheet" href="classnotes.css" type="text/css" />
</head>

<body>

  <!-- PAGE TITLE -->

<div class="title">
    <h1 class="pagetitle">Class notes from <strong class="keyword">Intro to Programming</strong></h1>
</div>'''
    for concept in concepts_list:
        print concept[0]
        print concept[1]
        all_html += '''
<div class="section">'''
        if text_left:
            all_html += '''
  <div class="section-texttoleft">
    <div class="sectiontitle">
      <h2>''' + concept[0] + '''</h2>
    </div>
    <div>
      <P>''' + concept[2]
            if concept[2].find("**") != -1:
                all_html += "</ul>"
            else:
                all_html += "</p>"
            all_html += '''
    </div>
  </div>
  <div class="imagetoright">
    ''' + tag_image(concept[1][0], concept[1][1], 400) + '''
  </div>
</div>'''
        else:
            all_html += '''
  <div class="imagetoleft">
    ''' + tag_image(concept[1][0], concept[1][1], 400) + '''
  </div>
  <div class="section-texttoright">
    <div class="sectiontitle">
      <h2>''' + concept[0] + '''</h2>
    </div>
    <div>
      <P>''' + concept[2]
            if concept[2].find("**") != -1:
                all_html += "</ul>"
            else:
                all_html += "</p>"
            all_html += '''
    </div>
  </div>
</div>'''
        text_left = not text_left
    all_html += '''

</body>

</html>'''
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

# Main function

def main():
    ''' Reads the specified notes file and outputs it as a new HTML file'''
    concepts_list = read_notes_into_list("notes.txt")
    all_html = generate_all_html(concepts_list)
    write_html_to_file(all_html, "classnotesbuilt.html")

# Do main

if __name__ == "__main__":
    main()

