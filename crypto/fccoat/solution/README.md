# FCCOAT

I really liked this challenge for some reason. Last year we had to use [hashclash](https://github.com/cr-marcstevens/hashclash/) to generate MD5 collisions, and this year was not different. Actually, there are multiple ways to generate a collision and this challenge was about the 'fastest' way of doing it. It turns out that if you are given an arbitrary input, it's possible to extend it with two different suffixes so that the results have the same MD5 signature.

After compilation there is a `hashclash/bin/md5_fastcoll` executable which can be run this way:

```
./hashclash/bin/md5_fastcoll -p somefile.txt
```

We are playing the game of wordle here. We have a list of possible 5 letter
words provided, we pick one of them, put it in a file and generate a collision (two different files). We upload these to the following endpoint: 

```
https://fccoat.secchallenge.crysys.hu/guess
```

The response contains some hints about the word we sent:

```
  '.' - means right place, right character
  '!' - means wrong place, right character
  '-' - means the character is not used
```

Now filter the list of candidates, and try the next one. Continue until the word is found and the flag is returned by the backend.




