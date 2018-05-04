import os
import random
import numpy as np
import csv
import xlrd
import matplotlib.pyplot as plt

def inxlsx():
    f = xlrd.open_workbook('/Users/wlt/Desktop/final.xlsx')
    sheet1 = f.sheet_by_index(0)
    sheet1 = f.sheet_by_name('Sheet1')
    Pdots = list(zip(sheet1.col_values(0), sheet1.col_values(1)))
    Pferris = list(zip(sheet1.col_values(2), sheet1.col_values(3)))
    Pdragon = list(zip(sheet1.col_values(4), sheet1.col_values(5)))
    Plantern = list(zip(sheet1.col_values(6), sheet1.col_values(7)))
    return Pdots, Pferris, Pdragon, Plantern

def outcsv(Ps):
    with open('/Users/wlt/Desktop/out.csv', 'w') as f:
        writer = csv.writer(f)
        for point in Ps:
            writer.writerow(point)

def transp(way, P2):
    Pnew = []
    for index in way[0:-1]:
        x2, y2 = P2[int(index)]
        Pnew.append((x2, y2))
    return Pnew

def generate(n): # generate random ways for arrangements
    way = list(range(n))
    random.shuffle(way)
    way.append(0) # place for fitness value
    return way

def fitness(way, P1, P2): # fitness function
    dist = 0
    for i in range(len(way)-1):
        x1, y1 = P1[i]
        x2, y2 = P2[int(way[i])]
        dist += ((x1-x2)**2 + (y1-y2)**2) ** 0.5
    return 1 / dist

def dist(way, P1, P2): # return the distance of the way
    return 1 / fitness(way, P1, P2)

def rank(arrs, P1, P2, m, n): # rank rows in arrangements
    for i in range(m):
        arrs[i, n] = fitness(arrs[i], P1, P2)
    arg = arrs[:, n].argsort()
    arrs = arrs[list(reversed(arg))]
    return arrs

def rand(arrs, m, n): # all genes mutated
    for i in range(m):
        if i < int(0.1 * m): continue
        random.shuffle(arrs[i])
    return arrs

def asexual(arrs, e, c, m, n): # asexual reproduction
    for i in range(m):
        if i <= int(e * m): continue
        arrs[i] = arrs[random.randint(0, int(e * m))].copy()
        for j in range(int(c * n)):
            a, b = [random.randint(0, n-1) for k in range(2)]
            arrs[i, a], arrs[i, b] = arrs[i, b], arrs[i, a]
    return arrs

def select(arrs, P1, P2, e, c, g, m, n): # select using loops
    index, distance = [], []
    for i in range(g):
        arrs = rank(arrs, P1, P2, m, n)
        arrs = asexual(arrs, e, c, m, n)
        index.append(i)
        distance.append(dist(arrs[0], P1, P2))
    return arrs, index, distance

def findway(P1, P2, e, c, g, m, n):
    arrs = np.array([generate(n) for i in range(m)], dtype=float)
    print(dist(list(range(n+1)), P1, P2))
    arrs, index, distance = select(arrs, P1, P2, e, c, g, m, n)
    Pnew = transp(arrs[0], P2)
##    print(dist(arrs[0], P1, P2))
##    print()
    return distance[-1] # best distance

def plot(i, d, name):
    plt.figure()
    plt.plot(i, d)
    plt.xlabel('Number of iterations')
    plt.ylabel('Total distance')
    plt.title(name)
    plt.show()

if __name__ == '__main__':
    e = 0.01
    c = 0.005
    g = 300
    m = 50
    n = 500
    Pdots, Pferris, Pdragon, Plantern = inxlsx()

##    print("""\
##Genetic Algorithm with parameters:
##{0} % elites
##{1} % changes
##{2} generations
##{3} individuals * {4} genes population
##    """.format(e * 100, c * 100, g, m, n))

    l, dists = [], []
    for m in [10, 20, 40, 80, 160, 320, 640, 1280]:
        dists.append(findway(Pdots, Pferris, e, c, g, m, n))
        l.append(m)
    plt.plot(l, dists)
    plt.xlabel("Number of Individuals")
    plt.ylabel("Distance")
    plt.title("Distance - Individual Graph")
    plt.xscale('log')
    plt.show()

##    Pdragon, i2, d2 = findway(Pferris, Pdragon, e, c, g, m, n)
##    Plantern, i3, d3 = findway(Pdragon, Plantern, e, c, g, m, n)
##    PdotsEnd, i4, d4 = findway(Plantern, Pdots, e, c, g, m, n)
##
##    Ps = zip(Pdots, Pferris, Pdragon, Plantern, PdotsEnd)
##    outcsv([p1 + p2 + p3 + p4 + p5 for (p1, p2, p3, p4, p5) in Ps])
##
##    os.system("say 'Finished all.'")
##    plot(i1, d1, 'Dots to Ferris')
##    plot(i2, d2, 'Ferris to Dragon')
##    plot(i3, d3, 'Dragon to Lantern')
##    plot(i4, d4, 'Lantern to Dots')
