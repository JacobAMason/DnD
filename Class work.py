def fib1(n):
    if n in (0,1):
        return n
    else:
        return fib1(n-1)+fib1(n-2)


def fib2(n):
    if n in (0,1):
        return n
    else:
        i,j = 0,1

        while n:
            i,j,n = j, i+j, n-1
        return i


#print(fib1(100))
print(fib2(100))