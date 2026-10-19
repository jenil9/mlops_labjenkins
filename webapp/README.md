# Run the microservices with Docker CLI

Run these commands from the `microservice` directory (the parent of `webapp`
and `dbapp`). No Docker Compose file is needed.

Build both images:

```bash
docker build -t iris-db ./dbapp
docker build -t iris-web ./webapp
```

Create a Docker network so the web container can reach the database container
by name, and a named volume for persistent SQLite data:

```bash
docker network create iris-network
docker volume create iris-prediction-data
```

Start the database container first:

```bash
docker run -d \
  --name dbapp \
  --network iris-network \
  -p 5002:5002 \
  -v iris-prediction-data:/app/instance \
  iris-db
```

Start the web container:

```bash
docker run -d \
  --name webapp \
  --network iris-network \
  -p 5001:5001 \
  -e DB_API_URL=http://dbapp:5002 \
  iris-web
```

Open <http://localhost:5001> to make a prediction and
<http://localhost:5001/show_records> to view saved predictions. The named
volume mounted at `/app/instance` keeps the database when containers are
removed and recreated.

Stop and remove the containers without deleting saved records:

```bash
docker stop webapp dbapp
docker rm webapp dbapp
```

To also delete the stored database, remove the volume explicitly:

```bash
docker volume rm iris-prediction-data
```

When finished, the Docker network can be removed with:

```bash
docker network rm iris-network
```
