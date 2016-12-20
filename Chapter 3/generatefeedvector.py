# -*- coding: utf-8 -*-
# 定义编码格式
import feedparser
import re


def getWordCounts(url):
    d = feedparser.parse(url)
    wc = {}

    # 循环遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.decription

        words = getWords(e.title + '' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed.title, wc


def getWords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word != '']

apcount={}
wordcounts={}
title, wc = getWordCounts('http://rss.sciencedirect.com/publication/science/00344257')
wordcounts[title] = wc
for word, count in wc.items():
    apcount.setdefault(word,0)
    if count>1:
        apcount[word] +=1

# wordlist =[]
# for w, bc in apcount.items():
# out = file('blogdata.txt','w')
# out.write('Blog')
# for word in word
