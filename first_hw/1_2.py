import random


def sort_by_row(matrix, n):
    for i in range(n-1):
        for row in range(n-1):
            if sum(matrix[row]) > sum(matrix[row + 1]):
                matrix[row], matrix[row+1] = matrix[row+1], matrix[row]
    return matrix


def reverse(matrix, n):
    reversed_matrix = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            reversed_matrix[j].append(matrix[i][j])
    return reversed_matrix


n = int(input())
# create sequence
seq = [x + 1 for x in range(n**2)]
random.shuffle(seq)
# create matrix with numbers from sequence in random order
matrix = [[] for _ in range(n)]
i = 0
for row in range(n):
    matrix[row] = seq[i:n+i]
    i += n

for row in matrix:
    print(*row)
print('\n')

sort_by_row(matrix, n)
matrix_sorted = reverse(sort_by_row(reverse(matrix, n), n), n)
for row in matrix_sorted:
    print(*row)