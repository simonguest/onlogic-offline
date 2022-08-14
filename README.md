<img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" width=200>

# Code<span>.org Docker Dev Environment
The Code<span>.org Docker dev environment enables you to run and develop on the Code<span>.org platform on your laptop, using Docker containers.

Doing so offers many advantages over setting up a development environment directly on your laptop. This include:

- No need to worry about managing dependencies (e.g., setting up rbenv, managing versions of Ruby, or removing/installing Ruby gems).
- Rebuilding your development environment is scripted, which makes it easy to test new changes, such as a new version of a Ruby gem or even a new version of MySQL. 
- It's easier to have multiple versions of the Code<span>.org dev environment and database on the same machine.
- A docker-based development environment works better for Code<span>.org volunteers, who may not want to install a bunch of our dependencies directly on their employer-provided machines.
- The docker-based environment uses Ubuntu, which mimics our production environment (and reduces the chance of things working on your laptop, but not on our production servers).
- When you are not developing, you can pause/stop the dev containers which frees up more resources on your machine.
- Rebuilding a container is a lot easier than rebuilding your laptop!

## How does it work?

The Code<span>.org Docker dev environment uses docker compose to create two containers: web and db. These both run on your host laptop.

The web container runs all of the code required for dashboard and pegasus. All of the source code is stored on the host laptop under the "src" sub-directory.

The db container runs MySQL 5.7. All of the data files for MySQL are stored on the host laptop using the "data" sub-directory.

Docker networking provides a connection between the two containers.

<<nice-looking diagram here>>

## Pre-requisite: Docker Desktop
The only pre-requisite you need on your host laptop is Docker desktop.  If you don't have it already installed and running, you can download it [here](https://www.docker.com/products/docker-desktop/).

Note: This repo has been tested using Docker version 20.10.9.

## Step 1: Build and run the containers
- Open a terminal and clone this repo:
	- ```git clone git@github.com:simonguest/codeorg-docker-dev.git```
- CD to this directory, git clone the Code<span>.org repository as a sub-directory called src:
	- ```cd codeorg-docker-dev.git```
	- ```git clone git@github.com:code-dot-org/code-dot-org.git src```
- Edit src/Gemfile:
	- Remove mini_racer gem (I really don't think we use this any more)
	- Update unf_ext to 0.0.8 (and also update Gemfile.lock unf_ext from 0.0.7.2)
	- Add gem 'tzinfo-data' (this is required for db seeding in containers)
- Edit src/config/development.yml.erb
	- Set db_writer to ```'mysql://root:password@db/'``` (this points the development environment to the db container vs. the local machine).
- Build the containers:
	- ```docker compose build```
- Run the containers:
	- ```docker compose up```
	- You'll need to open a new terminal window/tab to continue with the rest of the setup.

## Step 2: Configure AWS credentials
- Ensure $HOME/.aws on your host laptop contains valid AWS credentials. You probably already have this setup, but if you don't, you can find instructions [here](https://docs.google.com/document/d/1dDfEOhyyNYI2zIv4LI--ErJj6OVEJopFLqPxcI0RXOA/edit#heading=h.nbv3dv2smmks).
- Connect to the web container:
	- ```docker exec -ti web /bin/bash```
- Run the aws_access script:
	- ```cd /app/src```
	- ```bin/aws_access```
	- When prompted, copy and paste the URL into a separate browser window and copy the returned OAUTH_CODE to the clipboard.
- Stop the containers
	- Return to the first terminal window/tab and hit CTRL-C to shutdown the web and db containers.
- Set the OAUTH_CODE on the host:
	- ```export OAUTH_CODE=[copied value]```
	- (If you don't want to repeat this when you close the terminal window, add this to your ~/.bashrc or other terminal profile script.)
- Restart the containers:
	- ```docker compose up```

## Step 3: Seed the db
- Connect to the web container:
	- ```docker exec -ti web /bin/bash```
- Rake install:
	- ```cd /app/src```
	- ```bundle exec rake install```

## Step 4: Build the web package
- Connect to the web container:
	- ```docker exec -ti web /bin/bash```
- Rake build:
	- ```cd /app/src```
	- ```bundle exec rake build```

## Step 5: Run the server
- Connect to the web container:
	- ```docker exec -ti web /bin/bash```
- Run the dashboard server script:
	- ```cd /app/src```
	- ```bin/dashboard-server```
- Open a web browser and browse to http://localhost-studio.code.org:3000

## Optional: Exposing MySQL (on port 3306) to the host
If you have a MySQL client on your host laptop (e.g., JetBrains Datagrip or SQLPro), you can also connect directly to the MySQL database running in the db container.

To do this, edit your docker-compose.yml file and add the following section in the db configuration:

```
ports:
  - "3306:3306"
```

Stop and restart the containers, and your db container will now be accessible on localhost:3306. Use the credentials specified in the docker-compose.yml file.

Note: The db container won't start if you already have an existing MySQL installation on your host laptop (as port 3306 will already be in use). To overcome this, either uninstall MySQL on the host, or bind to a port other than 3306:

```
ports:
  - "3307:3306"
```

## FAQ

#### Q: If I delete the containers, does it delete any data?

No, all data resides on the host laptop and mounted by the containers when they start. Source is kept in the ./src folder. Database files are kept in the ./data folder.

#### Q: Where do I set my development environment to point to?

Use your preferred IDE to make changes in the ./src folder - just as you would if you were developing on your host laptop. 

#### Q: Do I need to go through all these steps every time?

No, once the containers are created, you are all set! Just start the containers:

```
docker compose up
```

And in another terminal window/tab, run the dashboard-server script.

```
docker exec -ti web /bin/bash
cd /app/src
bin/dashboard-server
```

#### Q: How do I rebuild my database?

All of the MySQL database files are held in the ./data directory. To rebuild the database from scratch, simply delete this folder, restart the containers, and run the seeding step again.

#### Q: I need to install a new Gem. How do I do this?

Edit src/Gemfile, connect to the Web container, and run bundle install:

```
docker exec -ti web /bin/bash
cd /app/src
bundle install
```

If you want this Gem to persist container restarts, rebuild the container:

```
docker compose build
```

#### Q: Is using Docker slower than developing on my laptop?

There should be little noticeable performance difference between developing using Docker and on your host laptop. Older versions of Docker used to have issues with mounting large volumes, but this has since been resolved with VirtioFS.

#### Q: Do I need to install Ruby and/or MySQL on my host laptop?

No! The only required dependency on the host laptop is Docker desktop.

#### Q: Does this work on Windows-based PCs?

It should, but this README needs to include the Windows-equivalent commands. Volunteers welcome :)

#### Q: Does this work for M1-based Macs?

Yes, the dev environment works for both x86 and ARM64-based machines.

#### Q: Does this work for Linux-based PCs?

Yes. These instructions will also work for Linux-based server images (such as an EC2 instance running in AWS).