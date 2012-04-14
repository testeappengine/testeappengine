#!/usr/bin/python

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import tweepy # API de acesso ao twitter

# Variavel global com mensagem de status
statusmessage = ''

# Modelo de banco de dados
class User(db.Model):
   username = db.StringProperty(required=True)
   phone = db.StringProperty(required=True)
   email = db.StringProperty(required=True)
   twitter = db.StringProperty()

# Pagina de cadastro
class SignPage(webapp.RequestHandler):

   site_url = 'http://twitterex-selecao.appspot.com'

   def get(self):
      global statusmessage
      values = {
	 'statusmessage': statusmessage,
      }
      self.response.out.write(template.render('main.html',values))
      statusmessage = ''

   def post(self):
      global statusmessage

      try: 
         user = User(
            username=self.request.get('username'),
            phone=self.request.get('phone'),
            email=self.request.get('email'),
            twitter=self.request.get('twitter')
         )
         user.put()
	 statusmessage = '<font color=green>Usu&aacute;rio ' + self.request.get('username') +' cadastrado com sucesso!</font>'
	 try:
            if self.request.get('twitter') != '':
               mensagem = "@" + self.request.get('twitter') + " acabou de se cadastrar no site " + self.site_url
            else:
               mensagem = self.request.get('username') + " acabou de se cadastrar no site " + self.site_url
  	    self.tweet(mensagem)
	 except:
	    statusmessage = '<font color="red">Erro ao postar mensagem no twitter.</font>'
      except:
	 statusmessage = '<font color="red">Algum campo obrigat&oacute;rio n&atilde;o foi preenchido!</font>'

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

# Pagina de lista de usuarios
class UsersPage(webapp.RequestHandler):
   def get(self):
      global statusmessage
      users = db.GqlQuery(
         'SELECT * FROM User '
	 'ORDER BY username ')
      values = {
         'users': users,
	 'statusmessage': statusmessage,
      }
      self.response.out.write(template.render('users.html',values))


def main():
   app = webapp.WSGIApplication([ ('/', SignPage),
   				  ('/users', UsersPage) ])
   wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
   main()

