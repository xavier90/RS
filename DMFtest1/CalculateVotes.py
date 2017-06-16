from PrepareUserLatentFactor import matrixDic
import numpy as np

part_user_matrix = []
non_zero_count = []
# for i in range(6):
#     part_user_matrix.append(matrixDic(i, wholeUsers=True, overlap=False))
#
# percentage = []
# for i in range(6):
#     non_zero_count.append(np.count_nonzero(part_user_matrix[i]))
#
# print non_zero_count

# non_zero_count for 11 users non-overlap
# [1415, 462, 237, 115, 196, 206]
# non_zero_count for 11 users overlap
# [1415, 1877, 2114, 2229, 2425, 2631]
#
# non_zero_count for whole users non-overlap
# [6863, 10313, 24137, 11631, 14237, 10946]
# non_zero_count for whole users overlap
# [6863, 17176, 41313, 52944, 67181, 78127]
# [0.004, 0.011, 0.026, 0.033, 0.042, 0.049]


#check num of rating in each time window
matrix_for_use = []
for i in range(12):
    matrix_for_use.append(matrixDic(i, True, False))

strange_user = 0
for idx in range(943):
    matrix = []
    for i in range(12):
        matrix.append(matrix_for_use[i][idx])

    num_rating = []
    num_rating.append(idx)
    for i in matrix:
        num_rating.append(np.count_nonzero(i))
    if np.count_nonzero(num_rating) == 2:
        strange_user += 1
    print num_rating

print strange_user


# find max num of rating in total
# matrix = matrixDic(5, True, True)
# maxcnt = 0
# for i in matrix:
#     cnt = np.count_nonzero(i)
#     if cnt < 531:
#         maxcnt = max(maxcnt, cnt)
# print maxcnt

# find index of max num of rating
# cnt = 0
# for i in matrix:
#     cnt += 1
#     if np.count_nonzero(i) == 490:
#         print cnt
#         break
