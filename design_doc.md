## Google Api Software Requirements

through te google api you can apply:

- CREATE
- UPDATE
- READ
- DELETE
  operations to resources offered by google services, including:
- Youtube
- Gmail
- Google Tasks
- Google Drive
- Google Calendar

### Configure
Firstly, enable the google calendar api https://developers.google.com/calendar/api/quickstart/python 
go onto the https://console.cloud.google.com/apis/credentials/consent?authuser=0&project=learned-vault-319419
dashboard and click on edit app
add the scopes that you want by enabling CRUD operations on a given resource
remove the existing .pickle token and run the script again

Note
---
make sure that the scopes are correct (one you click on them you can see the name of 
the serivce that you are trying to access)
make sure that the version o the application is correct

### General Instructions

link to the api documentation can be found at https://developers.google.com/tasks
refresh the token on the link below if you dont have permission switch to uchekesla account
donwload json and update secret_file
delete the pickle file that you have created
and to renew credentials go to https://console.cloud.google.com/apis/credentials?authuser=1&project=learned-vault-319419

> for gmail api documentation
> https://www.thepythoncode.com/article/use-gmail-api-in-python

create task and task lists types from the response that you get

### Improvements

- refactor out a `EmailMessage` class to build messages and add attachments
- for further improvements you can go to the following video to expand on the functionality of the google calendar API:
https://www.youtube.com/watch?v=_uHd0ypR5OI&list=PL3JVwFmb_BnTO_sppfTh3VkPhfDWRY5on&index=6
- categorise the different events by types so that when you have diferent event types you can give them different colors
depending on the event
- write all the tests and make sure that CRUD methods can be applied to all the resources

### Documentation

the following is a list of the documentation provided by google, to futher understand the system
read the Understanding the API section of the API

#### Google Calendar
__design__
https://developers.google.com/calendar/api/concepts
__documentation__
https://developers.google.com/calendar/api/guides/create-events
#### Google Mail
__documentation__
https://developers.google.com/gmail/api/guides/drafts
#### Google Task Api
__documentation__
https://developers.google.com/tasks/quickstart/python

for more information read the references and the guides to understand the API structure
