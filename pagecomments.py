import cgi
import urllib
import datetime
import time
# from tzlocal import get_localzone

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

"""
    This shows how to do a very simple comment addition to a site
    It provides basic structure to eventually support responses to comments
    and needs lots of prettying up.
"""

MAIN_PAGE_FORM_TEMPLATE = """\
    <form action="/signed" method="post">
      Subject:
      <input value="%s" name="comment_subject"><br>
      Your comment:
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      Your name:
      <input value="%s" name="author_name">
      Your city:
      <input value="%s" name="author_location">
      <br><input type="submit" value="Submit Comment">
    </form>
"""

DEFAULT_SUBJECT = 'Your site'
DEFAULT_AUTHOR = 'Anonymous'
DEFAULT_LOCATION = 'Unknown'


def comment_key(comment_subject=DEFAULT_SUBJECT):
    """
    Constructs a Datastore key for a commentpost entity.
    We use comment_subject as the key.
    """
    return ndb.Key('Guestbook', comment_subject)


class Author(ndb.Model):
    """Sub model for representing an author."""
    authorname = ndb.StringProperty(indexed=False)
    authorlocation = ndb.StringProperty(indexed=False)


class CommentPost(ndb.Model):
    """A main model for representing an individual coment entry."""
    author = ndb.StructuredProperty(Author)
    subject = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class CommentsSection(webapp2.RequestHandler):
    """
    Build the main comment page
    """
    def get(self):
        self.response.write('<html><body>')
        comment_subject = self.request.get('comment_subject',
                                          DEFAULT_SUBJECT)
        author_name = self.request.get('author_name', 
                                        DEFAULT_AUTHOR)
        author_location = self.request.get('author_location', 
                                            DEFAULT_LOCATION)

        recentdate = datetime.datetime.now() - datetime.timedelta(days=3)

        greetings_query = ndb.gql('SELECT * FROM CommentPost WHERE date>:1 ORDER BY date DESC',recentdate)
        greetings = greetings_query.fetch(10)

        self.response.write(MAIN_PAGE_FORM_TEMPLATE % 
                            (cgi.escape(comment_subject),
                            cgi.escape(author_name),
                            cgi.escape(author_location)))

        # to_zone = get_localzone()

        for greeting in greetings:
            author = greeting.author.authorname
            authorplace = greeting.author.authorlocation
            commentsubject = greeting.subject
            postdate = greeting.date
            self.response.write('<br><b>%s</b> from %s wrote on %s at %s about %s: <i>%s</i>' % 
                                (cgi.escape(author), 
                                 cgi.escape(authorplace), 
                                 postdate.strftime("%B %d"),
                                 postdate.strftime("%H:%M"),
                                 cgi.escape(commentsubject),
                                 cgi.escape(greeting.content)))

        self.response.write('</body></html>')


class Guestbook(webapp2.RequestHandler):
    """
    Accept comments for the comment page
    """
    def post(self):
        comment_subject = self.request.get('comment_subject',
                                          DEFAULT_SUBJECT)
        author_name = self.request.get('author_name', 
                                        DEFAULT_AUTHOR)
        author_location = self.request.get('author_location', 
                                            DEFAULT_LOCATION)

        greeting = CommentPost(
                    parent=comment_key(comment_subject))

        greeting.author = Author(
                    authorname=author_name,
                    authorlocation=author_location)

        greeting.content = self.request.get('content')
        greeting.subject = comment_subject
        greeting.put()

        # sloppy way to be sure database is updated before reloading.
        # i would never do this in the real world
        time.sleep(1)
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', CommentsSection),
    ('/signed', Guestbook),
], debug=True)
