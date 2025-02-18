# simple program to print the Fibonacci sequence
# f(0) = 0
# f(1) = 1
# f(2) = f(1) + f(0)
# f(n) = f(n-1) + f(n-2)
# 0 1 1 2 3 5 8....
def fibo(n):
    if (n<=1):
        return n
    else:
        return ( fibo(n-1) + fibo(n-2) )
    
num_terms = int(input("Enter how many terms in Fibonacci sequence do you want? "))
for i in range(num_terms):
    print(fibo(i), end=' ')