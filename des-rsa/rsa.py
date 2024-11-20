import math
from math import gcd
import random

# RSA Functions
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime(start=100, end=1000):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num

def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = modular_inverse(e, phi)
    return (e, n), (d, n)

def generate_e(phi_n):
    for i in range(2, phi_n):
        if math.gcd(i, phi_n) == 1:
            return i

def generate_random_e(phi_n):
    e = random.randint(2, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    return e

def encrypt(M, public_key):
    M = int(M, 16)
    if not (M >= 0 and M < public_key["n"]):
        raise ValueError(f"Your message in integer form is {M}, which is not in the range [0, n: {public_key['n']})")
    C = pow(M, public_key["e"], public_key["n"])
    return C

def decrypt(C, private_key):
    M = pow(C, private_key["d"], private_key["n"])
    M = hex(M)[2:].upper().rjust(16, "0")
    return M