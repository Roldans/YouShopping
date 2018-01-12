#encoding:utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'YouShopping.settings'

from difflib import SequenceMatcher
from principal.models import Producto
import csv


# Returns a distance-based similarity score for item1 and item2
def sim_distance(item1, item2):
    distance = 0
    distance = distance + 1/(1+abs(item1.price - item2.price))
    distance = distance + SequenceMatcher(None, item1.name, item2.name).ratio()
    categorias1 = item1.categorias.split(',')
    categorias2 = item2.categorias.split(',')
    eqCat = 0
    for categoria in categorias1:
        if categoria in categorias2:
            eqCat = eqCat + 1/len(categorias1)
    distance = distance + eqCat
        
    return 1 / (1 + distance)


# Number of results and similarity function are optional params.
def topMatches(item, n=5, similarity=sim_distance):
    items = Producto.objects.all()
    scores = [(similarity(item, other), other) for other in items if other != item]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def calculateSimilarItems(n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    items = Producto.objects.all()
    c = 0
    for item in items:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(items))
        # Find the most similar items to this one
        scores = topMatches(item, n=n, similarity=sim_distance)
        result[item] = scores
    print "fin del calculo de la matriz"
    return result

# Metodo llamado al iniciar la app tras el rellenado de la BD
def magicKingsMethod(N):
    # Write similaItemsMatrix
    similarItemsDic = calculateSimilarItems(n=N)
    with open('itemDic.csv','wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for item in similarItemsDic:
            spamwriter.writerow(str(item)+str(similarItemsDic[item]))

def readMatrix():
    return "happy gamero"


def getRecommendedItems(itemMatch):
    #TODO
    return True


def main():
    magicKingsMethod(3)


main()

