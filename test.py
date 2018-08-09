import numpy as np


from random import randint

# number_of_bins=9
#
# matrix = np.random.rand(3, 4)
# bins = [i*(1.0/number_of_bins) for i in xrange(number_of_bins+1)]
# labels = [(bins[i]+bins[i+1])/2.0 for i in xrange(number_of_bins)]
# labels=list(np.around(np.array(labels),3))
#
# print labels
# print matrix
#
# for i in range(matrix.shape[0]):
#     for j in range(matrix.shape[1]):
#         for _bin in range(len(bins)-1):
#             if matrix[i,j]>=bins[_bin] and matrix[i,j] < bins[_bin+1]:
#                 matrix[i, j]=labels[_bin]
# #
# print matrix

# draw = np.random.choice([1,2], 1, p=[0.5,0.5])
# print draw
next_robot=str(randint(0, 3))

print next_robot=='3'
