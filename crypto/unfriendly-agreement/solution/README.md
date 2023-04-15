# Unfriendly Agreement

I'm not a cryptographer and never studied elliptic curves formally, so whatever you read here is probably wrong. But the lack of knowledge cannot be an issue when facing these introductory challenges. I was sure that if I find the right paper, I'll be able to solve it.

Elliptic curves are a family of curves characterized by the y<sup>2</sup> = x<sup>3</sup> + ax + b equation for different `a` and `b` parameters. If we plot the points of such an implicit equation we see something like this:

<img src="https://user-images.githubusercontent.com/6275775/232182729-cda263e6-6e9d-44e6-b66b-0e51c1869605.png" width="600">

There is an algebra defined for two points of the curve: we can add them together in `A + B = C` fashion, where all three variables are points `(x, y)` and satisfy the corresponding elliptic curve's equation. Similarly we can multiply a point by an integer and get an other point of the curve like `P = k * Q`. We cannot multiply or divide points with each other. (The operations are not the usual coordinatewise operations but something special.)

We can pick a point 'G' on the curve and call it a *generator point* and get nice *group* of points by multiplying `G` with different numbers `{nG | n ∈ ℤ}`; the number of elements in the group is called the *order*. I will not emphasize below but when we are talking about numbers as the multipliers of G I always mean modulo the order of the group. All computations that result a number are meant to be `% order`.

What makes this useful for cryptography is that if we agree on the curve and the generator point `G` and I pick some random `k` and a corresponding point `P = kG`, I can tell you `P` and can be sure that there is no computably feasible way for you determine my `k` anymore. At least this is true if we have the right curve, the right G and `k` is a big enough random number. So we can build an asymetric key protocol over this thing.

## Preliminary steps

After lot of searching I found this [page](https://gist.github.com/AdamISZ/d8ed3df3f540d06980e3d65b4aef70bc#2-of-2-schnorr-without-adaptor-sig
) which summarizes the protocol we need to use here. It is slightly different from what's going on here, so it's better to follow my writeup. I'll work with the challenge's notation. The idea is that Alice and Bob needs to co-sign two messages M<sub>1</sub> and M<sub>2</sub>. Both of them needs to sign both messages, and they want to exchange some secret as soon as this happens. This takes multiple steps and it can happen that one party stops co-operating. In this case the secret should be held and the other party shouldn't be able to finish the protocol either.

I'll use small letters for secrets and capitals for public things. I'll use `w` to mean A or B.

Alice and Bob agree on a curve, G and some other details such as a Hash function `H`, how to encode strings etc. Both parties select a persistent key x<sub>w</sub>, X<sub>w</sub> and temporal keys for both messages r<sub>w,1</sub>, R<sub>w,1</sub> and r<sub>w,2</sub>, R<sub>w,2</sub>. Alice also selects an other pair of o, O this is called the *offset*. She makes O public, but keeps o for herself. This will be the final *secret* which will be revealed when both messages are signed by both of them. This is 7 keys already and we haven't even started...

Here comes the hash function into the picture. The function H takes a bit sequence and generates an integer. They need to agree on how to serialize keys and combine bit sequences which I'll just write as || without going into the specifics.

Using public information both Alice and Bob can compute H(X<sub>A</sub> || X<sub>B</sub>), there is no secret here. They can also compute: H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) for both w. This doesn't make much sense now, but they can definitely do it. Even more if they start from their own X<sub>w</sub> = x<sub>w</sub> * G they can calculate:

X<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) = x<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) * G  

We should give names to these:

(1) X'<sub>w</sub> := X<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) 

(2) x'<sub>w</sub> := x<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) * G

They don't know each other's x'<sub>w</sub>, but they can compute the corresponding X'<sub>w</sub> from the public X<sub>w</sub>. The sum of X'<sub>A</sub> and X'<sub>B</sub> will be called the temporal common public key, which I'll write with JK. They can determine this from public information.

JK = X'<sub>A</sub> + X'<sub>B</sub> 

For any integer M (or message) they can also compute:

(3) e<sub>i</sub>(M) = H(JK || R<sub>A,i</sub> + R<sub>B,i</sub> || M)

That's a lot of information to consume let's take a break.

<img src="https://user-images.githubusercontent.com/6275775/232190405-3688161d-c09e-45c2-8369-6ea2ab6dcb18.png" width="600">


## The signing process 

We can finally start signing some messages. Alice starts with M<sub>1</sub>:

S<sub>A,1</sub> = r<sub>A,1</sub> + o + e<sub>1</sub>(M<sub>1</sub>)x'<sub>A</sub>

S<sub>A,1</sub> is the signature, it is number (not point) that is made public (hence capital).

Bob can check that this really originates from Alice. The below equations look frightening, but you only need to remember that our notation is set up so that 'lowercase becomes uppercase when multiplied by G':

