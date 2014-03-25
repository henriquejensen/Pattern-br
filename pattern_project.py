# coding: utf-8

from pattern.web import Twitter
from pattern.db import Database, SQLITE
from pattern.db import pd
from pattern.db import field, pk, INTEGER, UNIQUE, STRING
from sqlite3 import IntegrityError

team = ['#galo', '#Galo', '#Atletico-MG', '#atletico mineiro']

twitter = Twitter()
db = Database(pd('tweets.db'))

if not "tweets" in db:
	schema = (pk(), field('code', INTEGER, index=UNIQUE), field('text', STRING(140)))
	db.create("tweets", schema)

#query in Twitter
for hashtag in team:
	for tweet in twitter.search(hashtag):
		try:
			db.tweets.append(code = tweet.id, text = tweet.text)
		except IntegrityError:
			pass

#Separate tweets in database
for data in db.tweets.filter():
	print data[2]
	print '-'*30

