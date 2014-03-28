# coding: utf-8

from pattern.web import Twitter
from pattern.db import Database, SQLITE, pd, field, pk, INTEGER, UNIQUE, STRING
from sqlite3 import IntegrityError
from pattern.search import search

twitter = Twitter()
db = Database(pd('tweets.db'))

teams = []
words = ['campeão|jogo|vitória|partida|campeonato']

def menu():
	print '''
	1 - Veja os trendtopics do dia
	2 - Digite o tweet da busca
	3 - Analisar os tweets da busca
	4 - 
		'''
	escolha = int(input(""))
	return escolha

def trendtopics():
	count=0
	for trend in twitter.trends():
		count+=1
		print str(count) + u'º ' + trend
	
def search_tweet():
	sair = "n"
	while sair!="s":
		team = raw_input("  Digite o tweet que deseja buscar ").replace(" ", '')
		
		if not team.startswith("#"):
			team = "#"+team
			
		if not team in teams:
			teams.append(team)
		
		sair = raw_input("  Se não deseja adcionar outro tweet digite s: ").lower()	

	if not "tweets" in db:
		schema = (pk(), field('code', INTEGER, index=UNIQUE), field('text', STRING(140)))
		db.create("tweets", schema)

	#query in Twitter
	for hashtag in teams:
		for tweet in twitter.search(hashtag):
			try:
				db.tweets.append(code = tweet.id, text = tweet.text)
			except IntegrityError:
				pass

	#Separate tweets in database
	for data in db.tweets.filter():
		print data[2]
		print '-'*30
		
def analisador_tweets():
	for tweet in db.tweets.filter():
		teste = search(words, tweet[2])
		if teste != '[]':
			print tweet[2]
	return
	
	
	

def main():
	escolha="nao"
	
	while escolha!="sim":
		escolha = menu()
		
		if escolha == 2:
			search_tweet()			
		if escolha == 1:
			trendtopics()
		if escolha == 3:			
			analisador_tweets()
		if escolha == 4:
			print "Função em construção"
			
main()
