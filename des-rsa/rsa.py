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

def generate_prime(start=7000000000000, end=10000000000000):
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

    public_key = {"e": e, "n": n}
    private_key = {"d": d, "n": n}

    return public_key, private_key

def encrypt(M, public_key):
    if not (M >= 0 and M < public_key["n"]):
        raise ValueError(f"Your message in integer form is {M}, which is not in the range [0, n: {public_key['n']})")
    C = pow(M, public_key["e"], public_key["n"])
    return C
def encrypt_private(M, private_key):
    if not (M >= 0 and M < private_key["n"]):
        raise ValueError(f"Your message in integer form is {M}, which is not in the range [0, n: {private_key['n']})")
    C = pow(M, private_key["d"], private_key["n"])
    return C
def decrypt(C, private_key):
    M = pow(C, private_key["d"], private_key["n"])
    return M
def decrypt_public(C, public_key):
    M = pow(C, public_key["e"], public_key["n"])
    return M
def int_to_hex(M):
    M = hex(M)[2:].upper()
    return M

#Example Usage:
if __name__ == "__main__":
    # Generate RSA keys
    public_key, private_key = generate_keys()
    public_key2, private_key2 = generate_keys()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    
    # Encrypt a message
    message = "FFFFFFFFFFFFFFFF"  # Hexadecimal string (can be any hex string)

    encrypted_block = encrypt_private(int(message,16), private_key)
    encrypted_block = encrypt(encrypted_block, public_key2)
    encrypted_block = int_to_hex(encrypted_block)
    print(f"Encrypted Block: {encrypted_block}")

    decrypted_block = decrypt(int(encrypted_block,16), private_key2)
    decrypted_block = decrypt_public(decrypted_block, public_key)
    decrypted_block = int_to_hex(decrypted_block)
    print(f"Decrypted Block: {decrypted_block}")