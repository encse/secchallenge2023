# Archives

The famous Jedi Archives. The whole website has just a single text field, and whatever is wrote there it is just passed in to the URL in a GET query: `https://archives.secchallenge.crysys.hu/?search=apple`. There is no 
visible output, we need to reach out to our Jedi mindtricks.

<img width="497" alt="image" src="https://user-images.githubusercontent.com/6275775/231849498-aca5eb41-71a8-4e18-a102-1c25264a991c.png">

Not this time, but it is something similar: blind NOSQL injection. I did my homework and
learned about two things. First, regexps like `/(.+)+D/` can be really slow in JavaScript.

```bash
> time node -e '/(.*)*D/.test("AAAAAAAAAAAAAAAAAAAAAAD")'
node -e '/(.*)*D/.test("AAAAAAAAAAAAAAAAAAAAAAD")'  0.02s user 0.04s system 35% cpu 0.162 total

> time node -e '/(.*)*D/.test("AAAAAAAAAAAAAAAAAAAAAAA")'
node -e '/(.*)*D/.test("AAAAAAAAAAAAAAAAAAAAAAA")'  0.97s user 0.03s system 92% cpu 1.072 total
```

It depends on wether the match succeeds. It's OK if the string ends with a D, but if there is no 
match, the combinatoric explosion slows it down tremendously. In general regexps with `(.*)*` 
in them are considered evil.

Second. Some NOSQL frameworks expect regexp arguments in the URL like this: `https://archives.secchallenge.crysys.hu/?search[$regex]=foobar`

Putting them together we can start looking for the flag character by character. This is slow:

`https://archives.secchallenge.crysys.hu/?search[$regex]=cd23(.*)*QQQQ`

But this is fast:

`https://archives.secchallenge.crysys.hu/?search[$regex]=cd24(.*)*QQQQ`

You get the idea. Whenever the prefix is correct, the query runs slowly, and it's much faster if the prefix 
is wrong. Just what we need. We can write a Python script that finds the flag character by character...

<img width="770" alt="image" src="https://user-images.githubusercontent.com/6275775/231848484-d2147ce1-548e-435e-af68-509a54116ccf.png">
