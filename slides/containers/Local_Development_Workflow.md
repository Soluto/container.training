
class: title

# Local development workflow with Docker

![Construction site](images/title-local-development-workflow-with-docker.jpg)

---

## Objectives

At the end of this section, you will be able to:

* Share code between container and host.

* Use a simple local development workflow.

---

## Local development in a container

We want to solve the following issues:

- "Works on my machine"

- "Not the same version"

- "Missing dependency"

By using Docker containers, we will get a consistent development environment.

---

## Working on the "namer" application

* We have to work on some application whose code is at:

  https://github.com/jpetazzo/namer.

* What is it? We don't know yet!

* Let's download the code.

```bash
$ git clone https://github.com/jpetazzo/namer
```

---

## Looking at the code

```bash
$ cd namer
$ ls -1
Dockerfile
Gemfile
Gemfile.lock
README.md
company_name_generator.rb
index.html.erb
```

--

Aha, a `Gemfile`! This is Ruby. Probably. We know this. Maybe?

---

## Let's start coding!
Can we develop ruby code without installing ruby?

Let's use docker!

```sh
docker run -p 8752:8752 -v $(pwd):/src -it ruby /bin/bash
root@59cc8a91c767:/#
```
Now we have a full running ruby environment inside a container!

---

## Our first volume

We will tell Docker to map the current directory to `/src` in the container.

```bash
$ docker run -p 8752:8752 -v $(pwd):/src -it ruby /bin/bash
```

* `-d`: the container should run in detached mode (in the background).

* `-v`: the following host directory should be mounted inside the container.

* `-P`: publish all the ports exposed by this image.

* `namer` is the name of the image we will run.

* We don't specify a command to run because it is already set in the Dockerfile.

Note: on Windows, replace `$(pwd)` with `%cd%` (or `${pwd}` if you use PowerShell).

---

## Mounting volumes inside containers

The `-v` flag mounts a directory from your host into your Docker container.

The flag structure is:

```bash
[host-path]:[container-path]:[rw|ro]
```

* If `[host-path]` or `[container-path]` doesn't exist it is created.

* You can control the write status of the volume with the `ro` and
  `rw` options.

* If you don't specify `rw` or `ro`, it will be `rw` by default.

There will be a full chapter about volumes!

---

## Running the sample app
To run the app inside our container:
```sh
root@59cc8a91c767:/# cd /src
root@59cc8a91c767:/# bundle install
root@59cc8a91c767:/# ruby company_name_generator.rb 
server listening on port 5678
```

Our code is running! 

How can we access our app?

---

## Connecting to our application

* Point our browser to our Docker node, on the port allocated to the container - 5678.

--

* Hit "reload" a few times.

--

* This is an enterprise-class, carrier-grade, ISO-compliant company name generator!

  (With 50% more bullshit than the average competition!)

  (Wait, was that 50% more, or 50% less? *Anyway!*)

  ![web application 1](images/webapp-in-blue.png)

---
## Making a change to our application

Our customer really doesn't like the color of our text. Let's change it.

```bash
$ vi index.html.erb
```

And change

```css
color: royalblue;
```

To:

```css
color: red;
```

---

## Viewing our changes

* Reload the application in our browser.

--

* The color should have changed.

  ![web application 2](images/webapp-in-red.png)

---

## Understanding volumes

* Volumes are *not* copying or synchronizing files between the host and the container.

* Volumes are *bind mounts*: a kernel mechanism associating a path to another.

* Bind mounts are *kind of* similar to symbolic links, but at a very different level.

* Changes made on the host or on the container will be visible on the other side.

  (Since under the hood, it's the same file on both anyway.)

---

## Looking at the `Dockerfile`

```dockerfile
FROM ruby:2.1
MAINTAINER Education Team at Docker <education@docker.com>

WORKDIR /src
COPY Gemfile /src
RUN bundler install
COPY . .

CMD ["ruby", "company_name_generator.rb"]
EXPOSE 8752
```

* This application is using a base `ruby` image.
* The code is copied in `/src`.
* Dependencies are installed with `bundler`.
* The application is started with `ruby`.
* It is listening on port 8752.

---

## Building and running the "namer" application

* Let's build the application with the `Dockerfile`!

--

```bash
$ docker build -t namer .
```

--

* Then run it. *We need to expose its ports.*

--

```bash
$ docker run -dP namer
```

--

* Check on which port the container is listening.

--

```bash
$ docker ps -l
```

---

## Making changes to the code

Option 1:

* Edit the code locally
* Rebuild the image
* Re-run the container

Option 2:

* Enter the container (with `docker exec`)
* Install an editor
* Make changes from within the container

Option 3:

* Use a *volume* to mount local files into the container
* Make changes locally
* Changes are reflected into the container

---


## Recap of the development workflow

1. Write a Dockerfile to build an image containing our development environment.
   <br/>
   (Rails, Django, ... and all the dependencies for our app)

2. Start a container from that image.
   <br/>
   Use the `-v` flag to mount our source code inside the container.

3. Edit the source code outside the containers, using regular tools.
   <br/>
   (vim, emacs, textmate...)

4. Test the application.
   <br/>
   (Some frameworks pick up changes automatically.
   <br/>Others require you to Ctrl-C + restart after each modification.)

5. Iterate and repeat steps 3 and 4 until satisfied.

6. When done, commit+push source code changes.

---

## Section summary

We've learned how to:

* Share code between container and host.

* Set our working directory.

* Use a simple local development workflow.

