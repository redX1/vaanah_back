def fiba(n):
    if n <= 1:
        return 1
    return fiba(n - 2) + fiba(n - 1)
