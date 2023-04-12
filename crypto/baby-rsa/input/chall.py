from Crypto.Util.number import getPrime, getRandomInteger
from math import lcm, gcd
from flag import FLAG


p = getPrime(1024)
q = getPrime(1024)

n = p * q
print(f"n = {n}")

phi = lcm(p-1, q-1)

e1 = getRandomInteger(42)
while gcd(e1, phi) != 1:
    e1 = getRandomInteger(42)
print(f"e1 = {e1}")

e2 = getRandomInteger(42)
while gcd(e1, e2, phi) != 1:
    e2 = getRandomInteger(42)
print(f"e2 = {e2}")

flag_int = int.from_bytes(FLAG.encode(), 'big')

c1 = pow(flag_int, e1, n)
print(f"c1 = {c1}")

c2 = pow(flag_int, e2, n)
print(f"c2 = {c2}")
