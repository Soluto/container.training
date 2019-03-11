# Compose for development stacks

Dockerfiles are great to build container images.

But what if we work with a complex stack made of multiple containers?

In our case - run integration tests that requires Mongo DB.

Eventually, we will want to write some custom scripts and automation to build, run, and connect
our containers together.

There is a better way: using Docker Compose.

In this section, you will use Compose to bootstrap a development environment.

---

## What is Docker Compose?

Docker Compose (formerly known as `fig`) is an external tool.

Unlike the Docker Engine, it is written in Python. It's open source as well.

The general idea of Compose is to enable a very simple, powerful onboarding workflow:

1. Checkout your code.

2. Run `docker-compose up`.

3. Your app is up and running!

---

## Compose overview

This is how you work with Compose:

* You describe a set (or stack) of containers in a YAML file called `docker-compose.yml`.

* You run `docker-compose up`.

* Compose automatically pulls images, builds containers, and starts them.

* Compose can set up links, volumes, and other Docker options for you.

* Compose can run the containers in the background, or in the foreground.

* When containers are running in the foreground, their aggregated output is shown.

---

## The `docker-compose.yml` file

Here is the file used in the demo:

.small[
```yaml
version: '3'

services:
  mongo:
    image: mongo
    logging:
      driver: none
  api:
    build:
      context: ../
      dockerfile: ./solution/Dockerfile
    command: ["yarn", "test"]
    environment:
      - CONNECTION_STRING=mongodb://mongo:27017
```
]

---

## Compose file structure

A Compose file has multiple sections:

* `version` is mandatory. (We should use `"2"` or later; version 1 is deprecated.)

* `services` is mandatory. A service is one or more replicas of the same image running as containers.

---

## Containers in `docker-compose.yml`

Each service in the YAML file must contain either `build`, or `image`.

* `build` indicates a path containing a Dockerfile.

* `image` indicates an image name (local, or on a registry).

* If both are specified, an image will be built from the `build` directory and named `image`.

The other parameters are optional.

They encode the parameters that you would typically add to `docker run`.

---

## Compose commands

To launch the stack, run:

```bash
docker-compose up --build
```

---

## Waiting for tests to complete

We saw how to run the tests, but how can we use that to run tests?

This is where we can use the `--exit-code-from` flag:

```bash
docker-compose up --exit-code-from api
```

---

## Service discovery in container-land

How does each service find out the address of the other ones?

--

- We do not hard-code IP addresses in the code

- We do not hard-code FQDN in the code, either

- We just connect to a service name, and container-magic does the rest

  (And by container-magic, we mean "a crafty, dynamic, embedded DNS server")
  
--

For example, this is how the web is connected with the DB:
```
CONNECTION_STRING=mongodb://mongo:27017
```

---

## A real life example

The tools we learned today are used commonly for testings.
Checkout for example [Kamus](https://github.com/Soluto/kamus) end to end tests.
[CI build example](https://circleci.com/gh/Soluto/kamus/1346)

.small[
```
version: '3'
services:
  encryptor:
    image: $ENCRYPTOR_IMAGE
    environment:
  decryptor:
    image: $DECRYPTOR_IMAGE
    environment:
      - Kubernetes__ProxyUrl=http://wiremock:8080
  black-box:
    build:
      context: ../
    environment:
      - ENCRYPTOR=http://encryptor:9999/
      - DECRYPTOR=http://decryptor:9999/
      - PROXY_URL=http://zap:8090
      - KUBERNETES_URL=http://wiremock:8080
  wiremock:
    build:
      context: ../Wiremock
```
]