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
docker run -it -v $(pwd):/home/securethebox-server securethebox-server:latest /bin/bash
```
- windows
```
docker run -it -v $(%cd%):/home/securethebox-server securethebox-server:latest /bin/bash
```