# Build docker image
```
docker build . -t securethebox-server
```

# Run docker image and get shell (service starts automatically)
```
docker run -it -p 5000:5000 securethebox-server:latest /bin/bash
```

# Run app.py manually
```
./venv/bin/python3.7 app.py
```

# Mount local directory to Docker home (Just use git_scripts.py instead)
- mac
```
docker run --rm -it -p 9090:9090 -v $(pwd):/home/securethebox-server securethebox-server:latest /bin/sh
docker run --rm -it -p 9090:9090 -v $(pwd):/home/securethebox-server airflow /bin/sh
docker exec -it airflow /bin/sh
```
- windows
```
docker run -it -v $(%cd%):/home/securethebox-server securethebox-server:latest /bin/sh
```