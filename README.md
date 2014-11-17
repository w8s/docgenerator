daüxer
======

Daüxer is a web application that dynamically presents system requirements documentation directly from issue trackers and wikis. 

Currently, Daüxer only supports Fog Creek's FogBugz. Plans are in place to support Atlassian's Jira and Confluence.

Point Daüxer at your instance of FogBugz, and it will pull specific requirements, and wiki entries to generate a requirements document.

*This project is volatile and subject to frequent change.*

## Configuration

Edit lines 4-5 with the URL and Token needed to access the FogBugz API.

## Getting Started

    vagrant up

This will initialize the vagrant box and start two docker containers comprising the application: one running mongodb, and one running the flask app.

## Dependencies

* [Flask](http://flask.pocoo.org/)
* [Python FogBugz API Wrapper](https://pypi.python.org/pypi/fogbugz/)
