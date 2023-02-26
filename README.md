## Quiz-App
### Quizzes (tests) on various topics

<a id="top-page"></a>
[![Owner](https://img.shields.io/badge/owner-VinZVI-blue)](https://github.com/VinZVI)

[![Python Version](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.1-brightgreen.svg)](https://djangoproject.com)

Project website [Quiz-App](http://vinzvi.pythonanywhere.com/).

![](https://github.com/VinZVI/quiz_site/blob/9c2da13e6a8b23955d9d4f8b25399698282e3c3c/Quiz-App.png)

In this application, users can post their tests (quizzes) and take other tests posted on the site.



## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/VinZVI/quiz_site.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

