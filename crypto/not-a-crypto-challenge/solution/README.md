# not-a-crypto-challenge

I couldn't solve this challenge, but here is a writeup anyway. It was 'not a crypto challenge', so
it was clear that it is rather about encodings. I thought that it's just about one simple encoding, but this
proved to be a big mistake on my side... It was actually a chain of simple stuff.

First the braille strings are split on '⠀' to words. Then we use the following mapping to convert
the words to octal numbers (i.e. base 8). This is similar to the actual Braille number representation, but
those are using the top two rows, not the bottom two.


```python
octal_digit = {'⠶': 7, '⠖': 6, '⠢': 5, '⠲': 4, '⠒':3, '⠆': 2, '⠂': 1, '⠴': 0}
```

Once we have base-8 numbers, we convert them to ascii characters and decode it as a base32 encoded string.
The result needs to be decoded as base64, and the output of that is fed into a rot13 decoder which finally returns the flag.

```
input -> [octal numbers encoded as 'braille'] -> [ascii string] -> [base32] -> [base64] -> [rot13] -> flag
```

I'm like  ¯\\_(ツ)_/¯ ... I could have solved the last two steps by looking at the input but I was lost at the beginning.