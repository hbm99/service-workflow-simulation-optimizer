from typing import List
import numpy as np
import matplotlib.pyplot as plt
from itertools import count

from environment import Cashier, Cell, Product, Section

CONVERSION_DICT = {Cell: 0 , Section: 1, Cashier: 2}

a = np.array([[ 0 ,  0 , 'g', 'g', 'g'], 
              [ 0 ,  0 ,  0 , 'g', 'g'],
              ['d',  0 ,  0 ,  0 , 'g'], 
              ['d', 'd',  0 ,  0 , 'g'], 
              ['d', 'd', 'd', 'd', 'g']], dtype=object)

# we want to build a dictionary mapping objects to integers
seq2 = count(2) # we don't know in advance how many different objects we'll see
d = {0:0, 1:1}  # but we know that the integers are either 0 or 1
for o in a.flatten():  
    if o not in d: d[o] = next(seq2)

# with the help of the dictionary, here it is a plottable matrix
b = np.array([d[x] for x in a.flatten()]).reshape(a.shape)

N = len(d)
# to avoid a continuous colorbar, we sample the needed colors
cmap = plt.cm.get_cmap('viridis', N) 

# eventually,
# we can plot the matrix, the colorbar and fix the colorbar labelling
plt.imshow(b, cmap=cmap)
cb = plt.colorbar(drawedges=True)
dc = (N-1)/N
cb.set_ticks([dc*(n+1/2) for n in range(N)])
cb.set_ticklabels([v for k, v in sorted((v,k) for k,v in d.items())])

# plt.show()

def pretty_printing(map: List[List[Cell]]):
    new_map = convert_to_np_array(map)
    
    #new_map = new_map.reshape(a.shape)
    
    N = len(CONVERSION_DICT)
    # to avoid a continuous colorbar, we sample the needed colors
    cmap = plt.cm.get_cmap('viridis', N) 

    # eventually,
    # we can plot the matrix, the colorbar and fix the colorbar labelling
    plt.imshow(new_map, cmap=cmap)
    cb = plt.colorbar(drawedges=True)
    dc = (N-1)/N
    cb.set_ticks([dc*(n+1/2) for n in range(N)])
    cb.set_ticklabels([v for k, v in sorted((v,k) for k,v in CONVERSION_DICT.items())])

    plt.show()

def convert_to_np_array(map: List[List[Cell]]):
    new_map = [None] * len(map)
    for i in range(len(map)):
        new_map[i] = [None] * len(map[i])
    for i in range(len(map)):
        for j in range(len(map[i])):
            new_map[i][j] = CONVERSION_DICT[type(map[i][j])]
    return np.array(new_map, dtype=object)
    
a = [[Cell(), Cashier(), Cell()],
     [Cell(), Cell(), Cell()],
     [Cell(), Section(Product('Pizza', 1), 0), Cell()]]
pretty_printing(a)