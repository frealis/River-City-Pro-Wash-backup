
# River-City-Pro-Wash

*Website for a power washing company*

- This website was built using Django and uses a Postgres database. It has also been tested using Docker with Windows 10 (Home) and Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/) which uses Oracle VM Virtualbox, and -not- Microsoft's Hyper-V.


# Run the Web Application

- To start the web application locally, navigate to the root directory (which contains manage.py) and run:

  $ python manage.py runserver

  ... and the website should be accessible at 127.0.0.1:8000. Alternatively, to run the web application using a Dockerfile, navigate to the root directory (which contains docker-compose.yml) and run:

  $ docker-compose up

  ... and the website should be accessible at 192.168.99.100:8000 (on Windows machines). However, there are a lot of caveats with running the web application from a Docker image which are explained below.


# Docker

- (4/3/2019) Docker's _Getting Started_ guide states: "Pull and run the image from the remote repository. From now on, you can use docker run and run your app on any machine with this command:

  $ docker run -p 4000:80 username/repository:tag

  ... If the image isn’t available locally on the machine, Docker pulls it from the repository." 
  
  ... Trying this with a Django application will pull a copy of the image from an online repository (if the image is not already available on the local drive) from https://hub.docker.com, but it will -not- automatically launch the application. This is regardless of whether or not a Postgres database is set up, or the port is mapped correctly on the command line (ie. 8000:8000 is my guess), or if it's something else. However, docker compose does work:

  $ docker-compose up

  ... when trying to launch the web app from a docker image. However, you maybe have to run it twice: run it, then Ctrl+C (kill) it, and then run it again. I'm not sure if this has to do with setting up a container and creating a Postgres database with the necessary tables for migration first, or if it's something else. 

- This web app has been tested through Docker by launching an image and using a single container on a single virtual machine (a default machine that can be set up using the Docker Quickstart Terminal for Docker Toolbox), but swarms/services/stacks/nodes have not been tested. To view any existing virtual machines:

  $ docker-machine ls

- When deciding whether to launch the application via manage.py or docker-compose, you have to make appropriate database settings adjustments in order to use Postgres; Docker, when set to create a Postgres database through docker-compose.yml, will initially create a database named 'postgres' (which is why you probably have to set the 'NAME': attribute of the DATABASE settings in settings.py to 'postgres', at least initially). To test this out, make sure that all images and containers are deleted from your local machine (run these following commands from any directory, it doesn't matter):

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


# Social Media Icon Credits

- Instagram
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Yelp
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Twitter
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>