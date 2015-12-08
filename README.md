# Django NPS #

**Django app supporting Net Promoter Score (NPS) surveys**

---

NB This project was originally forked from https://github.com/epantry/django-netpromoterscore,
but has since moved far enough away from that project to be considered a separate project (i.e.
it won't ever be merged back in).

---

##Background - Net Promoter Score

The NPS is a measure of customer loyalty that is captured by asking your
customers a singe question:

    How likely is it that you would recommend our [company|product|service] to a friend or colleague?"

The answer to this question is a number from 0-10 (inclusive). These scores
are then broken out into three distinct groups: 'detractors' (0-6), 'neutral'
(7-8) and 'promoters' (9-10). The NPS is then the difference between the
number of promoters and detractors (as a percentage of the whole population).

For example, if you ask 100 people, and you get the following results:

    detractors: 20%
    neutrals:   10%
    promoters:  70%

Then your NPS is 70 - 20 = 50.
_(NPS is expressed as a number, not a %)_

NPS was orginally developed at the strategy consultants Bain & Company by Fred Reichheld in 2003.
They retain the registered trademark for NPS, and you can read all about the history of it on
their site "[Net Promoter System](http://netpromotersystem.com/about/index.aspx)".

## Usage

This app is used to store the individual scores, and calculate the NPS based
on these. It does not contain any templates for displaying the question itself,
neither does it put any restriction around how often you ask the question, or
to whom. It is up to the app developer to determine how this should work - 
each score is timestamped and linked to a Django User object, so you can
easily work out the time elapsed since the last time they were asked.

For example, if you want to ensure that you only survey users every X days,
you can add a context property to the template using the `display_to_user`
method:

```python
>>> # only show the survey every 90 days
>>> show_nps = UserScore.objects.display_to_user(request.user, 90)
True
```

If you then show the survey - the output of which is a single value (the score)
together with an optional reason ("what is the main reason for your score"), is
then posted to the `post_score` endpoint, which registers the user score.

The NPS value itself can be calculated on any queryset of `UserScore` objects -
which allows you to track the score based on any attribute of the score itself
or the underlying user. For instance, if you have custom user profiles, you
may wish to segement your NPS by characteristics of those profiles.

```python
>>> # December's NPS
>>> UserScore.objects.filter(timestamp__month=12).net_promoter_score()
50
```

The `post_score` endpoint returns a `JsonResponse` which contains a `'success': True|False`
value together with the `UserScore` details:

```python
{
  "success": True,
  "score": {"id": 1, "user": 1, "score": 0, "group": "detractor"}
}
```

If the score was rejected, the errors are returned in place of the score (errors
are a list of lists, as returned from the Django `Form.errors` property:

```python
{
  "success": False,
  "errors": [["score", "Score must be between 0-10"]]
}
```

##Tests

There is a full suite of tests for the app, which are best run through `tox`. If
you wish to run the tests outside of tox, you should install the requirements first:

```shell
$ pip install -r requirements.txt
$ python manage.py test
```

##Licence

MIT

##Contributing

Usual rules apply:

1. Fork to your own account
2. Create a branch, fix the issue / add the feature
3. Submit PR

Please take care to follow the coding style - and PEP8.


<!-- Django Net Promoter Score is designed to help you find out what your customers think of your application. The net promoter score metric is based on user feedback to one question, "On a scale from 1 to 10 how likely are you to recommend us to a friend or colleague?". You can jazz this question up to fit your projects needs, and use Django Net Promoter Score to keep track of user response and detect when it is time to ask a user the question again. Django Net Promoter Score also features an administrative page that displays a breakdown of the net promoter score metric over a 13 month period.

## Installation ##

Few simple steps:

 - Install `django-netpromoterscore` package:

        $ pip install django-netpromoterscore

 - Add `netpromoterscore` to your `INSTALLED_APPS`

 - Add urls to your urls.py:

        urlpatterns = patterns('',
            ...
            url(r'^api/survey/$', SurveyView.as_view(), name='survey'),
            url(r'^admin/net-promoter-score/', NetPromoterScoreView.as_view(), name='net-promoter-score'),
            ...
        )

- You are done!

## API ##

    GET /api/survey/

Returns `{ "survey_is_needed": true_or_false }`

    POST /api/survey/

With json POST data without `"id"` like `{ "score": 9 }` creates new PromoterScore instance for current user.

If `"id"` is provided and POST data is like `{ "id": 15, "reason": "Awesome!"}`, updates existing PromoterScore instance.

Returns `{ "id": PROMOTER_SCORE_ID }`

## Information on NPS Metric ##
There is some fantastic information available online to help you understand the NPS metric and how to use it to create healthier relationships with your users.

The [Bain & Company website](http://netpromotersystem.com/ "Title") is a handy resource for gaining insight into your applications net promoter score.

## Features ##
__Administrative Page__
![net promoter score administrative page][id]
[id]: http://i.imgur.com/lwI4W5K.png "Net Promoter Score Admin Page"
 -->
