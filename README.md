djangodash2012
==============

[![Build Status](https://secure.travis-ci.org/elegion/djangodash2012.png?branch=master)](http://travis-ci.org/elegion/djangodash2012)

Django Dash 2012 entry for team e-Legion

License
-------

MIT/X11. See LICENSE-MIT file.

What
----

Online tool to create automatic acceptance tests for REST/JSON APIs.

Testing
-------

If you accidentally deleted demo testcases, you always can use demo fixtures:

    python manage.py loaddata fixtures/demo/editor.json fixtures/demo/auth.json

Tips and tricks
---------------

### Query parameters

Query parameters support special mini-language. Currently it is possible to
provide either plain value by simply typing it in the field, or a random value,
typing `{random}` special form:

    {random:7:d}
    {random:8:7}
    {random:140}

The special form syntax is: `{random:length:symbols}`, where `length` is an
integer and `symbols` is one of:

 * `d` for digits
 * `l` for lowercase letters
 * `L` for uppercase letters
 * `symbols` might be ommited to use digits and letters

### Assertions

Assertion expressions have a syntax to do response fields querying. Let's shoot
examples along with explanation.

Status code of last query:

    .status_code

Take first query, its parsed json body, second array index, text property:

    0.json.1.text
