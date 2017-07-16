# -*- coding: utf-8 -*-
import oauth2
import json
import urllib
import tweepy
from keys import *
import psycopg2


# Faz a autenticação no twitter
def conexao_twitter():
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    token = oauth2.Token(TOKEN_KEY, TOKEN_SECRET)
    cliente =  oauth2.Client(consumer, token)
    return cliente


# Requisicao básica
def requisicao(conta):
    api = conexao_twitter()
    url = urllib.parse.quote_plus(conta)
    response = api.request('https://api.twitter.com/1.1/search/tweets.json?q=%23viagem+AND+' +  url, method='GET')
    response_decoded = response[1].decode()
    return response_decoded


# pega a hashtag passada
def hashtags(hashtag):
    todas_hashtags = requisicao(hashtag)
    htgs = json.loads(todas_hashtags)
    return htgs


# faz a autenticação do tweepy
def tweepy_auth(ck, cs, tk, ts):
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(tk, ts)
    api = tweepy.API(auth)
    return api


# retweeta usando o tweepy
def retweet(id_usuario, nome_usuario):
    api = tweepy_auth(ck=CONSUMER_KEY, cs=CONSUMER_SECRET, tk=TOKEN_KEY, ts=TOKEN_SECRET)
    api.update_status(status="@" + nome_usuario + " conheça o www.meuchipdeviagem.com.br", in_reply_to_status_id=int(id_usuario))
    print('Enviado uma resposta para o tweet id: ' + id_usuario)


def conexao_db():
    try:
        connection = psycopg2.connect("dbname='twitterdb' user='twitter_user' host='localhost' password='abc123'")
        print("Conectado ao banco de dados com sucesso")
    except:
        print ("Ocorreu um erro ao conectar com o banco de dados")

conexao_db()

hashtags = hashtags('#Alemanha')

mcv = hashtags['statuses']
for dado in mcv:
    print ('ID: ' + str(dado['id']))
    print ('Usuário: ' + dado['user']['screen_name'])
    print ('Tweet: ' + str(dado['text']))
    #retweet(str(dado['id']), dado['user']['screen_name'])


#consulta = json.loads(response_decoded)
