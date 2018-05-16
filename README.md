Introduction
------------

Analysis of Chicago crime data to predict crime types

Utilized features: `["latitude", "longitude", "datetime", "loc_desc"]`
Primary target:
 - `"index_crime"`: Roughly speaking, this is true for serious crimes with an obvious victim.

Alternative targets are available. See settings of `modelling.py`.

Installation
============

As user with PostgreSQL database creation privileges:
WARNING: Will replace database 'chicago_crimes'

also currently probably broken.
```sh
git clone https://claymager/chicago-crime.git
cd chicago-crime/git
bash setup.sh
```

Edit SQL connections in `queries.py` to something sane.

Use
===

To launch the webapp:
 - run `app.py`
 - open localhost:5000 in browser

To experiment with models, features, and targets:
- edit settings section in `modelling.py`
- run `modeling.py`
- view results in log/

To add models to webapp:
(changing model or target)
- edit settings section in `mk_model.py`
- run `mk_model.py`
- edit `template/index.html#modelName` with new option
