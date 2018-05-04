import numpy as np
import xlrd
import csv

def inxlsx():
    f = xlrd.open_workbook('/Users/wlt/Desktop/gaout.xlsx')
    sheet1 = f.sheet_by_index(0)
    sheet1 = f.sheet_by_name('Sheet1')
    Pdots = list(zip(sheet1.col_values(0), sheet1.col_values(1)))[:500]
    Pferris = list(zip(sheet1.col_values(2), sheet1.col_values(3)))[:500]
    Pdragon = list(zip(sheet1.col_values(4), sheet1.col_values(5)))[:500]
    Plantern = list(zip(sheet1.col_values(6), sheet1.col_values(7)))[:500]
    PdotsEnd = list(zip(sheet1.col_values(8), sheet1.col_values(9)))[:500]
    return Pdots, Pferris, Pdragon, Plantern, PdotsEnd

def outcsv(pos):
    with open('/Users/wlt/Desktop/layer.csv', 'w') as f:
        writer = csv.writer(f)
        for point in pos:
            writer.writerow(point)

def modify(pos, crashDist):
    is_modified = False
    for i in range(1, pos.shape[0]):
        for j in range(i+1, pos.shape[0]):
            line = (pos[i] - pos[j])
            if (line[0]**2 + line[1]**2) < crashDist**2 and line[2] == 0:
                is_modified = True
                pos[j, 2] += 1
    return pos, is_modified

def move(posI, posF, crashDist=0.3, t=100):
    dPath = (posF - posI) / t
    pos = posI.copy()
    positions = []
    for i in range(1, t + 1):
        pos += dPath
        is_modified = True
        while is_modified:
            is_modified = True
            pos, is_modified = modify(pos, crashDist)
    return pos

if __name__ == '__main__':
    Pdots, Pferris, Pdragon, Plantern, PdotsEnd = inxlsx()
    layer = np.zeros((500, 1))
    
    Pdots = np.append(Pdots, layer, axis=1)
    Pferris = np.append(Pferris, layer, axis=1)
    Pdragon = np.append(Pdragon, layer, axis=1)
    Plantern = np.append(Plantern, layer, axis=1)
    PdotsEnd = np.append(PdotsEnd, layer, axis=1)

    pos1 = move(Pdots, Pferris)
    print('1')
    pos2 = move(Pferris, Pdragon)
    print('2')
    pos3 = move(Pdragon, Plantern)
    print('3')
    pos4 = move(Pdots, Pferris)
    print('4')

    outcsv(np.hstack((pos1, pos2, pos3, pos4, pos5)))
