Django NPS
==========

**Django app supporting Net Promoter Score (NPS) surveys**

Background - Net Promoter Score
-------------------------------

The NPS is a measure of customer loyalty that is captured by asking your
customers a singe question:

::

    How likely is it that you would recommend our [company|product|service] to a friend or colleague?"

The answer to this question is a number from 0-10 (inclusive). These scores
are then broken out into three distinct groups: 'detractors' (0-6), 'neutral'
(7-8) and 'promoters' (9-10). The NPS is then the difference between the
number of promoters and detractors (as a percentage of the whole population).

For example, if you ask 100 people, and you get the following results:

.. code::

    detractors: 20%
    neutrals:   10%
    promoters:  70%

Then your NPS is 70 - 20 = 50. *(NPS is expressed as a number, not a %)*

NPS was orginally developed at the strategy consultants Bain & Company by Fred Reichheld in 2003.
They retain the registered trademark for NPS, and you can read all about the history of it on
their site "`Net Promoter System <http://netpromotersystem.com/about/index.aspx>`_".

Usage
-----

This app is used to store the individual scores, and calculate the NPS based
on these. It does not contain any templates for displaying the question itself,
neither does it put any restriction around how often you ask the question, or
to whom. It is up to the app developer to determine how this should work - 
each score is timestamped and linked to a Django User object, so you can
easily work out the time elapsed since the last time they were asked.

For example, if you want to ensure that you only survey users every X days,
you can add a context property to the template using the ``display_to_user``
method:

.. code:: python

    >>> # only show the survey every 90 days
    >>> show_nps = UserScore.objects.display_to_user(request.user, 90)
    True


If you then show the survey - the output of which is a single value (the score)
together with an optional reason ("what is the main reason for your score"), is
then posted to the ``post_score`` endpoint, which registers the user score.

The NPS value itself can be calculated on any queryset of ``UserScore`` objects -
which allows you to track the score based on any attribute of the score itself
or the underlying user. For instance, if you have custom user profiles, you
may wish to segement your NPS by characteristics of those profiles.

.. code:: python

    >>> # December's NPS
    >>> UserScore.objects.filter(timestamp__month=12).net_promoter_score()
    50

The ``post_score`` endpoint returns a ``JsonResponse`` which contains a ``'success': True|False``
value together with the `UserScore` details:

.. code:: python

    {
      "success": True,
      "score": {"id": 1, "user": 1, "score": 0, "group": "detractor"}
    }

If the score was rejected, the errors are returned in place of the score (errors
are a list of lists, as returned from the Django `Form.errors` property:

.. code:: python

    {
      "success": False,
      "errors": [["score", "Score must be between 0-10"]]
    }

Tests
-----

There is a full suite of tests for the app, which are best run through `tox`. If
you wish to run the tests outside of tox, you should install the requirements first:

.. code:: shell

    $ pip install -r requirements.txt
    $ python manage.py test

Licence
-------

MIT

Contributing
------------

Usual rules apply:

1. Fork to your own account
2. Create a branch, fix the issue / add the feature
3. Submit PR

Please take care to follow the coding style - and PEP8.

Acknowledgements
----------------

Credit is due to **epantry** for the `original project <https://github.com/epantry/django-netpromoterscore>`_ from which this was forked.

Thanks also to the kind people at **Eldarion** (`website  <http://eldarion.com/>`_) for releasing the PyPI package name.
