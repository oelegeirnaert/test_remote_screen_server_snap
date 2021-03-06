======
Roman!
======

Since Python was named after the Monte Python comedy troupe, it seems fitting to open the Roman package with a question:

   ... but apart from better sanitation and medicine and education and irrigation and public health and roads and a freshwater system and baths and public order... what have the Romans done for us?
      -- _The Life Of Brian_, Monty Python

The answer: Roman Numerals!

-------
Purpose
-------

This is a "hello world" example of how to create a Python package. It does so by going through the process of creating a package (`roman`) that
- converting between roman numeral strings and integers
- converting between temperatures

Have a look at the Github repo to see the tutorial!

## Installation

To install
```bash
# installation is easy!
$ pip install --extra-index-url https://testpypi.python.org/simple/ roman
```

To uninstall (e.g. when updating) you can use `pip`, _even if you are only working locally_
```bash
# so is uninstalling!
$ pip uninstall roman
```

## Usage

Once installed, we can use this module with
```python
>>> import roman
>>> roman.int_to_roman_string(4)
'IV'
>>> roman.roman_string_to_int('MMC')
2100
>>> roman.convert_all(0, 'C')
{'K': 273.15, 'F': 32, 'C': 0}
```

## Useful references

- [This useful article on creating your first Python package](https://medium.com/38th-street-studios/creating-your-first-python-package-181c5e31f3f8)
- [The tox documentation](https://tox.readthedocs.io/en/latest/)
- [The Python code on Project structure](https://docs.python-guide.org/writing/structure/)
- [The Flask MegaTutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) for helping set up the git tag structure
