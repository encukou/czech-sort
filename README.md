Czech Sort
==========

This is a pure-Python library for Czech-language alphabetical sorting.


Quick Use
---------

From Python:

```python
>>> import czech_sort

>>> czech_sort.sorted(['sídliště', 'shoda', 'schody'])
['shoda', 'schody', 'sídliště']

>>> sorted(['sídliště', 'shoda', 'schody'], key=czech_sort.key)
['shoda', 'schody', 'sídliště']
```

On the command line::

```console
$ python -m czech_sort < file.txt
shoda
schody
sídliště
```

Why another sorting library?
----------------------------

To sort Python strings in the Czech language, there are three other options:

* Use [`PyICU`]. This can sort *really* well, and do all kinds of wonderful,
  standards-compliant Unicode things. Perfect for publication-quality results.
  Unfortunately, ICU can be a major pain to install, making it overkill if you
  just want to sort a list of strings.
* Set the locale, then use [`locale.strxfrm`].
  (Yes, `strxfrm`! Try saying that ten times fast!)
  This depends on the Czech POSIX locale being available, so it's hardly
  portable.
* Just use Python's built-in string sort. This sorts lexicographically by
  Unicode codepoints. It might be good enough for you? Maybe?

[`PyICU`]: https://pypi.python.org/pypi/PyICU
[`locale.strxfrm`]: https://docs.python.org/3/library/locale.html#locale.strxfrm

Scope
-----

The `czech-sort` library is a compromise. It should give you good results in
the 99% case.

Do not use this if you need proper sorting of symbols, non-Latin scripts,
or diacritics other than Czech/Slovak.

Any other deviation from the relevant standard, `ČSN 97 6030`, should be
considered a bug. However, neither the author nor the community at large
have access to the standard, which makes finding such bugs somewhat difficult.


Full API
---------

### `czech_sort.sorted(iterable)`

 Takes an iterable of strings, and returns a list of them, sorted.

### `czech_sort.key(s)`

 Returns a sort key object for a given string.

 This function is suitable as the `key` for functions like the built-in
 `sorted` or `list.sort`.

### `czech_sort.bytes_key(s)`

 Returns a sort key for a given string, as bytes.

 This is suitable as a DB-API custom function like the built-in
 `sqlite3` connection's `create_function`.

 WARNING: Do not store the results of this function. The format can change
 in future versions of `czech_sort`.


Compatibility
-------------

The czech-sort library can be used with Python 2.6+ and 3.5+.

Under Python 2, it only accepts `unicode` strings.


Installation
------------

Install this into your [`virtualenv`] by running:

```console
$ pip install czech-sort
```

[`virtualenv`]: https://docs.python.org/3/library/venv.html


Contribute
----------

Bug reports and comments are welcome [at Github][issues].

[issues]: http://github.com/encukou/czech-sort/issues/new

Patches are also welcome! Source code is hosted at Github:

```console
$ git clone http://github.com/encukou/czech-sort
```

To run the included tests:

```console
$ python -m pip install -e.[test]
$ python -m pytest
```

If you would like to contribute, but are confused by the above,
then please e-mail encukou `at` gmail `dot` com.


License
-------

The project is licensed under the MIT license. May it serve you well.
