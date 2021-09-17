# -*- encoding: utf-8 -*-
"""
@File       :   ArticleReptile.py    
@Contact    :   mcfly@mail.sdu.edu.cn
@github     :   https://github.com/McflyWZX

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/9/17 15:32   Mcfly      1.0         None
"""
import requests
from lxml import etree
import pickle
import os
import string


class Book:
    def __init__(self, bookTxt: str, writer: str):
        self.bookTxt = bookTxt
        self.writer = writer

    def __repr__(self):
        return self.writer + '\r\n' + self.bookTxt

    def getWordTable(self):
        # 转化小写
        bookTxtLower = self.bookTxt.lower()
        # 去除标点
        bookTxtWithoutPunctuation = bookTxtLower.translate(str.maketrans({i: '' for i in string.punctuation}))
        wordsList = bookTxtWithoutPunctuation.split()
        wordsTable = set(wordsList)
        print(len(wordsTable))
        return wordsTable

    def getWords(self):
        # 转化小写
        bookTxtLower = self.bookTxt.lower()
        # 去除标点
        bookTxtWithoutPunctuation = bookTxtLower.translate(str.maketrans({i: '' for i in string.punctuation}))
        wordsList = bookTxtWithoutPunctuation.split()
        return wordsList


def getArticle(numBook: int):
    urlGetRoomInfo = "https://avalon.law.yale.edu/18th_century/fed%02d.asp" % numBook
    r = requests.post(urlGetRoomInfo)

    bookTree = etree.HTML(r.text)
    # 获取文章内容
    bookTxtList: list = bookTree.xpath('//div[@class="text-properties"]/p/text()')
    bookTxtList.extend(bookTree.xpath('//div[@class="text-properties"]/ol//li/text()'))
    bookTxtList.extend(bookTree.xpath('//div[@class="text-properties"]/ol//p/text()'))
    bookTxt = ''
    for bookSentence in bookTxtList:
        bookTxt += bookSentence
    # 获取作者名字
    TitleTxtList = bookTree.xpath('//div[@class="text-properties"]//td[@align="center"]//h4/text()')
    TitleTxtList = TitleTxtList or bookTree.xpath('//div[@class="text-properties"]//td[@align="center"]//h3/text()')
    *_, writer = TitleTxtList
    writer = writer.rstrip().strip('\r\n')
    book = Book(bookTxt, writer)
    return book


def getAllArticle():
    # 读取全部85篇文章
    minLen, minIndex = 99999, 99
    books = {}
    for i in range(85):
        book = getArticle(i + 1)
        if book.writer not in books.keys():
            books[book.writer] = []
        books[book.writer].append(book)
        if len(book.bookTxt) < minLen:
            minLen, minIndex = len(book.bookTxt), i + 1
        print('\rDownload the articles: len%04d %02d/85' % (len(book.bookTxt), (i + 1)), end='')
    print('\r\nThe min len article is %02d with len: %03d' % (minIndex, minLen))
    # 将对象数据储存在文件
    path = os.getcwd()
    for writer, bookOneWriter in books.items():
        # 判断文件夹是否存在并自动创建
        if not os.path.exists(path + '\\Article\\' + writer):
            os.makedirs(path + '\\Article\\' + writer)
        # 储存对象
        i = 0
        for book in bookOneWriter:
            with open(path + '\\Article\\' + writer + '\\' + writer + '%02d.pkl' % i,
                      'wb') as f:  # open file with write-mode
                pickle.dump(book, f)  # serialize and save object
            i += 1


def loadArticles(writer: str):
    articles = []
    path = os.getcwd()
    i = 0
    path = path + '\\Article\\' + writer + '\\' + writer
    while os.path.exists(path + '%02d.pkl' % i):
        f = open(path + '%02d.pkl' % i, 'rb')
        article: Book = pickle.load(f)
        articles.append(article)
        i += 1
    return articles
