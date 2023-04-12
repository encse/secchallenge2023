# Baby RSA

This challenge demonstrates a basic vulnerability of RSA. If we look at the input we can immediately notice that the same plaintext message `m` was encrypted with two different exponents `e1` and `e2` which are relative primes:

```
e1 = getRandomInteger(42)
while gcd(e1, phi) != 1:
    e1 = getRandomInteger(42)

print(f"e1 = {e1}")

e2 = getRandomInteger(42)
while gcd(e1, e2, phi) != 1:
    e2 = getRandomInteger(42)

print(f"e2 = {e2}")
```

The ciphertexts `c1` and `c2` are simply `m ^ e1 (mod n)` and `m ^ e2 (mod n)`.

Since the two expontents are relative primes we can use the extended euclidean algorithm to compute `a` and `b` such that `a * e1 + b * e2 = 1`.  This is a well known property of `gcd`.

Using this, we can easily determine the orginal message:

```
c1 ^ a * c2 ^ b = 
(m ^ e1) ^ a * (m ^ e2) ^ b =
m ^ (a * e1 + b * e2) =
m ^ 1 = 
m (mod n)
```

You can use `pow(x,y,n)` to calculate `c1 ^ a * c2 ^ b` in python. The result is a big integer, which needs to be converted to characters with:

```
flag = m.to_bytes((m.bit_length() + 7) // 8, "big")

print(flag)
```
