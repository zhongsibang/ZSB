a = [1,2,3]
b = [[1,1],[2,2],[3,3]]

c = {}
for i in range(len(a)):
    c[a[i]] =b[i]
print(c)