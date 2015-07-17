Readme.txt

This uses python to generate an HTML file from a .txt file full of notes and serve it directly to Google App Engine.  When not used in GAE it can instead be used to generate static html code.

TO RUN THE GAE:
Use app.yaml in GAE to run servpage.py.

TO GENERATE THE HTML to a static file:
Run "python buildhtmlfromnotes.py"

By default, this will read notes.txt and generate a file called classnotesbuilt.html and now also you_tubers.html.

It requires the notes have very little formatting. The rules for the notes file are:
- Each section starts after a blank line
- The first line in the section is the title
- The second line in the section lists an image file and description, of the form: "filename  description"
- The rest of the lines in the section are the text of the class notes
- Bullets are created with a '**'
- Don’t leave trailing lines at the end of the file.