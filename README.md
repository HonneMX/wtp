# wtp
The project was created to provide a sandbox for novice testers to get acquainted with the principles of the WEB site API and Database. 
All these three layers are deployed by two commands 
From the repository root 
docker-compose build
docker compose up

This will raise the web site on the local machine port 3000
The API will be deployed to the local machine on port 8080. 
The database is deployed on the local machine port 5432


The API is written with FastAPI and you can use the /docs prefix (http://localhost:8080/docs#/) 
to open a list of methods
