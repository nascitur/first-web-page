#!/usr/bin/python
#
# handle.py

import webapp2
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# class MainPage(Handler):
#     def get(self):
#         foodlist = self.request.get_all("food")
#         self.render("shoppinglist.html", name=foodlist, foodlist=foodlist)


app = webapp2.WSGIApplication([('/', MainPage),
                                ],
                              debug=True)

# total:
# self.response.out.write(jinja_env.get_template())