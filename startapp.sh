docker network create my-network
docker container run -d --name mongodb -p 27017:27017 --network my-network mongo:6.0  
docker build . -t restapi:0.1.0
docker container run --name fastapi-app2 -d -p 8000:8000  --network my-network restapi:0.1.0