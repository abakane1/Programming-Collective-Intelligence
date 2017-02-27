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
    # 正则删除html
    txt = re.compile(r'<[^>]+>').sub('', html)
    # 正则提取单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word != '']


apcount = {}
wordcounts = {}
feedlist = [line for line in file('Data/feedlist.txt')]
for feedurl in feedlist:
    title, wc = getWordCounts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

# 选择出现概率在10%~50%单词
wordlist = []
for w, bc in apcount.items():
    frac = float(bc) / len(feedlist)
    if 0.1 < frac < 0.5: wordlist.append(w)

# Output
out = file('Result/blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
