#!/usr/bin/python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

errormessage = ''

class User(db.Model):
   username = db.StringProperty(required=True)
   reqproperty1 = db.StringProperty(required=True)
   reqproperty2 = db.StringProperty(required=True)
   optproperty = db.StringProperty()
   when = db.DateTimeProperty(auto_now_add=True)

class TwitterExample(webapp.RequestHandler):
   def get(self):
      global errormessage
      users = db.GqlQuery(
         'SELECT * FROM User '
	 'ORDER BY when DESC ')
      values = {
         'users': users,
	 'errormessage': errormessage,
      }
      self.response.out.write(template.render('main.html',values))
      errormessage = ''
   def post(self):
      global errormessage
      try: 
         user = User(
            username=self.request.get('username'),
            reqproperty1=self.request.get('reqproperty1'),
            reqproperty2=self.request.get('reqproperty2'),
            optproperty=self.request.get('optproperty')
         )
         user.put()
      except:
	 errormessage = 'Algum campo obrigat&oacute;rio n&atilde;o foi preenchido!'

      self.redirect('/')

def main():
   app = webapp.WSGIApplication([ (r'.*', TwitterExample) ], debug=True)
   wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
   main()

