
# Maze solver

## Install
### Install pipenv

This project uses `pipenv`to handle dependencies and virtual environments. Make sure you have [pipenv](https://github.com/pypa/pipenv#installation) installed before proceeding.

### Install dependencies 
```
cd mazesolver
pipenv install
```

## Solve maze

### 1) Store maze in `static/`
Store the file of the maze to be solved in `static/` or use one of the files already there in the next steps

### 2) Open shell
```
pipenv shell
```
### 3) Run main.py from shell
You can either pass the filename of the file stored in `static` as a command line argument. Example:

```
python src/main.py board-1-1.txt
```

**OR**

passing the file name in the prompt. Example:

```
python3 src/main.py
> file name >>> board-1-1.txt
```


## Run tests
coverage run tests/tests.py

coverage report
coverage report -m

coverage html

