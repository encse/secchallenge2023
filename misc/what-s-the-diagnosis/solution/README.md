# What's the diagnosis?

I couldn't solve this challenge on my own, but got some extra spoliers after the contest. The first step was clear:
we need to do something with the wifi password that seems to start with `00`.

I took `hospital_wifi.cap` and converted to a format that can be fed into `hashcat` with:

```
hcxpcapngtool -o hash.hc22000 hospital_wifi.cap
```

The output is `hash.hc22000`, we can invoke hashcat with:

```
hashcat -1 '?d?l' -a 3 hash.hc22000  '00?1?1?1?1?1?1'
```

This means:

|Param            | Desription                                                 |
| --------------- | ---------------------------------------------------------- |
| -1 '?d?l'       | set the first  charset (1) to digits and lowercase letters |
| -a 3            | attack mode = brute force                                  |
| hash.hc22000    | the file with our hash                                     |
| 00?1?1?1?1?1?1  | password format; ?1 means 'use the first charset'          |


this would have taken too much time in my MackBook Air which doesn't have an
active cooling. So I asked for more help, then one of the organizers told me that the
third letter is 'r'. Meanwhile I set up a GPU instance on AWS and could bruteforce the
remaining 5 characters in a few minutes.

## Stage 2

If we open `hospital.pcapng` in Wireshark we can find lots of encrypted packages in various 
protocols, most of them is TLS or Quic, but there is a third category called 'Radius'. We can use Wireshark
to decrypt these messages. In Preferences / Protocols / RADIUS there is an 
option to set the 'shared secret':

<img width="686" alt="image" src="https://user-images.githubusercontent.com/6275775/234602053-1a260169-cb61-4e63-b0f1-02e6cef0b7c8.png">

Set the WIFI password here.  We know from the task description that the doctors used the 
same password everywhere, so this seems to be the next logical step.


This is how a packet looks before:

<img width="586" alt="image" src="https://user-images.githubusercontent.com/6275775/234603121-36b0459e-f327-4233-a245-4d6fe79124a8.png">

and after:

<img width="999" alt="image" src="https://user-images.githubusercontent.com/6275775/234603494-acf1c4d6-c4ee-4df2-94e8-e543e89cd7c8.png">

the 'User-Password' field became readable. It looks like some base64 encoded string. Surely enough
if we collect all strings (there are about 40) all of them are similar, but one string starts with 
`data:image/png;base64,iVBORw0KG` and one of them is `z/+9R////2X77v/BQAA//+FFIs4e5KCfQAAAABJRU5ErkJggg==`;
We can be fairly sure that it's just one big image sliced up.

The usernames are all scientists like Hippocrates, AlbertSzentGyorgyi etc. I ordered the list on the year 
they were born and suddenly the base64 string started to make sense. I
just concatenated it and opened in the browser. It was a QR code, maybe the flag? But I was rickrolled the
1000th times during the challenge.... 

I was close to giving up because this seemd like a dead end, albeit a lot of work went into it. I tried
binwalk, strings, zstego on the image but nothing helped. I checked the other packages in the capture files
hoping for some hints, but I couldn't find anything. A week later I talked to Pepe who said that
`zstego` was the necessary tool. But I remembered trying it before... At the end it has turned out that
my zstego version was too old (from last year) and it was throwing and exception for this particular image.
After installing the latest version it could find the flag which is somehow hidden in the palette of the image.

This has been a real 'misc' challenge with some WTF on the top :D
