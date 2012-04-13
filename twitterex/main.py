#!/usr/bin/python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import tweepy # API de acesso ao twitter

# Variavel global com possivel mensagem de erro
errormessage = ''

# Modelo de banco de dados
class User(db.Model):
   username = db.StringProperty(required=True)
   reqproperty1 = db.StringProperty(required=True)
   reqproperty2 = db.StringProperty(required=True)
   optproperty = db.StringProperty()
   when = db.DateTimeProperty(auto_now_add=True)

# Tratador do aplicativo
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
	 self.tweet("user: " + self.request.get('username'))
      except:
	 errormessage = 'Algum campo obrigat&oacute;rio n&atilde;o foi preenchido!'

      self.redirect('/')

   def tweet(self,message):
      # informacoes da conta do twitter
      consumer_key = "RUHd84zbIf8lWmGLnouMA"
      consumer_secret = "YgfRXdxNi8CFSiAXeOBJp9uJuwN508eVpy9OxDh4"
      access_token = "552775803-jumbKROlK7wIwT0UG8ChjEZvZGRr7eYy5JVYC4GD"
      access_secret = "3rs3VW3mQvBXyJG3JR7jTmmJ4yCvNuJAAi6nYk44U"

      # autenticacao e atualizacao de status
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_secret)
      api = tweepy.API(auth)
      result = api.update_status(message)

def main():
   app = webapp.WSGIApplication([ (r'.*', TwitterExample) ], debug=True)
   wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
   main()

