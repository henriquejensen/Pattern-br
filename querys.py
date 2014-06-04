# coding: utf-8

from pattern.db import Database, pd, field, pk, UNIQUE, STRING, INTEGER
from pattern.web import Twitter, Google, Facebook


class QueryGoogle(object):

    def __init__(self):
        self.dbGoogle = Database(pd("google.db"))
        self.listaBusca = []
        if not "google" in self.dbGoogle:
            schema = (
                pk(), field('url', STRING(), index=UNIQUE),
                field('titulo', STRING(140)), field('text', STRING(140)))
            self.dbGoogle.create("google", schema)

    def busca(self, args):
        goo = Google()
        for g in goo.search(args):
            self.listaBusca.append(g.url)

    def imprimirBuscas(self):
        if self.listaBusca == []:
            print("Não existem buscas")

        else:
            for i in self.listaBusca:
                print(i)

    def apagarBuscas(self, palavra):
        if self.listaBusca == []:
            print("Não existem buscas")

        elif palavra in self.listaBusca:
            self.listaBusca.remove(palavra)

        else:
            print("busca não existe")


class QueryTwitter(QueryGoogle):

    def __init__(self):
        self.dbTwitter = Database(pd("twitter.db"))
        self.listaBusca = []
        if not "twitter" in self.dbTwitter:
            schema = (
                pk(), field('code', INTEGER, index=UNIQUE),
                field('text', STRING(140)))
            self.dbTwitter.create("twitter", schema)

        def busca(self, args):
            goo = Twitter()
            for g in goo.search(args):
                self.listaBusca.append(g.url)


class QueryFacebook(QueryGoogle):

    def __init__(self):
        self.dbFace = Database(pd("facebook.db"))
        self.listaBusca = []
        if not "facebook" in self.dbFace:
            schema = (
                pk(), field('code', INTEGER, index=UNIQUE),
                field('text', STRING(140)),
                field('url', STRING()))
            self.dbFace.create("twitter", schema)

    def busca(self, args):
        goo = Facebook()
        for g in goo.search(args):
            self.listaBusca.append(g.url)
