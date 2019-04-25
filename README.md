
# River-City-Pro-Wash

*Website for a power washing company*

- This website was built using Django and uses a Postgres database. It has also been tested using Docker with Windows 10 (Home) and Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/) which uses Oracle VM Virtualbox, and -not- Microsoft's Hyper-V.


# Run the Web Application Locally

- To start the web application locally, navigate to the root directory (which contains manage.py) and run:

  $ python manage.py runserver

  ... and the website should be accessible at 127.0.0.1:8000. 

- To start the web application locally using the Heroku Local CLI plugin:

  $ heroku local web -f Procfile.windows

  ... and the website should be accessible at localhost:5000.
  
- Alternatively, to run the web application using a Dockerfile, navigate to the root directory (which contains docker-compose.yml) and run:

  $ docker-machine start default          // start up a virtualbox named 'default'
  $ docker-machine env                    // make sure environment variables exist
  $ docker-machine regenerate certs default // do this if prompted for new certs
  $ docker-compose up

  ... and the website should be accessible at 192.168.99.100:8000 (on Windows machines). However, there are a lot of caveats with running the web application from a Docker image which are explained below.

- Local environment variables are managed using dotenv https://github.com/theskumar/python-dotenv.


# Docker

- (4/3/2019) Docker's _Getting Started_ guide states: "Pull and run the image from the remote repository. From now on, you can use docker run and run your app on any machine with this command:

  $ docker run -p 4000:80 username/repository:tag

  ... If the image isn’t available locally on the machine, Docker pulls it from the repository." 
  
  ... Trying this with a Django application will pull a copy of the image from an online repository (if the image is not already available on the local drive) from https://hub.docker.com, but it will -not- automatically launch the application. This is regardless of whether or not a Postgres database is set up, or the port is mapped correctly on the command line (ie. 8000:8000 is my guess), or if it's something else. However, docker compose does work:

  $ docker-compose build    // create a docker image
  $ docker-compose up

  ... when trying to launch the web app from a docker image. However, you maybe have to run it twice: run it, then Ctrl+C (kill) it, and then run it again. I'm not sure if this has to do with setting up a container and creating a Postgres database with the necessary tables for migration first, or if it's something else. 

  ... also, if you make any changes (ex. added new dependencies in requirements.txt), you have to create a new docker image in order to reflect those changes via:

  $ docker-compose build

- This web app has been tested through Docker by launching an image and using a single container on a single virtual machine (a default machine that can be set up using the Docker Quickstart Terminal for Docker Toolbox), but swarms/services/stacks/nodes have not been tested. To view any existing virtual machines:

  $ docker-machine ls

