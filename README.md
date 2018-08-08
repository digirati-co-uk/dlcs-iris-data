# DCS Iris Session Data Library

This library provides a simple session data storage system for DLCS Text Pipeline services.
It wraps the S3 provider from the iris-data project (https://github.com/digirati-co-uk/iris-data) and provides some simple but useful utility and consistency on top of it. 


### Installation


* (optional: create virtual environment)
* ``` pip install -r requirements.txt ```
* create or edit iris_settings.py including an "IRIS_SESSION_BUCKET" property

