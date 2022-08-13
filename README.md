# Code.Org Docker Development Environment

## How it works

1. Uses two containers...

## Advantages of using Docker instead of your main machine

1. Don't worry about dependencies
2. Can blow away environment and recreate very quickly
3. Because of this, can quickly test new changes to the environment: e.g., new version of a ruby gem
4. Multiple versions of your dev environment
5. Multiple versions of the database

## Pre-requisites

1. Docker Desktop (tested on Docker 20.10.9)
2. Ensure host has localhost-studio.code.org in /etc/hosts
3. This repo, cloned locally

## Building the images

1. Ensure $HOME/.aws on your host machine contains valid AWS credentials
2. Git pull the Code.org repository as a sub-directory called src:
   1. ```git clone git@github.com:code-dot-org/code-dot-org.git src```
   2. If you don't care about history, you can also do a shallow clone:
   3. ```git clone --depth=1 git@github.com:code-dot-org/code-dot-org.git src```
3. Update src/Gemfile
   1. Remove mini_racer gem (I really don't think we use this any more)
   2. Update unf_ext to 0.0.8 (and also update Gemfile.lock unf_ext from 0.0.7.2)
   3. Add gem 'tzinfo-data' to Gemfile
4. Update src/config/development.yml.erb
   1. Set db_writer to 'mysql://root:password@db/'
5. ```docker compose build``` to build both the web and db containers

## Setting the AWS OAUTH_CODE (required first time)

1. Start the containers:
   1. ```docker compose up```
2. Connect to the Web container:
   1. ```docker exec -ti web /bin/bash```
3. Configure AWS credentials
   1. ```cd /app/src```
   2. ```bin/aws_access```
   3. If prompted, copy and paste the URL into a separate browser window and copy the returned OAUTH_CODE.
4. Stop the containers
   1. Press CTRL-C in the docker compose window to stop the web and db containers
5. Set the OAUTH_CODE on the host:
   1. ```export OAUTH_CODE=[copied value]```
6. Start the containers again:
   1. ```docker compose up```

## Seeding the db (required first time)

1. Connect to the Web container:
   1. ```docker exec -ti web /bin/bash```
2. Rake install:
   1. ```cd /app/src```
   2. ```bundle exec rake install```

## Building the web package

1. Connect to the Web container:
   1. ```docker exec -ti web /bin/bash```
2. Rake build:
   1. ```bundle exec rake build```

## Running the server

1. Connect to the Web container:
   1. ```docker exec -ti web /bin/bash```
2. Run the dashboard server:
   1. ```bin/dashboard-server```
3. Open web browser and browse to http://localhost-studio.code.org:3000

## Troubleshooting

1. Confirm connection to db container using: mysql -h db -u root -p