- When deciding whether to launch the application via manage.py or docker-compose, you have to make appropriate database settings adjustments in order to use Postgres; Docker, when set to create a Postgres database through docker-compose.yml, will initially create a database named 'postgres' by default (which is why you probably have to set the 'NAME': attribute of the DATABASE settings in settings.py to 'postgres', at least initially). To test this out, make sure that all images and containers are deleted from your local machine (run these following commands from any directory, it doesn't matter):

  $ docker rm $(docker ps -a -q)    // Remove all containers
  $ docker rmi $(docker images -q)  // Remove all images

  ... and then navigate to the root directory of your Django web application and run:

  $ docker-compose up

  ... after awhile you'll see something like "2019-04-03 04:50:35.270 UTC [50] LOG:  database system was shut down at 2019-04-03 04:50:34 UTC". Next, get the 'postgres' image's CONTAINER ID, sneak into the container, access the postgres database, and see all of the containerized databases by running:

  $ docker container ls
  $ docker exec -it <CONTAINER ID> bash -l  // CONTAINER ID for postgres IMAGE
  root@<CONTAINER ID>:/# psql -U postgres
  postgres=# \l

  ... once you're done with looking at this, Ctrl+Z out of there and then Ctrl+C (kill) whichever terminal is currently running the dockerized instance of the web application. Wait for the application to stop (or alternatively, you can go into another terminal and run $ docker-compose down) and then run $ docker-compose up again. Hopefully at this point you get yellow text that reads "... exited with code 0."
  
  ... however, you might get an error code in yellow text that reads "... exited with code 1." which may have something to do with recently being inside of the database's container. If so, just Ctrl+C and run $ docker-compose up again.

- To login to the www.rivercityprowash.com/admin console while the application is running in a dockerized container, you'll have to create a user with both a username and a password -- when the database is set up in the docker container, it doesn't have a password by default because no password is specified in settings.py. 


# Deploy to Heroku

- Heroku has a free service that can host 1 website at a time on what they refer to as a "dyno". It doesn't offer much processing power (something like 512 MB of RAM) and will basically turn the dyno off after 30 minutes or so of inactivity, but will turn back on with a subsequent HTTP request, although there is a lag time of 10 to 20 seconds for the dyno to start up again.

- The nice thing about Heroku is that you can deploy it from the command line, and each deployment gets assigned a version number. Since each version is basically a git file, you can easily rollback to older versions or use other commands like 'git diff' to compare different versions:

  $ heroku releases         // view the past 15 or so web app versions
  $ heroku rollback v#      // rollback to a specific version, ex. v1, v3, etc.
  $ git diff # #            // # # represent two different deploys

- https://devcenter.heroku.com/articles/django-app-configuration
- https://medium.com/agatha-codes/9-straightforward-steps-for-deploying-your-django-app-with-heroku-82b952652fb4

- To run locally via heroku:

  $ heroku local web -f Procfile.windows

  ... which runs at localhost:5000

- To upload to git/deploy and view online:

  $ git push heroku master
  $ heroku ps:scale web=1 (to make sure at least 1 web dyno is running)
  $ heroku open

  ... note: when you push a web app to heroku, only the 'master' branch takes effect. Pushing code from any other branch is ignored by Heroku.

- When you set DEBUG = False and push this app to production, it will give a 500 error unless the ALLOWED_HOSTS =[] in settings.py includes the URL where this site is hosted. Some people also think that not having collected static files or not migrating the database may also produce this error. To do both:

  $ python manage.py collectstatic
  $ git push heroku master (to push static files to Heroku server)
  $ heroku run python manage.py migrate (to apply migration files)

  ... to troubleshoot:

  $ heroku logs --tail      // show recent logs
  $ heroku releases         // show recent heroku releases, denoted v#, ex. v3
  $ heroku rollback         // rollback to previous release
  $ heroku rollback v#      // rollback to v#, ex. v10, v33, etc.
  $ git diff # #            // compare previous heroku git commits by deploy #

  ... also note: if you have static files in the templates, ie. {% static 'whatever' %}, and they are commented out via HTML comment tags, they are still visible to the program and can cause issues, especially when Debug = False.

- When altering models.py locally and updating your local database via:

  $ python manage.py makemigrations
  $ python manage.py migrate

  ... you are basically a) creating a migration file with SQL instructions, and b) applying those instructions to alter the database. Heroku has analogous commands:

  $ heroku run python manage.py makemigrations
  $ heroku run python manage.py migrate

  ... however, as long as you push your migration files from the /migration folder to Heroku, you can omit running the first command (makemigrations).

- Heroku environment variables can be viewed and set via:

  $ heroku config                 // view environment variables on heroku server
  $ heroku config:set key=value   // set environment variables on heroku server

- To connect to the Heroku Postgres database from the command line:

  $ heroku pg:psql
  
  1. https://devcenter.heroku.com/articles/heroku-postgresql


# Deploy to AWS

- Web apps deployed on AWS exist in their own environment. New applications and their environments can be created either from the AWS console or from the command line. AWS has two types of command lines -- awscli (the general all-purpose AWS command line) and awsebcli (the Elastic Beanstalk web development command line). 

- AWS has a free tier that is available for 12 months, and this basically allows for 1 website to be deployed at all times. This website will exist in an environment that can be shut off if needed -- terminating the environment will -not- terminate the application, but it will save on the allotted free tier hours that are granted each month for the first 12 months, so it's a good idea to turn it off when it's not needed. To view, get the status, and terminate an environment:

  $ eb list         // list environments, -a or -all to view all, * marks active
  $ eb use <env>    // switch between environments
  $ eb status       // get detailed information on current environment
  $ eb terminate    // terminate current environment

  ... in contrast to Heroku, where changes are pushed via git and have to be pushed from the 'master' branch, changes in AWS are deployed by packaging all of the application's files into a *.zip file from a) the current directory if it has been set up with the EB CLI , or b) the current git branch if git has been set up. Once the file has been zipped up, they get sent to an Amazon S3 bucket and then to an AWS environment. 
  
  ... when updating the AWS site from a git repository, if you make changes to your current branch and do not commit them, then they will not be deployed to AWS using CLI commands.

- To deploy from the command line, basically you have to create a new folder called .ebextensions and add a configuration file to it called django.config with some code that can be found in the link below. The main commands involved with deploying an application using AWS Elastic Beanstalk are:

  $ eb init         // initializes the EB CLI in the current directory
  $ eb deploy       // packages web app as *.zip and sends to online AWS env
  $ eb open         // opens the web app in a browser

  1. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

- AWS looks for static files generated by python manage.py collectstatic specifically in a folder called static/ located in the root directory of the project. It has to be static/, not staticfiles/. This requirement could be due to a configuration setting in nginx, Apache, or whatever runs a Python AWS server.

