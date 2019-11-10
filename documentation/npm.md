# Initialized Commitizen
```
commitizen init cz-conventional-changelog --save-dev --save-exact
```

# Running npm scripts
- Scripts are defined in package.json file
- run: npm run dev
```
"scripts": {
    "dev": "export APPENV=\"DEV\"; venv/bin/python3.7 app.py",
}
```