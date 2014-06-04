# coding: utf-8

from pattern.web import Twitter, Google, Facebook, URLTimeout
from pattern.db import Database, pd, field, pk, INTEGER, UNIQUE, STRING
from sqlite3 import IntegrityError
from pattern.search import search
import querys
import os


def menu():
    print '''
    1 - Veja os trendtopics do dia
    2 - Digite o tweet da busca
    3 - Analisar os tweets da busca
    4 - Apagar tweet ou texto das buscas
    5 - Apagar tweets do banco de dados
    0 - Sair
        '''
    try:
        choose = raw_input(" escolha uma opção: ")
        print
        return choose
    except:
        return


def trendtopics():
    '''
    Função que retorna os 10 assuntos mais comentados no twitter no instante da busca

    obs: a conversao u'' de unicode, serve para tratar os caracteres especiais que
    existem nos comentarios do twitter.

    '''
    count = 0
    for trend in twitter.trends():
        count += 1
        try:
            print str(count) + u'º ' + trend

        except URLTimeout:
            print(" ****Conexão com problema****\n")
            return


def search_tweet():
    '''
    Função que faz a busca no twitter de determinado assunto que o usuario digitar.

    # em cada palavra (hashtag)
    tweets é uma lista que armazena o tweet de busca do usuario com um
    que ele passar. Para cada hashtag dentro de tweets, ele faz uma busca no Twitter

    '''
    exit = "sim"
    while exit == "sim":
        hashtag = raw_input(
            "  Digite o tweet que deseja buscar: ").replace(" ", '')

        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag

        if not hashtag in tweets:
            tweets.append(hashtag)

        exit = raw_input(
            " Deseja adicionar outro tweet digite - sim ou nao:  ").lower()

    if not "tweets" in db:
        # se não existir o banco de dados de tweets, então ele é criado
        schema = (
            pk(), field('code', INTEGER, index=UNIQUE), field('text', STRING(140)))
        db.create("tweets", schema)

    try:
        for hashtag in tweets:
            # query in Twitter
            for tweet in twitter.search(hashtag):
                try:
                    db.tweets.append(code=tweet.id, text=tweet.text)
                except IntegrityError:
                    pass
    except URLTimeout:
        print(" ****Conexão com problema****\n")
        pass

    print
    # Separate tweets in database
    for data in db.tweets.filter():
        print(u' {id}º - {text}').format(id = data[0], text = data[2])
        print '-' * 100


def analisador_tweets():
    '''
    Função faz a busca no banco de dados de todos os tweets armazenados nas buscas e imprime na tela

    '''
    exit = 'sim'
    while exit == 'sim':
        try:
            enter = raw_input(" Digite o texto que deseja buscar nos tweets: ")
            if not enter in words:
                words.append(enter)
            else:
                print(" Texto ja existe\n")
            exit = raw_input(
                " Deseja adicionar outro texto digite - sim ou nao:  ").lower()
        except:
            print(" ****Entrada inválida****\n")
            exit = 'nao'
            pass

    print
    find = 0
    for tweet in db.tweets.filter():
        for i in words:
            if search(i, tweet[2]):
                find = 1
                print(u' {text}').format(text = tweet[2])
                print '-' * 100

    if find == 0:
        print(" ****Não existem tweets com esse texto****\n")


def apagar_busca():
    '''
    Função que apaga os tweets digitados pelo usuario ou o texto que foi utilizado
    para busca no Twitter

    '''
    exit = 'sim'
    try:
        while exit == 'sim':
            choose = raw_input(
                '''\n 1 - Apagar tweets da busca\n 2 - Apagar textos da busca\n 0 - Retornar ao menu principal\n escolha: ''')

            if choose == '1':
                print("\n tweets registrados")
                for t in tweets:
                    print(" {s} | ").format(s = t),
                eraser = raw_input("\n digite o tweet a ser removido: ")

                if eraser in tweets:
                    tweets.remove(eraser)
                    print("\n tweet removido com sucesso\n")
                else:
                    print(" tweet não existe\n")

            elif choose == '2':
                print("\n textos registrados")
                for w in words:
                    print(" {s} | ").format(s = w),
                eraser = raw_input("\n digite o texto a ser removido: ")

                if eraser in words:
                    words.remove(eraser)
                    print("\n texto removido com sucesso\n")
                else:
                    print(" texto não existe\n")
            else:
                return

            exit = raw_input(" Deseja continuar - sim ou nao:  ").lower()
    except:
        print("\n ****Opção invalida****\n")
        return

def apagar_bd():
    '''
    Função que apaga o banco de dados caso ele exista

    '''
    try:
        os.remove("/media/dados/jensen/Pattern-br/tweets.db")
        print("\n ****Banco apagado com sucesso****\n")

    except:
        print(" ****Não existe banco de dados****\n")
        return

def main():
    choose = "nao"

    while choose != "sim":
        choose = menu()

        if choose == '1':
            trendtopics()
        elif choose == '2':
            search_tweet()
        elif choose == '3':
            analisador_tweets()
        elif choose == '4':
            apagar_busca()
        elif choose == '5':
            apagar_bd()
        elif choose == '0':
            choose = "sim"
        elif choose.lower() == 'x':
            print("\n ****Função em construção****\n")
        else:
            print("\n ****Opção invalida****")


if __name__ == '__main__':
    print '\t' + 30 * '-' + "\n\t\tBienvenido\n\t" + 30 * '-'

    twitter = Twitter()
    google = Google()
    face = Facebook()
    tweets = []
    words = []
    db = Database(pd('tweets.db'))
    main()

    print '\t' + 30 * '-' + "\n\t\tWinter is coming\n\t" + 30 * '-'
