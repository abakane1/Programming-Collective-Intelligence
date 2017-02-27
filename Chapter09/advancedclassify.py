from pylab import *
import googlemaps
from datetime import datetime
import csv
from svm import *


#######################
#
#
#
#######################
class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]
        self.match = int(row[len(row) - 1])


def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','), allnum))
    return rows


# visualization
def plotagematches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, 'go')
    plot(xdn, ydn, 'ro')

    show()


##################
#
# Basic Linear Classification
#
##################

def lineartrain(rows):
    averages = {}
    counts = {}
    for row in rows:
        cl = row.match
        averages.setdefault(cl, [0.0] * (len(row.data)))
        counts.setdefault(cl, 0)

        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])

        counts[cl] += 1

    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]

    return averages


def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])


def veclength(v):
    return sum([p ** 2 for p in v])


def dpclassify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0:
        return 0
    else:
        return 1


#################
#
# Categorical Features
#
#################

# Yes/No Questions
def yesno(v):
    if v == 'yes':
        return 1
    elif v == 'no':
        return -1
    else:
        return 0


# Lists of Interests
def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x += 1
    return x


# Determining Distances Using Google Maps
def milesdistance(a1, a2):
    gmaps = googlemaps.Client(key='AIzaSyC37Ex3LHElQWLUbLN81DkO4SNIjpubKH0')
    geodistance = gmaps.distance_matrix(a1, a2)
    if geodistance['status'] == 'OK':
        for row in geodistance['rows']:
            mils = float(row['elements'][0]['duration']['text'].split(' ')[0])
            return mils

    else:
        return 0


def testgooglemap():
    gmaps = googlemaps.Client(key='AIzaSyC37Ex3LHElQWLUbLN81DkO4SNIjpubKH0')
    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions("Sydney Town Hall",
                                         "Parramatta, NSW",
                                         mode="transit",
                                         departure_time=now)
    return directions_result


# Creating the New Dataset
def loadnumerical():
    oldrows = loadmatch('matchmaker.csv')
    newros = []
    dataCSV = open('newmatch.csv', 'w')
    writer = csv.writer(dataCSV, dialect='excel')
    for row in oldrows:
        d = row.data
        data = [float(d[0]), yesno(d[1]), yesno(d[2]), float(d[5]), yesno(d[6]), yesno(d[7]), matchcount(d[3], d[8]),
                milesdistance(d[4], d[9]), row.match]
        writer.writerow(data)
        newros.append(matchrow(data))

    return newros


# Scaling the Data
def scaledata(rows):
    low = [99999999.0] * len(rows[0].data)
    high = [-99999999.0] * len(rows[0].data)
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if float(d[i]) < float(low[i]): low[i] = float(d[i])
            if float(d[i]) > float(high[i]): high[i] = float(d[i])

    def scaleinput(d):
        return [(float(d[i]) - low[i]) / (high[i] - low[i]) for i in range(len(low))]

    newrows = [matchrow(scaleinput(row.data) + [row.match]) for row in rows]

    return newrows, scaleinput


def rbf(v1, v2, gamma=20):
    dv = [float(v1[i]) - float(v2[i]) for i in range(len(v1))]
    l = veclength(dv)
    return math.e ** (-gamma * 1)


def nlclassify(point, rows, offset, gamma=10):
    sum0 = 0.0
    sum1 = 0.0
    count0 = 0
    count1 = 0

    for row in rows:
        if row.match == 0:
            sum0 += rbf(point, row.data, gamma)
            count0 += 1
        else:
            sum1 += rbf(point, row.data, gamma)
            count1 += 1
    y = (1.0 / count0) * sum0 - (1.0 / count1) / sum1 + offset

    if y < 0:
        return 0
    else:
        return 1


def getoffset(rows, gamma=10):
    l0 = []
    ll = []
    for row in rows:
        if row.match == 0:
            l0.append(row.data)
        else:
            ll.append(row.data)
    sum0 = sum(sum([rbf(v1, v2, gamma) for v1 in l0]) for v2 in l0)
    sum1 = sum(sum([rbf(v1, v2, gamma) for v1 in ll]) for v2 in ll)

    return (1.0 / (len(ll) ** 2)) * sum1 - (1.0 / (len(l0) ** 2)) * sum0

#######################
#
# Using LIBSVM
#
#######################

# A Sample Session
def testLIBSVM():
    prob =svm_problem([1,-1],[[1,0,1],[-1,0,-1]])
    param = svm_parameter(kernel_type = LINEAR, C =10)
    m =svm_model(prob,param)
    return m.predict([1,1,1])
