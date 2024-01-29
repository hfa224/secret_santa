# Run the application

First start the poetry shell:

poetry shell

And install dependencies

poetry install (why is this necessary?)

Then use

flask --app secret_santa run --debug

# Database

Use:

flask --app secret_santa init-db

To intialise the database. This will clear any existing tables and add new ones

# To run tests

To run the tests, run:

pytest

To run test coverage, run:

coverage run -m pytest

coverage report

coverage html

