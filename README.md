# ChennaiLoco

[![Build Status](https://travis-ci.org/digi0ps/ChennaiLoco.svg?branch=master)](https://travis-ci.org/digi0ps/ChennaiLoco)
[![Coverage Status](https://coveralls.io/repos/github/digi0ps/ChennaiLoco/badge.svg)](https://coveralls.io/github/digi0ps/ChennaiLoco)
[![Updates](https://pyup.io/repos/github/digi0ps/ChennaiLoco/shield.svg?token=395e8e90-8e77-45a5-9b2f-ca308d4bc61a)](https://pyup.io/repos/github/digi0ps/ChennaiLoco/)
[![Python 3](https://pyup.io/repos/github/digi0ps/ChennaiLoco/python-3-shield.svg?token=395e8e90-8e77-45a5-9b2f-ca308d4bc61a)](https://pyup.io/repos/github/digi0ps/ChennaiLoco/)

## A short introduction
This project ( or as we call it the Chennai Loco ) deals with creating a web app for storing a huge database of the schedules of Chennai Electric trains and providing users a simple and an easy interface for searching the schedules of the Trains and also viewing details of each Train and Station ( with user ratings and reviews ). 


## Architecture 
### Backend

We are using Django, the Python framework as our backend. As Python being a high level language, Django follows the same principles of it by making the developer work easier with abstraction of complex workings.

### Database

Currently we are using an SQLite database in our development stage. We will soon be migrating to Postgres when we shift to production. There lives 6 relations in the database:


- Train - details about each train.
- Station - details about each station.
- Route - a relationship table between Train and Station storing arriving and departing time at each station of every train.
- StationReview - review about the station (linked to station via foreign key)
- User - details about each user and his password

### Frontend

We are using HTML, CSS along with the help of Bootstrap for all the frontend design and Javascript/jQuery for all the scripting. Although we plan on using a modern web framework and design such as React.js or Google MDL after Review 2. 
## Modules 
### Home Page

The home page gives a quick intro to our site so that the user can quickly start using it

### Search Tab

This is the most important function of the web app. It allows the users to search information about Chennai Train services. In search you have a number of options to search by.

*Train between Stations* - This option searches trains between stations.

*Train* - This option allows the users to search by the train number.

*Station* - Similar to the previous one this option allows the user to search by station name.

### Trains Tab

This lists all the train currently in the database.

### Stations Tab

This lists all the stations currently available in the database.

