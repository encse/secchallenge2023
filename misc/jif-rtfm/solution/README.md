# jif.rtfm

The challenge was about the obsolete Gif Plaintext Extension feature. 
You can read about it here https://www.w3.org/Graphics/GIF/spec-gif89a.txt.

Somebody at one point in the past thought that it would be a good idea to encode 
texts in gif files that can be shown by gif players. No sane player supports 
this today, that goes without saying.

The title of the challenge 'jif' was a reference to the message hidden in 
the gif file known as 'BOB89A.GIF'

![BOB89A.GIF](BOB89A.GIF)

```
--------: Introducing GIF89a :--------

When you finish reading this, press   
any key to continue. If you just sit  
back and watch, we'll continue when   
the built-in delay runs out.          
GIF89a provides for "disposing of"  
an image or text. All the text in   
this GIF is "restore to previous",  
so that the underlying image is     
restored when you press a key or    
the delay runs out.                
"Transparent" images or text can be 
written over an underlying image so 
that parts of the old image "show   
through" the new one. 
Oh, incidentally, it's pronounced "JIF"

```

There was an other hint in the file if you extracted it 
with 'strings'.

```
> strings jif.rtfm
...
You are probably too young for this challenge. But you can always rtfm and prove me wrong.
...
```

I looked up the spec and wrote a small python script 
that can extract such messages from .gif files.

The flag was hidden character by character in multiple plaintext blocks.
