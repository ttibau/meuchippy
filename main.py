# -*- coding: utf-8 -*-
import oauth2
import json
import urllib
import tweepy
from keys import *
import psycopg2
from datetime import date
import datetime
import sys
import time

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
    api.update_with_media(filename='folder.jpg', status="@" + nome_usuario + " quer viajar e já ter seu chip de celular configurado aqui mesmo no Brasil? Acesse: http://bit.ly/meuchipdeviagem O MELHOR PREÇO", in_reply_to_status_id=int(id_usuario))
    print('Enviado uma resposta para o tweet id: ' + id_usuario)


# Conecta ao banco de dados
def conexao_db():
    try:
        connection = psycopg2.connect("dbname='twitterdb' user='twitter_user' host='localhost' password='abc123'")
    except:
        print ("Ocorreu um erro ao conectar com o banco de dados")
    return connection


# Insere os dados ao banco
def insert_db(usuario, texto, data, id_tweet, hashtag):
    conn = conexao_db()
    cursor = conn.cursor()
    print("Inserindo dados")
    try:
        cursor.execute("INSERT INTO tweets (usuario, texto, data, id_tweet, hashtag) VALUES (%s, %s, %s, %s, %s)", (usuario, texto, data, id_tweet, hashtag))
        conn.commit()
    except:
        print ("Deu erro ao salvar os dados na tabela")


# Método que vai verificar se o id do tweet já está no banco de dados
# Se retornar falso, o tweet já foi enviado hoje, logo não deve ser feito o retweet
def verifica_tweet(id_tweet):
    conn = conexao_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets WHERE id_tweet = '{0}'".format(id_tweet))
    tweets = cursor.fetchall()
    for tweet in tweets:
        hoje = date.today().toordinal()
        data_banco = tweet[3].toordinal()
        print (hoje, data_banco)
        if (hoje <= data_banco):
            return False
        elif(tweet == None):
            return False
        else:
            return True

hashtag_query = str(sys.argv[1])
print (hashtag_query)
hashtags = hashtags(hashtag_query) # Vai pegar os tweets com essa hashtag
mcv = hashtags['statuses']
print ("Quantidade coletada: ", len(mcv))
for dado in mcv:
    tweet_usuario = str(dado['user']['screen_name'])
    tweet_id = str(dado['id'])

    tweet_texto = str(dado['text'])
    tweet_verificacao = verifica_tweet(tweet_id)
    print (tweet_verificacao)
    if (tweet_verificacao == True):
        retweet(str(dado['id']), dado['user']['screen_name'])
        insert_db(usuario=tweet_usuario, texto=tweet_texto, data=datetime.datetime.now(), id_tweet=tweet_id, hashtag=hashtag_query)
        print("Retweetado e salvo no banco, aguardando mais 15 segundos para retweetar novamente")
        time.sleep(30)
    elif(tweet_verificacao == False):
        print("Não salva no banco, o tweet já foi feito hoje")
    elif(tweet_verificacao == None):
        print("O id é inexistente no banco")
        retweet(str(dado['id']), dado['user']['screen_name'])
        insert_db(usuario=tweet_usuario, texto=tweet_texto, data=datetime.datetime.now(), id_tweet=tweet_id, hashtag=hashtag_query)
        print("Retweetado e salvo no banco, aguardando mais 15 segundos para retweetar novamente")
        time.sleep(30)
