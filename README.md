# Log Queue API

## About the Project

In this project, I am going to build a service that can process data from events. There are two types of events:

1. User Events
2. Organization Events

To process these events, I will implement a log / a message queue. I have no prior experience with stream processing or with Kafka, but I will use this opportunity to explore Kafka.

There is going to be a service that aggregates the data and enables to fetch data through http get requests. 

The GET request should only hold the latest state of the user. It should consume
that data, combine it and hold it in memory until it will be fetched from it

## The raw src data

As mentionned above, there are two data sources: User Events and Organization Events. Here are two samples:


### Organization Events

The following data is emitted when a new organization is created:

```json
[
  {
    "organization_key": "ff3959a49ac10fc70181bc00e308fbeb",
    "organization_name": "Metal Gear Solid",
    "organization_tier": "Medium",
    "created_at": "2018-01-24 17:28:09.000000"
  },
  ...
]
```

### User Event

Whenever there is a change to user data, the following event will be emitted. 

There are three event_types: 

1. User Created
2. User Deleted
3. User Updated

```json
[
  {
    "id": "069feb770fe581acc9d3313d59780196",
    "event_type": "User Created",
    "username": "Snake",
    "user_email": "snake@outerheaven.com",
    "user_type": "Admin",
    "organization_name": "Metal Gear Solid",
    "received_at": "2020-12-08 20:03:16.759617"
  },
  ...
]
```

## Getting Started

To set up your local development environment, please use a fresh virtual environment.

To create the environment run:

    conda env create --name log-queue-api --file=environment-dev.yml

To activate the environment run:

    conda activate log-queue-api

To update this environment with your production dependencies run:

    conda env update --file=environment.yml

You can now import functions and classes from the module with `import log_queue_api`.

If you want to deploy this project as a docker container, please ensure that [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed, then run

    docker-compose up

this will build the entire project with all dependencies inside a docker container. You may use the command line interface of the application now, e.g. by editing the `command` tag in the [`docker-compose.yml`](./docker-compose.yml).

### Testing

We use `pytest` as test framework. To execute the tests, please run

    python setup.py test

To run the tests with coverage information, please use

    python setup.py testcov

and have a look at the `htmlcov` folder, after the tests are done.

### Notebooks

To use your module code (`src/`) in Jupyter notebooks (`notebooks/`) without running into import errors, make sure to install the source locally

    pip install -e .

This way, you'll always use the latest version of your module code in your notebooks via `import log_queue_api`.

Assuming you already have Jupyter installed, you can make your virtual environment available as a separate kernel by running:

    conda install ipykernel
    python -m ipykernel install --user --name="log-queue-api"

Note that we mainly use notebooks for experiments, visualizations and reports. Every piece of functionality that is meant to be reused should go into module code and be imported into notebooks.

### Distribution Package

To build a distribution package (wheel), please use

    python setup.py dist

this will clean up the build folder and then run the `bdist_wheel` command.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

## Contact

David Kuda (david@kuda.ai)

## License

© David Kuda