- To set and view environment variables (aka 'Environment Properties'):

  $ eb setenv key=value     // set a key=value environment variable
  $ eb printenv             // view environment variables

  ... to use environment variables in AWS vs. Heroku (with python-dotenv installed):

  > SECRET_KEY = os.getenv("SECRET_KEY")    # heroku (using python-dotenv)
  > SECRET_KEY = os.environ["SECRET_KEY"]   # aws

    1. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-container.html?shortFooter=true
    2. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html?icmpid=docs_elasticbeanstalk_console
    3. http://docs.python.org/library/os.html.

- To switch AWS accounts from the command line you can use "Named Profiles". Navigate to C:/Users/<username>/.aws/ and modify the credentials file in order to add additional named profiles. For example:

  [profile eb-cli]
  aws_access_key_id = XXXXXXXXXXXXX
  aws_secret_access_key = XXXXXXXXXXXX

  [profile eb-cli2]
  aws_access_key_id = XXXXXXXXXX
  aws_secret_access_key = XXXXXXXXXXXX

  ... then initialize a new elastic beanstalk application (or select one that already exists):

    $ eb init --profile <profile name> <application name, optional>

  ... or change the default named profile if the above command doesn't work:

    $ set AWS_EB_PROFILE=<profile name>

  1. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-configuration.html#eb-cli3-profile
  2. https://stackoverflow.com/questions/29190202/how-to-change-the-aws-account-using-the-elastic-beanstalk-cli

- To enable HTTPS with AWS Elastic Beanstalk in production, you have to:

  1. Own a registered domain
  2. Have an authenticated server certificate stored in the AWS Certificate Manager
    a. Generate the certificate with the AWS Certificate Manager (ACM)
    b. Generate the certificate somewhere else (OpenSSL)
  3. Assign the certificate to the environment's load balancer

  ... for development purposes, you can generate a self-signed certificate (aka a test certificate); however, if used in production then anyone who visits the site will get a warning that the site is unsafe. 

  ... note (4/21/19): with Django, if you set SECURE_SSL_REDIRECT=True within the settings.py file an upload/deploy that file without having the load balancer configured to listen for https connections on port 443 then the AWS Elastic Beanstalk application gets irreversibly screwed up, meaning that a GET request/visiting the page will hang and time out, even if you change the setting back to SECURE_SSL_REDIRECT=False. The only way that I know how to fix this is to erase the AWS Elastic Beanstalk application (the one created via eb init) and completely start over.

  1. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https.html
  2. https://aws.amazon.com/certificate-manager/

- To set up AWS Simple Email Service (SES) you have to jump through a ton of hoops:

  1. Install boto3, which is a Python package/module, and test it out.
    > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html

  2. Implement some kind of process to handle email bounces and complaints.
    > http://docs.aws.amazon.com/ses/latest/DeveloperGuide/bounce-complaint-notifications.html
    > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/bouncecomplaintdashboard.html

  3. Create a support ticket to move out of the Amazon SES "Sandbox" and increase your SES sending limits, which includes sending emails to addresses that have not been verified on your account (which is basically any customer's email address).
    > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html

  4. Grant permission for your Elastic Beanstalk default instance profile, aka "aws-elasticbeanstalk-ec2-role", to send emails. This can also be used on any IAM account instead if you're playing it safe and using an IAM account instead of your root user account. Anyways, to do this, you have to add the "AmazonSESFullAccess" policy to whichever instance profile/account you're using, or create a custom policy that does the same thing.
    > https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/iam-instanceprofile.html#iam-instanceprofile-addperms
    > https://docs.aws.amazon.com/ses/latest/DeveloperGuide/control-user-access.html

  5. Verify the domain that the email is coming from -- I'm not exactly sure if this is necessary, but if you go to the SES console you can verify domains from there.

- To connect to a Postgres database from the command line or pgadmin, you have to make it public (which involves a VPC, or "virtual private cloud", and a subnet). To access from the CLI:

  $ psql --host=<DB instance endpoint> --port=<port> --username=<master user name> --password --dbname=<database name> 

  ... dbname is "postgres" by default.
  
  1. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html
  2. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreatePostgreSQLInstance.html
  3. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Non-VPC2VPC

- To SSH into an AWS instance, the instance has to support ssh and the VPC has to allow the connection (from some IP, I think?). Anyways, the first time you try to connect, you might get a connection error. AWS seems to record this error and add your IP address (or whatever it is) to a list of "known hosts" so that you can connect on the next attempt. Related CLI commands:

  $ eb ssh --interactive    // re-create instance settings to include SSH
  $ eb ssh                  // SSH into the instance once things are working

  1. https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-ssh.html


# Generate a new random SECRET_KEY

- https://foxrow.com/generating-django-secret-keys


# Social Media Icon Credits

- Instagram
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Yelp
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Twitter
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>