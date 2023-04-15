# Unfriendly Agreement

I'm not a cryptographer and never studied elliptic curves formally, so whatever you read here is probably wrong. But the lack of knowledge cannot be an issue when facing these introductory challenges. I was sure that if I find the right paper, I'll be able to solve it.

Elliptic curves are a family of curves caracterized by the y<sup>2</sup> = x<sup>3</sup> + ax + b equation for different `a` and `b` parameters. If we plot the points of such an implicit equation we see something like this:

<img src="https://user-images.githubusercontent.com/6275775/232182729-cda263e6-6e9d-44e6-b66b-0e51c1869605.png" width="600">

There is an algebra defined for two points of the curve: we can add them together in `A + B = C` fashion, where all three variables are points `(x, y)` and satisfy the corresponding elliptic curve's equation. Similarly we can multiply a point by an integer and get an other point of the curve like `P = k * Q`. We cannot multiply or divide points with each other.

We can pick a point 'G' on the curve and call it a *generator point* and get nice *group* of points by multiplying `G` with different numbers `{nG | n ∈ ℤ}`; the number of elements in the group is called the *order*. I will not emphasize below but when we are talking about numbers as the multipliers of G I always mean modulo the order of the group. All computations that result a number are meant to be `% order`.

What makes this useful for cryptography is that if we agree on the curve and the generator point `G` and I pick some random `k` and a corresponding point `P = kG`, I can tell you `P` and can be sure that there is no computably feasible way for you determine my `k` anymore. At least this is true if we have the right curve, the right G and `k` is a big enough random number. So we can build an asymetric key protocol over this thing.

## Preliminary steps

After lot of searching I found this [page](https://gist.github.com/AdamISZ/d8ed3df3f540d06980e3d65b4aef70bc#2-of-2-schnorr-without-adaptor-sig
) which summarizes the protocol we need to use here.

The idea is that Alice and Bob want to co-sign two messages M<sub>1</sub> and M<sub>2</sub>, i.e. both of them needs to sign both messages, and they want to exchange some secret as soon as this happens. This takes multiple steps and it can happen that one party stops cooperating. In this case the secret should be held and the other party cannot complete the protocol either.

The steps are the following. They agree on a curve, G and some other details such as a Hash function `H`, how to encode strings etc.

I'll use small letters for secrets (or integers) and capitals (or points of the curve) for public things. I'll use `w` to mean A or B.

Both parties select a persistent key x<sub>w</sub>, X<sub>w</sub> and temporal keys for both messages r<sub>w,i</sub>, R<sub>w,i</sub> where i ∈ {1, 2}. This is 6 keys already and we haven't even started...

The so called public things are revealed to the other party only at some point of the protocol, but we are not interested in the exact mechanics now. We suppose it is public from the beginning.

They know the messages as well in advance.

Now A selects an other pair of `o,O` this is called the *offset*. She also makes `O` public, but keeps `o` secret. This will be the final *secret* which will be revealed when both messages are signed by both of them. 

Here comes the hash function into the picture. `H` takes a bit sequence and generates an integer. They need to agree on how to serialize keys and combine bit sequences which I'll mark with || meanining that they just put the bits after each other.
Both A and B can compute H(X<sub>A</sub> || X<sub>B</sub>), there is no secret here. They can also compute: H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) for both `w`. 

Start from X<sub>w</sub> = x<sub>w</sub> * G they calculate this:

X<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) = x<sub>w</sub> * H(H(X<sub>A</sub> || X<sub>B</sub>) || X<sub>w</sub>) * G  

let's call this:

(1) X'<sub>w</sub> = x'<sub>w</sub> * G 

Again, capital means *public* and the other party can compute it on its own knowing the previously published  information. They know each others' X'<sub>w</sub> but not x'<sub>w</sub>. 

The sum of this will be called the temporal common public key, which I'll mark with `JK`:

JK = X'<sub>A</sub> + X'<sub>B</sub> 

For any integer m (or message) they can also compute:

(2) e(m) = H(JK || R<sub>A</sub> + R<sub>B</sub> || m)

That's a lot of information to consume let's take a break.

<img src="https://user-images.githubusercontent.com/6275775/232190405-3688161d-c09e-45c2-8369-6ea2ab6dcb18.png" width="600">


## The signing process 

We can finally start signing some messages. Alice starts with m<sub>1</sub>:

S<sub>A,1</sub> = r<sub>A,1</sub> + o + e(m<sub>1</sub>)x'<sub>A</sub>

S<sub>A,1</sub> is the signature, it is number (not point) that is made public (hence capital).

Bob can check that this really originates from Alice. The below equations look frightening, but you only need to remember that our notation is set up so that 'lowercase becomes uppercase when multiplied by G':

S<sub>A,1</sub> * G = 

(r<sub>A,1</sub> + o + e(m<sub>1</sub>)x'<sub>A</sub>) * G = 

r<sub>A,1</sub>G + oG + e(m<sub>1</sub>)x'<sub>A</sub> * G = 

R<sub>A,1</sub> + O + e(m<sub>1</sub>) * X'<sub>A</sub>

Everything in the last line is common knowledge. If A is not rouge, B can check that: 

S<sub>A,1</sub> * G = R<sub>A,1</sub> + O + e(m<sub>1</sub>) * X'<sub>A</sub> 

As you work on the solution you should add asserts like this to the code you are writing to see that you are on track.

Once Bob is satisfied with Alice's signature he generates his part:

S<sub>B,1</sub> = r<sub>B,1</sub>  + e(m<sub>1</sub>)x'<sub>B</sub>.

He doesn't have an offset, so it is not added to r<sub>B,1</sub>, but Alice can still check that it comes from Bob the same way as above:

S<sub>B,1</sub> * G =  ... = R<sub>B,1</sub>  + e(m<sub>1</sub>)X'<sub>B</sub>

Alice is happy, so she signs the second message, and B answers:

S<sub>A,2</sub> = r<sub>A,2</sub> + o + e(m<sub>2</sub>)x'<sub>A</sub>

S<sub>B,2</sub> = r<sub>B,2</sub> + e(m<sub>2</sub>)x'<sub>B</sub>

A has all the information, but she still needs to compute the final signatures (C for common):

S<sub>C,1</sub> = S<sub>A,1</sub> + S<sub>B,1</sub> - o

S<sub>C,2</sub> = S<sub>A,2</sub> + S<sub>B,2</sub> - o

Once she publishes one of these, B can compute `o` as well, revealing the final secret:

o = S<sub>A,1</sub> + S<sub>B,1</sub> - S<sub>C,1</sub>
 
or

o = S<sub>A,2</sub> + S<sub>B,2</sub>  - S<sub>C,2</sub>

That's all the math we need for the challenge.

## Solving the challenge

After all of this preparation we can solve quite easily. First we compute S<sub>B,1</sub> and S<sub>B,2</sub>:

S<sub>B,1</sub> = r<sub>B,1</sub>  + e(m<sub>1</sub>)x'<sub>B</sub>

S<sub>B,2</sub> = r<sub>B,2</sub>  + e(m<sub>2</sub>)x'<sub>B</sub>

we need to compute e and x'<sub>B</sub> as well, but we have everything for these, see (1) and (2) above.

Next, using the final signature of the first message, we can work backwards and compute o:

o = S<sub>A,1</sub> + S<sub>B,1</sub> - S<sub>C,1</sub>

And finally determine S<sub>C,2</sub> with:

S<sub>C,2</sub> = S<sub>A,2</sub> + S<sub>B,2</sub> - o

The flag is this number wrapped in the usual `cd23{...}` thing.

