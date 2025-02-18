# project euler problem 2
def fibo(n):
    if (n<=1):
        return n
    else:
        return ( fibo(n-1) + fibo(n-2) )
    
sum = 0
four_million = 4000000
num_terms = 50
for i in range(num_terms):
    if (fibo(i) < four_million and fibo(i)%2==0):
        sum += fibo(i)
    if (fibo(i) > four_million):
        break
    else:
        continue
print(sum)
