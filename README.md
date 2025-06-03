# Backend

Recruitment app for Intercars

# Architecture

You told me to focus not on views but on backend, so I decided to write this app as "headless" and as the main framework I chose not pure django but django-rest-framework. I based the standards on styleguide created by HackSoftware available here:

https://github.com/HackSoftware/Django-Styleguide

I chose this styleguide for two reasons:

1. I like it a lot :) Although I slightly modified it for myself

2. Your app has been working for years and is written for years - this styleguide is very "rigid" and describes well the responsibility of individual elements, which is why I think it is very suitable for such applications.

I treated the "intercars" module as common, I don't know if it wouldn't be better to separate it to another app, but I'll leave it as it is. There are utilities and commons downloaded from the aforementioned style guide. Personally, I don't like the implementation itself and if I had more time, I would improve these utilities a bit.

## Docker Images:

Redis = I wanted to use it for caching but I ran out of time

Postgres = Database

Backend = Django Server. The code is in the /app/ directory

# Run

```bash
$ cd docker
$ docker-compose up --build
```

The server will automatically "start up" but there are no fixes written. You need to create users via

```bash
./manage createsuperuser
```

# Tests

Script run_test.sh

The script automatically starts tests and returns coverage to the *htmlcov* directory. This is convenient for CI, because it returns output
from tests (which will nicely show the error in CI) and at the same time the *htmlcov* directory is useful when it is thrown into
artifacts.

In addition, the prospector is configured and installed, which is easiest to run from the main project directory:

```bash
python3 -m prospector
```

# Swagger

end: ```http://0.0.0.0:8000/swagger/```
Quickly how to use it:

Find the ```/ login /``` end and log in to the user you created earlier using "createsuperuser".
In the return you will get a token, which you should enter in the window that appears after clicking the ```Authenticate``` button
which is at the top of the swagger page on the right. The token should be entered in the formula: ```Token xxxxxxxxx```. From now on,
the header will be added to every frame when using swagger. This is the most convenient option for using this
API.

# TODO:

There are a few things I still wanted to do but I ran out of time. The most obvious ones are:

1. IbanField - which would automatically determine and validate the iban field
2. BaseSerializer - which would have, for example, Meta in which ref_name=None would always be, so that you wouldn't have to write it every time.

3. I wanted to use redis as a cache

4. Working gitlab CI-CD

5. More tips, but I think there's enough code to show how I think.

6. You can make the iban primary key from the field
7. Unity for services - I decided that tests for users are enough to show that I can write them :)
8. Logging - I usually use structlog, but the app doesn't do much, so I finally skipped the topic.
