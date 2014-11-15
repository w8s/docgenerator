daüxer
======

Daüxer is a web application that dynamically presents system requirements documentation directly from issue trackers and wikis. 

Currently, Daüxer only supports Fog Creek's FogBugz. Plans are in place to support Atlassian's Jira and Confluence.

Point Daüxer at your instance of FogBugz, and it will pull specific requirements, and wiki entries to generate a requirements document.

*This project is volatile and subject to frequent change.*

## Configuration

Currently, edit line 12 in `dauxer.py` to be a list of the projects you would like to pull from your FogBugz instance.

Also, edit lines 4-5 with the URL and Token needed to access the FogBugz API.