# Timbal Build

1. Ensure $HOME/.aws on the host contains valid AWS credentials
2. Delete ./data directory (for clean db)
3. Delete ./rbenv directory (for clean gems)
4. Git pull the ./src directory
5. Update the Gemfile
   1. Remove mini_racer gem
   2. Update unf_ext to 0.0.8 (and update Gemfile.lock unf_ext also)
6. Update config/development.yml.erb
   1. Set db_writer to 'mysql://root:password@db/'
7. ```docker compose up``` to build the web and db containers
8. Once images are running:
   1. Connect to the web tier: docker exec -ti web /bin/bash
   2. Confirm connection to db container using: mysql -h db -u root -p
   3. Bundle install
      1. gem install bundler -v 1.17.3
      2. cd app/src
      3. bundle install
   4. Configure AWS Credentials
      1. export AWS_PROFILE=cdo
      2. bin/aws_access - copy the URL provided to get the OAuth code
      3. export OAUTH_CODE=[returned code]
      4. bin/aws_access again - should return with the right developer id
   5. Confirm hooks can be installed with: bundle exec rake install:hooks
   6. Install tzinfo-data (required for bundle install)
      1. Edit Gemfile. Add gem 'tzinfo-data' anywhere in file
      2. Run bundle install to add the new gem
   6. bundle exec rake install

