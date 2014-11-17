FROM ubuntu:trusty
MAINTAINER cacois@gmail.com

# Update stuff
RUN apt-get update

# Install Python Setuptools
RUN apt-get --no-install-recommends install -y python-setuptools build-essential python-dev libpq-dev ca-certificates

# Install NPM and Bower
RUN apt-get --no-install-recommends install -y nodejs npm
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g bower

# Install pip
RUN easy_install pip

ADD requirements.txt /tmp/requirements.txt

# Install requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000

VOLUME ["/src"]
WORKDIR src

ENTRYPOINT ["python", "/src/run.py"]
CMD ["runserver"]
