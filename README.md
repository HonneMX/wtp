# wtp
EN

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

RU

Проект создан с целью предоставить песочницу для начинающих тестировщиков, что бы познакомится с принципов работы WEB сайта API и Базы Данных. Все эти три слоя разворачиваются двумя командами 

из корня репозитория 
docker-compose build
docker compose up

Это позволит поднять web сайт на локальной машине порт 3000
API развернется на локальной машине на 8080 порту. API написана с помощью FastAPI для открытия списка методов можно воспользоватся приставкой /docs (http://localhost:8080/docs#/)
База данных развернута на локальной машине порт 5432 
