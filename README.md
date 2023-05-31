# Most recent branch is develop

# civic-platform-teamrando
civic-platform-teamrando created by GitHub Classroom

This is the backend for the civic_platform.

- ***The GIT-Workflow is described here: [git-documentation](documentation/git-documentation.md)***
- ***The technical documentation can be found here: [technical-documentation](documentation/technical-documentation.md)***

<h1>Goal</h1>

The civic platform allows users to upload data of different media types (text, image, audio, video, url) and add it to the database. For other users it is then possible to comment on the data, use tags to categorize it and to make bookmarks. The data is not only stored in the database, but used for discussion and to expand the knowledge and interest of the users.
The database is therefore the core of the application.

The data can be used for research, to write an article or to address an important issue in the community and back it up with the collected data.

Features

- a map used with the leaflet library, that visualizes the sigle datapoints.
- the function to fill out forms to collect data and analyze it afterwards

<h1>Permissions</h1>


|                             | Owner         | Admin         | Editor        | Viewer       |
| -------------               | ------------- | ------------- | ------------- |------------- |
| Upload new data record      |  x            |               |               |              | 
| View data record            |  x            | x             |               |x             | 
| Update data record          |  x            |               |               |              | 
| Delete data record          |  x            | x             |               |              | 
| Download data record        | x             |               |               | x            | 
| Comment a data record       | x             |               |               |x             | 
| View a comment              | x             |x              |               |x             | 
| Update a comment            | x             |               |               |              | 
| Delete a comment            | x             |x              |               |              | 
| Tag a data record           | x             |               |               |x             | 
| View a tag                  | x             |x               |               |x             | 
| Update a tag                |               |x              |               |              | 
| Delete a tag                |               |x              |               |              | 
| Make a bookmark on data     | x             |               |               |x             | 
| View a bookmark on data     | x             |               |               |x             | 
| Update a bookmark on data   | x             |               |               |              | 
| Delete a bookmark on data   |               |x              |               |              | 

