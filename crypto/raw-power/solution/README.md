# raw power

Raw power was really an introductory challenge. I took all printable characters in Python with:

```
import itertools

printable = string.printable:
```

I generated all possible ten long binary strings with:
```
import itertools

digits = "01"
combinations = list(itertools.product(digits, repeat=10))
```

To compute the hashes we need:

```
import hashlib 

hashlib.md5(key).hexdigest()
hashlib.sha1(key).hexdigest()
hashlib.sha256(key).hexdigest()
hashlib.sha512(key).hexdigest()
```

The rest is just combining these Lego bricks. It's against the rules to provide a runnable script, so you have to do it on your own.
