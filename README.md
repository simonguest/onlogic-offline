# Code.Org Docker Dev Environment
The Code.org Docker dev environment enables you to run and develop the Code.org platform in Docker containers.

Doing so offers many advantages over setting up a development directly on your laptop. Using Docker, you don't need to worry about managing dependencies (e.g., setting up rbenv, managing versions of Ruby, or removing/installing Ruby gems). It's also easy to rebuild your development environment, which makes it possible to quickly test new changes, such as a new version of a Ruby gem. Finally, using Docker, it's also possible to have multiple versions of the Code.org dev environment and database running on the same machine.

## How does it work?

The Code.org Docker dev environment uses docker compose to create two containers: web and db. 

The web container runs all of the code required for dashboard and pegasus. All of the source code is stored on the host machine under the "src" sub-directory.

The db container runs MySql 5.7. All of the data files for MySql are stored on the host machine using the "data" sub-directory.

<<nice-looking diagram here>>

Note: As everything is containerized, you do not need Ruby or MySQL installed on your host machine!

## Pre-requisite: Docker Desktop
The only pre-requisite you need on your host is Docker desktop.  If you don't have it already installed and running, download it [here](https://www.docker.com/products/docker-desktop/).

Note: This repo has been tested using Docker 20.10.9.

## Step 1: Build and run the containers
- In this repo, git pull the Code.org repository as a sub-directory called src:
  - ```git clone git@github.com:code-dot-org/code-dot-org.git src```
- Edit src/Gemfile:
	- Remove mini_racer gem (I really don't think we use this any more)
	- Update unf_ext to 0.0.8 (and also update Gemfile.lock unf_ext from 0.0.7.2)
	- Add gem 'tzinfo-data' (this is required for db seeding)
- Edit src/config/development.yml.erb
	- Set db_writer to ```'mysql://root:password@db/'``` (this points the development environment to the db container vs. the local machine).
- Build the containers:
	- ```docker compose build```
- Run the containers:
	- ```docker compose up```
	- You'll need to open a new terminal window/tab to continue with the rest of the setup.

## Step 2: Configure AWS credentials
- Ensure $HOME/.aws on your host machine contains valid AWS credentials. If you don't already have this setup, you can find instructions [here](https://docs.google.com/document/d/1dDfEOhyyNYI2zIv4LI--ErJj6OVEJopFLqPxcI0RXOA/edit#heading=h.nbv3dv2smmks).
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
	- (If you don't want to have to repeat this, you can add this line to your ~/.bashrc or other terminal profile script.)
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

## Exposing MySQL (on port 3306) to the host
If you have a MySQL client on your host machine (e.g., JetBrains Datagrip or SQLPro), you can also connect directly to the MySQL database running in the db container.

To do this, edit your docker-compose.yml file and add the following section in the db configuration:

```
ports:
  - "3306:3306"
```

Stop and restart the containers, and your db container will now be accessible on localhost:3306. Use the credentials specified in the docker-compose.yml file.

Note: The db container won't start if you already have an existing MySQL installation on your host machine (as port 3306 will already be in use). To overcome this, either uninstall MySQL on the host, or bind to a port other than 3306:

```
ports:
  - "3307:3306"
```