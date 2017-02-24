import feedparser
import re

# Selecting Sources
feedlist = ['http://gis.harvard.edu/taxonomy/term/303/feed',
            'http://rss.sciencedirect.com/publication/science/01681699',
            'http://www.geosci-model-dev.net/xml/rss2_0.xml',
            'http://link.springer.com/search.rss?facet-content-type=Article&amp;facet-journal-id=122&amp;channel-name=Theoretical%20and%20Applied%20Genetics',
            'http://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1757-1707',
            'http://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1467-9671',
            'http://www.tandfonline.com/action/showFeed?ui=0&amp;mi=l9vf8z&amp;ai=16s&amp;jc=tgis20&amp;type=etoc&amp;feed=rss',
            'https://dl.sciencesocieties.org/publications/cs/rss',
            'http://rss.cnki.net/kns/rss.aspx?journal=zgde&amp;virtual=knavi',
            'http://rss.sciencedirect.com/publication/science/01681923',
            'http://link.springer.com/search.rss?facet-content-type=Article&amp;facet-journal-id=11442&amp;channel-name=Journal+of+Geographical+Sciences',
            'http://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1365-2486',
            'http://rss.sciencedirect.com/publication/science/01678809',
            'http://rss.sciencedirect.com/publication/science/01989715',
            'http://rss.sciencedirect.com/publication/science/03784290',
            'http://rss.sciencedirect.com/publication/science/00344257', ]


# Downloading Sources
def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c

    return p


def separatewords(txt):
    splitter = re.compile('\\W*')

    return [s.lower() for s in splitter.split(txt) if 3 < len(s) < 30]


def getarticlewords():
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0
    for feed in feedlist:
        f = feedparser.parse(feed)

        for e in f.entries:
            if e.title in articletitles: continue

            txt = e.title.encode('utf8') + stripHTML(e.description.encode('utf8'))
            words = separatewords(txt)
            articlewords.append({})
            articletitles.append(e.title)

            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ec += 1
    return allwords, articlewords, articletitles


# Converting to a Matrix
def makematrix(allw, articlew):
    wordvec = []

    for w, c in allw.items():
        if 3 < c < len(articlew) * 0.6:
            wordvec.append(w)

    ll = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]

    return ll, wordvec
