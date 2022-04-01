# Count Unique IDs per Minute

![system design overview](https://images.ctfassets.net/pedj0c0bs6fa/1GXGRyWeCBwvPw6d1Pym1T/2f7080d1ce6b80491fd114fe31abd4a9/kafka_ts_uid.drawio__1_.png)

- We have a website, and we track how many visits we have. Each visit is a json object.
- The raw data has lots of key value pairs. Please have a look at [`data/sample_data.json`](./data/sample_data.json) to get a feeling for the data.
- From the data set, we are only interested in the timestamp and the uid.
- With these values, we want to find out how many unique visitors we have.
- An initial analysis examines how many visitors we have per minute.
- Eventually, we will need an analysis of unique_visitors per hour, per day, per week, per month, per year

Please refer to the walkthrough in [`notebooks/walkthrough.ipynb`](./notebooks/walkthrough.ipynb).

### Counting Unique Visitors per Minute

```python
def count_uniques_per_min():
    window = {}
    window_count = 0
    previous_ts: int = 1

    while True:
        ts, uid = stream.dequeue()

        if ts % 60 != 0:
            if window.get(uid):
                continue
            window[uid] = 1
            window_count += 1

        if ts % 60 == 0 and ts - previous_ts != 0:
            utc_ts = datetime.utcfromtimestamp(ts)
            data = json.dumps({"datetime": str(utc_ts), "count": window_count})
            publish(topic="visits_per_minute", value=data)
            window = {}
            window_count = 0
            previous_ts = ts
```

Explanation and Complexity:

- We are using a HashMap in memory
- On every new minute, the HashMap will be reset
- We need a data structure that enables efficient ( O(1) or O(logn) ) operations of `check_if_uid_exists(uid)` and `add_new_data()`
- So a HashMap seems to be a good fit for it. A tree-like structure might work, too.

Considerations:

- Since the dict / hashmap is kept in memory, this will only work on one machine and can't be distributed in a cluster
- Memory should be large enough (or more precisely: Data is not supposed to be too big) to keep data in memory
- If there were ever so many unique visits per minute that memory couldn't keep it, you would need to offload it to disk.

### Counting Unique Visitors in Larger Time Windows

Since there will be waaay more data if the window was a week, a month or even a year, we can no longer hold the data in memory and need to offload it to disk. 

We can keep the algorithm, though, as long as we find an efficient implementation of these operations:

- `check_if_uid_exists(uid)`
- `add_new_data(ts, uid)`

For every time frame, we would need to keep a separate database in disk. 

We would need to publish the information every day to a topic, so we would need a cron job that publishes:

- Unique users past seven days
- Unique users past 30 days
- Unique users past 90 days
- Unique users past 180 days
- Unique users past 365 days


## How to run the application and execute the code

Make sure that you have a (dev) Kafka instance that you can communicate to according to `./config/kafka_config.ini` (in our case:``localhost:9092`). The main entrypoint to the application is the file `./src/cli.py`. You can see a walk through the functionality in [`./notebooks/walktrhough.ipynb`](./notebooks/walktrhough.ipynb). 

You can run `docker-compose up` to start kafka. 

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
