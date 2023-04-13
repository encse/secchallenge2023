# Evilbook

Evilbook was a Python/Flask challenge. It starts with a Facebook style social networking site 
where we can register a new user and log in with it.   

Examining the source code after login reveals a link to the debug version of the site:
https://debug-evilbook.secchallenge.crysys.hu/.

The nice thing about this other site is that it is running werkzeug / 
Flask in debug mode, so we get a nice exception for every runtime error we trigger. 
One way to use this is to delete the 'email' field from the password reset form,
or *sending a text instead of a number* in the captcha field. The relevant url is 
https://debug-evilbook.secchallenge.crysys.hu/forgot-password.

If we send in in some text instead of a number we get the following:

```python
    # Get the user's answer from the request
    user_answer = request.form['answer']
    email = request.form['email']
    if 'debug_answer' in session:
        # TODO fix value error
        if int(user_answer) == session['debug_answer']:
            ^^^^^^^^^^^^^^^^
            check_email = User.query.filter_by(email=email).first()
            if check_email:
                rounded_time = round(time.time(), 2)
                random.seed(rounded_time)
                password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for _ in range(12))
```

This reveals how the password is reset when the user_answer is correct. Let's go back to the original website now. There is 
an email in our timeline, let's try to steal this account with our newly learned knowledge. 

<img width="731" alt="image" src="https://user-images.githubusercontent.com/6275775/231820579-4e9f3346-1e6f-485f-8bef-4090f0a2c531.png">

We can write a Python script that resets the password and tries to log in with every possible passwords 
that could be generated in the small time window between the sending of the password change request and 
the arrival of the response. This is just a few trial and errors, about 10 or 20 maximum.

Now we can log in with the admin user and find the flag in his timeline.
