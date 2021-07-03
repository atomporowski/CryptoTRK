# CryptoTRK

## Setup & Installtion


```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python3 app.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`


##Setting up Docker
building app
```bash
docker build -t crypto-trk .
```

This app is configured to run in Docker container.
```bash
docker run -t -d -p 5000:5000 crypto-trk
```
To get into docker container
```bash
docker exec -it <id> bash
```
Checking logs
```bash
docker logs <id>
```

##Running tests
```bash
pytest tests.py -vvv
```
