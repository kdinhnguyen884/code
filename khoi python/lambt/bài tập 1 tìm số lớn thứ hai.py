a = list(map(int, input().split()))
b = max(a)
a = [x for x in a if x != b]
print(max(a))
