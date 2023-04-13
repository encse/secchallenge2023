# A Jim Brown and an Ella Fitzgerald

Let's register a user and log in. We find a profile page with our account balance, 
username and a field that we can use to store any secret "which is perfectly safe" for ourselves. 
There is a password management page, a money transfer page and a logout option.

The goal is to steal Terry Benedict's account. First his user id can be found by simply transfering $1 to each account starting from 1. 
Soon after we reach user id 12 and get this message:

<img width="488" alt="image" src="https://user-images.githubusercontent.com/6275775/230441813-e1a856fb-3437-4163-a88c-6c587c3fc014.png">

Next step is overriding Benedict's password with the vulnerable password page which takes a user supplied
user-id and the new password. Don't overcomplicate it, set it to 'a'.

Staying in our browser we can issue a fetch request right from the developer console:

```
fetch("https://benedicts.secchallenge.crysys.hu/change_password", {

  "headers": {
    "content-type": "application/x-www-form-urlencoded",
  },
  
  "body": "account_number=12&password=a&password_confirm=a",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```
That's it. We can log in now and grab the flag from Benedict's profile:

<img width="488" alt="image" src="https://user-images.githubusercontent.com/6275775/230442994-553a3a70-a9d0-4fc1-ab7a-cb44f8ba238d.png">
