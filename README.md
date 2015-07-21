docgenerator
======

`docgenerator` is a web application that dynamically presents system requirements documentation directly from issue trackers and wikis. 

Currently, `docgenerator` only supports Fog Creek's [FogBugz](http://www.fogcreek.com/fogbugz/).

Point `docgenerator` at your instance of FogBugz, and it will pull specified requirements, and wiki entries to generate a requirements document artifact.

## Configuration

In `/src/app/integration/ifogbugz.py`, edit lines `5, 6` with the URL and Token needed to access the FogBugz API.


## Getting Started

    vagrant up

This will initialize a vagrant box and start a docker container running the flask app.

## Dependencies

The dependencies are included in the Vagrant configuration. 

* [Flask](http://flask.pocoo.org/)
* [Python FogBugz API Wrapper](https://pypi.python.org/pypi/fogbugz/)

## Other Resources

[Slides from ConFoo presentation](https://drive.google.com/open?id=0B51wD4VXm0XyMTR3aUlRcmdtRWM&authuser=0) 
