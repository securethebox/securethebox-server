# Build docker image
```
docker build . -t securethebox-server
```

# Run docker image and get shell (service starts automatically)
```
docker run -it securethebox-server:latest /bin/bash
```

# Run app.py manually
```
./venv/bin/python3.7 app.py
```

# Mount local directory to Docker home
- mac
```
docker run -it -v $(pwd):/home/securethebox-server securethebox-server:latest /bin/bash
```
- windows
```
docker run -it -v $(%cd%):/home/securethebox-server securethebox-server:latest /bin/bash
```