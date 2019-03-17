
class: title

# Building Docker images with a Dockerfile

![Construction site with containers](images/title-building-docker-images-with-a-dockerfile.jpg)

---

## Objectives

We will build a container image automatically, with a `Dockerfile`.

At the end of this lesson, you will be able to:

* Write a `Dockerfile`.

* Build an image from a `Dockerfile`.

---

## `Dockerfile` overview

* A `Dockerfile` is a build recipe for a Docker image.

* It contains a series of instructions telling Docker how an image is constructed.

* The `docker build` command builds an image from a `Dockerfile`.

---

## Writing our first `Dockerfile`

Our Dockerfile must be in a **new, empty directory**.

Create a `Dockerfile` inside this directory.

```bash
$ cd compose-exercise
$ vim Dockerfile
```

Of course, you can use any other editor of your choice.

---

## Type this into our Dockerfile...

```dockerfile
FROM node

WORKDIR /app
COPY . .
RUN yarn install
```

* `FROM` indicates the base image for our build.

* `WORKDIR` set the working directory for the rest of the commands

## The `RUN` instruction

* Each `RUN` line will be executed by Docker during the build.

* Our `RUN` commands **must be non-interactive.**
  <br/>(No input can be provided to Docker during the build.)

---

## The `COPY` instruction

The `COPY` instruction adds files and content from your host into the
image.

```dockerfile
COPY . /src
```

This will add the contents of the *build context* (the directory
passed as an argument to `docker build`) to the directory `/src`
in the container.

---

## Build it!

Save our file, then execute:

```bash
$ docker build -t api .
```

* `-t` indicates the tag to apply to the image.

* `.` indicates the location of the *build context*.

We will talk more about the build context later.

To keep things simple for now: this is the directory where our Dockerfile is located.

---

## What happens when we build the image?

The output of `docker build` looks like this:

.small[
```bash
Sending build context to Docker daemon  25.03MB
Step 1/4 : FROM node
 ---> c63e58f0a7b2
Step 2/4 : WORKDIR /app
 ---> Running in ef77b990dd3d
Removing intermediate container ef77b990dd3d
 ---> 5029fcef7d04
Step 3/4 : COPY . .
 ---> 9b7600bcc932
Step 4/4 : RUN yarn install
 ---> Running in bc1af5515cd0
yarn install v1.13.0
info No lockfile found.
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Saved lockfile.
Done in 0.07s.
Removing intermediate container bc1af5515cd0
 ---> 46277efee36f
Successfully built api:latest
```
]

* Let's explain what this output means.

---

## Sending the build context to Docker

```bash
Sending build context to Docker daemon  25.03MB
```

* The build context is the `.` directory given to `docker build`.

* It is sent (as an archive) by the Docker client to the Docker daemon.

* This allows to use a remote machine to build using local files.

* Be careful (or patient) if that directory is big and your link is slow.

---

## Executing each step

```bash
Step 3/4 : COPY . .
 ---> 9b7600bcc932
Step 4/4 : RUN yarn install
 ---> Running in bc1af5515cd0
(...output of the RUN command...)
Removing intermediate container bc1af5515cd0
 ---> 46277efee36f
```

* A container (`9b7600bcc932`) is created from the previous step.

* The `RUN` command is executed in this container.

* The container is committed into an image (`e01b294dbffd`).

* The build container (`9b7600bcc932`) is removed.

* The output of this step will be the base image for the next one.

---

## The caching system

If you run the same build again, it will be instantaneous. Why?

* After each build step, Docker takes a snapshot of the resulting image.

* Before executing a step, Docker checks if it has already built the same sequence.

You can force a rebuild with `docker build --no-cache ...`.

---

## More efficient images

If you make change any file, docker will run `yarn install` again. Why?
Let's look on the docker file again: 

```dockerfile
(1) FROM node

(2) WORKDIR /app
(3) COPY . .
(4) RUN yarn install
```

Take a look on line 3.

---

## Docker file - V2

```dockerfile
FROM node

WORKDIR /app
COPY package.json yarn.lock /app/
RUN yarn install
COPY . .
```

Now `yarn install` will run only if `package.json` has changed!

---

## Running the image

The resulting image is not different from the one produced manually.

```bash
$ docker run -it api
> 
```

Why nothing happened?

## The `CMD` instruction

The `CMD` instruction is a default command run when a container is
launched from the image.
Add the following line to the dockerfile:

```dockerfile
CMD ["node", "src/server.js"]
```

---

## The complete dockerfile

You're dockerfile now should look like the following:

```dockerfile
FROM node

WORKDIR /app
COPY package.json yarn.lock /app/
RUN yarn install
COPY . .
CMD ["node", "src/server.js"]
```

---

## Running the image V2

Build the updated dockerfile using:
```
docker build . -t api
```
The resulting image is not different from the one produced manually.

```bash
$ docker run -it api
Example app listening on port 5678!
```

YAY!