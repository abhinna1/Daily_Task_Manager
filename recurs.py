def table(num):
    if limit==1:
        return 3
    else:
        return num* times(limit-1)
print(table(3))