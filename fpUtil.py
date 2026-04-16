
import random
def extandedEuclideanAlgorithm(a : int,b : int):
    return extended_gcd(a, b)
    
def inverse(a : int,p : int):
    gcd,x,y = extended_gcd(a,p)
    if gcd != 1:
        raise Exception("The inverse does not exist")
    else:
        return x % p
    


def extended_gcd(a, b):
    # Base Case: if a is 0, gcd is b
    # 0*x + b*y = b  => x=0, y=1
    if a == 0:
        return b, 0, 1
    
    # Recursive call
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    # Update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y


def get_prime_factors(n):
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0: # Remove all instances of this factor
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

def find_generator(p: int):
    # The order of the multiplicative group modulo p is p - 1
    group_size = p - 1
    factors = get_prime_factors(group_size)
    
    while True:
        # Pick a random candidate between 2 and p-1
        candidate = random.randrange(2, p)
        is_generator = True

        for factor in factors:
            # Use pow(a, b, c) for (a**b) % c
            if pow(candidate, group_size // factor, p) == 1:
                is_generator = False
                break
        
        if is_generator:
            return candidate
        
    
def is_prime(n):
    # Numbers less than 2 are not prime
    if n < 2:
        return False
        
    count = int(n**0.5) + 1 
    for i in range(2, count):
        if n % i == 0:
            return False
            
    # If no factors were found after the loop, it's prime!
    return True



    


