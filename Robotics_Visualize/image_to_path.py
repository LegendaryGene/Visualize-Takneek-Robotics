import cv2 as cv
import numpy as np
from collections import deque

path = "Test_n.jpg"
image = cv.imread(path)
image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
image = cv.fastNlMeansDenoisingColored(image, None, 25, 70, 4, 12)
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
_, image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)
i=0 
size = 0
n, m = image.shape
for i in range(n):
    if image[i+2][2] == 0:
        break
    else:
        size = size + 1
grid_rows = n//size
grid_cols = m//size
print(f" Matrix is ({grid_rows} , {grid_cols})")
mat = np.zeros([grid_rows,grid_cols], dtype= np.int32)
x = 0
y = 0
area = size**2

for i in range(0, grid_rows):
    for j in range(0, grid_cols):
        avg = 0
        for k in range(y, min(y+size, n-1)):
            for l in range(x, min(x+size, m-1)):
                avg = avg + image[k][l]
        x = x+size
        avg=avg/area
        if(avg > 100):
            mat[i][j] = 1
        else:
            mat[i][j] = 0
    y = y+size
    x = 0
print("The resulting matrix is: ")
print(mat) # prints the numerical map matrix where 0 is blue cell and 1 is yellow cell

# Path planning using BFS
ans = 0
visited = [[False] * grid_cols for _ in range(grid_rows)]
q = deque([(0, 0, [(0, 0)])])
visited[0][0] = True
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

while q:
    row, col, path = q.popleft()
    if row == grid_rows-1 and col == grid_cols-1:
        ans = path
    for d in directions:
        r = row+d[0]
        c = col+d[1]
        if r<0 or c<0 or r>= grid_rows or c >= grid_cols or mat[r][c] == 0 or visited[r][c]:
            continue

        visited[r][c] = True
        q.append((r,c,path+[(r,c)]))

if ans:
    print(ans)
else:
    print("No path possible")