S<sub>A,1</sub> * G = 

(r<sub>A,1</sub> + o + e<sub>1</sub>(M<sub>1</sub>)x'<sub>A</sub>) * G = 

r<sub>A,1</sub>G + oG + e<sub>1</sub>(M<sub>1</sub>)x'<sub>A</sub> * G = 

R<sub>A,1</sub> + O + e<sub>1</sub>(M<sub>1</sub>) * X'<sub>A</sub>

Everything in the last line is common knowledge. If A is not rouge, B can check that: 

S<sub>A,1</sub> * G = R<sub>A,1</sub> + O + e<sub>1</sub>(M<sub>1</sub>) * X'<sub>A</sub> 

As you work on the solution you should add asserts like this to the code you are writing to see that you are on track.

Once Bob is satisfied with Alice's signature he generates his part:

S<sub>B,1</sub> = r<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)x'<sub>B</sub>.

He doesn't have an offset, so it is not added to r<sub>B,1</sub>, but Alice can still check that it comes from Bob the same way as above:

S<sub>B,1</sub> * G =  ... = R<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)X'<sub>B</sub>

Alice is happy, so she signs the second message, and B answers:

S<sub>A,2</sub> = r<sub>A,2</sub> + o + e<sub>2</sub>(M<sub>2</sub>)x'<sub>A</sub>

S<sub>B,2</sub> = r<sub>B,2</sub> + e<sub>2</sub>(M<sub>2</sub>)x'<sub>B</sub>

Alice now has everything, but she still needs to compute and publish the final signatures (C for common):

S<sub>C,1</sub> = S<sub>A,1</sub> + S<sub>B,1</sub> - o

S<sub>C,2</sub> = S<sub>A,2</sub> + S<sub>B,2</sub> - o

Once she publishes one of these, B can compute o as well, revealing the final secret:

o = S<sub>A,1</sub> + S<sub>B,1</sub> - S<sub>C,1</sub>
 
or from the other message:

o = S<sub>A,2</sub> + S<sub>B,2</sub>  - S<sub>C,2</sub>

That's all the math we need for the challenge.

## Solving the challenge

After all of this preparation we can solve it quite easily. First we compute S<sub>B,1</sub> and S<sub>B,2</sub>:

S<sub>B,1</sub> = r<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)x'<sub>B</sub>

S<sub>B,2</sub> = r<sub>B,2</sub>  + e<sub>2</sub>(M<sub>2</sub>)x'<sub>B</sub>

we need to compute e and x'<sub>B</sub> as well, but we have everything for these, see (1) (2) and (3) above.

Next, using the final signature of the first message, we can work backwards and compute o:

o = S<sub>A,1</sub> + S<sub>B,1</sub> - S<sub>C,1</sub>

And finally determine S<sub>C,2</sub> with:

S<sub>C,2</sub> = S<sub>A,2</sub> + S<sub>B,2</sub> - o

The flag is this number S<sub>C,2</sub> wrapped in the usual `cd23{...}` format.

## Appendix

I cannot stop without sheding some light on why we need this complicated e and JK. The idea is that once Alice publishes 
the final signature(s) we should be able to check that she really follows the rules and not trying to trick us. This is because:

S<sub>C,1</sub> * G = 

from the definition of S<sub>C,1</sub>:

= (S<sub>A,1</sub> + S<sub>B,1</sub> - o) * G = 

using the definition of S<sub>A,1</sub> and S<sub>B,1</sub>:

= (r<sub>A,1</sub> + o + e<sub>1</sub>(M<sub>1</sub>) * x'<sub>A</sub>) * G + (r<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)x'<sub>B</sub>) * G + o*G =

multiply by G:

= R<sub>A,1</sub> + O + e<sub>1</sub>(M<sub>1</sub>) * X'<sub>A</sub> + R<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)X'<sub>B</sub> - O =

O fells out:

= R<sub>A,1</sub> + e<sub>1</sub>(M<sub>1</sub>) * X'<sub>A</sub> + R<sub>B,1</sub>  + e<sub>1</sub>(M<sub>1</sub>)X'<sub>B</sub> =

reorder:

= R<sub>A,1</sub> + R<sub>B,1</sub> + e<sub>1</sub>(M<sub>1</sub>) * (X'<sub>A</sub> + X'<sub>B</sub>) =

use the definition of JK:

= R<sub>A,1</sub> + R<sub>B,1</sub> + e<sub>1</sub>(M<sub>1</sub>) * JK =

from the definition of e<sub>1</sub>:

= R<sub>A,1</sub> + R<sub>B,1</sub> +  H(JK || R<sub>A,1</sub> + R<sub>B,1</sub> || M<sub>1</sub>) * JK

We can calculate this from public information without S<sub>C,1</sub>. And once we get S<sub>C,1</sub> from Alice
we just multiply it with G and check if the equation holds.









