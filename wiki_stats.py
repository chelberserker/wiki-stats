#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:

            (n, _nlinks) = (map(int, f.readline().split()))
            
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            n_lks = 0 # current number of links
            for i in range(n):
                self._titles.append(f.readline())
                (size, redirect, lks) = (map(int, f.readline().split()))
                self._sizes[i] = size
                self._redirect[i] = redirect
                for j in range(n_lks, n_lks + lks):
                    self._links[j] = int(str(f.readline()))
                n_lks += lks
                if n > 0:
                    self._offset[i+1] = self._offset[i] + lks
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id+1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i] == title:
                return(i)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes(_id)

def analyse_links_from_page(G):
    numlinks_from = list(map(G.get_number_of_links_from, range(G.get_number_of_pages())))
    _max = max(numlinks_from)
    _min = min(numlinks_from)
    mxn = sum(x == _max for x in numlinks_from)
    mnn = sum(x == _min for x in numlinks_from)
    print("Minimal number of links from page:", _min)
    print("Pages with minimal number of links:", mnn)
    print("Maximal number of links from page:", _max)
    print("Pages with maximal number of links:", mxn)
    print("Mean number of links: %0.2f  (st. dev. : %0.2f)" %(statistics.mean(numlinks_from), statistics.stdev(numlinks_from)))




def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    # TODO: нарисовать гистограмму и сохранить в файл


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    print("Number of pages with redirect:", sum(wg._redirect))
    analyse_links_from_page(wg)



    # TODO: статистика и гистограммы
