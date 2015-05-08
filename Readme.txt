Readme.txt

This uses python to generate an HTML file from a .txt file full of notes.

TO GENERATE THE HTML:
Run "python buildhtmlfromnotes.py"

By default, this will read notes.txt and generate a file called classnotesbuilt.html and now also you_tubers.html.

It requires the notes have very little formatting. The rules for the notes file are:
- Each section starts after a blank line
- The first line in the section is the title
- The second line in the section lists an image file and description, of the form: "filename  description"
- The rest of the lines in the section are the text of the class notes
- Bullets are created with a '**'