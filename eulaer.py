from typing import Dict
from fpUtil import get_prime_factors

def eulaer(d: dict):
    # The totient function is multiplicative, so start with 1
    res = 1

    for p, k in d.items():
        calc = (p ** (k - 1)) * (p - 1)
        res *= calc
    
    return res

if __name__ == '__main__':
    number_to_factor = 804
    
    # We retrieve the raw list like [2, 2, 3, 67]
    factors_list = get_prime_factors(number_to_factor)
    
    # Convert list to dict of counts {2: 2, 3: 1, 67: 1}
    factors = {}
    for f in factors_list:
        factors[f] = factors.get(f, 0) + 1

    print(eulaer(factors))
    
    

