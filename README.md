# Exercise: RESTful Cluster API

The goal of this exercise is to create a clean JSON API for creating a "cluster", and retrieving a created "cluster" by its ID, using Django with Django REST Framework.

A cluster represents a computation resource (such as an EC2 task) launched on the cloud, and is created with the following arguments:

- the ID of the `User` who created it
- A number of CPUs to allocate per worker, which must be >0 and <=16
- An amount of memory to allocate per worker, which must be >0 and <= 128GiB.

### Success Criteria

We must be able to make POST requests to a `clusters/` API endpoint to create a cluster, and GET requests to `/clusters/:id` to look one up.

All requests must require authentication. (A popular option is via an `Authorization` header, with a token, but that's not required).

Only the user who created a cluster should be able to look it up.

At creation time, the POST should validate that the arguments are correct (e.g. that there's a valid number of CPUs and amount of memory).

Running `pytest` in the root of the repo should run at least one test, but thorough coverage is by no means expected nor required.

### Repo Contents, i.e. what's provided

The repo contains a Django project named `clusters` and an app named `launcher`.

A basic `User` model and partial `Cluster` model are defined in `launchers`.

Two sample `User`s are provided: `alice` and `betty`, both of whose password is `hunter2`.

### Install

This was built with Python 3.8, though Python 3.7 should work fine.

In a virtual environment, install the dependencies found in `requirements.txt`.

Ensure that your local SQLite database is up to date and contains the sample admin users:

```shell
python manage.py migrate && python manage.py loaddata launcher/fixtures/initial.yaml
```

### Endpoints:

Users can access their clusters via a GET request to `http://<base_url>/clusters/`

Users can create a cluster via a POST request to `http://<base_url>/clusters/`, which must include the json parameters:

```
{
  'creator': 1,  # the user id of the user
  'cpus': 10,
  'memory': 10,
}
```

Users can see the detail view of a cluster belonging to them via a GET request to `http://<base_url>/clusters/<:id>`

### Authentication:

To retrieve a valid token, login credentials must be POSTed to `http://<base_url>/token/login/`.
This post must be accompanied by the `X-CSRF-Token` value in the headers of the request. This value can be retrieved from the `csrftoken` value cookie associated with the request.

In order to access `/clusters/` resources, the request headers must include a valid authorization token in the form:

```
{ 'Authentication': 'Token 123abc321bca4b122407a1f0363d969e19160a2f'}
```
