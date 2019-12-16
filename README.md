# Navegg Back-end Challenge - Create an API

The general purpose is receiving a list of websites and organize this information to classify and store all the details of the website.  
### Project

This was made using Django and Django REST Framework

### Setup

Install the depencies

```sh
$ pipenv shell
$ pipenv install
```

Migrate the databse

```sh
$ cd navegg
$ ./manage.py migrate
```
To populate the database with the CSV data
```sh
$ ./setup
```

To start the server
```sh
$ ./manage.py runsever
```


### API endpoints:
    GET:    /item/ -> list all active register in the database.
    GET:    /item/[id]/ -> list one register.
    POST:   /item/ -> create new register.
    PATCH:  /item/[id]/ -> modify register
    DELETE: /item/[id]/ -> remove register


## POST and PATCH JSON Example
```json
{
	"name":"Site Name",
	"url": [
		{"description": "name.com"}, 
		{"description": "name.com/name1"}
	],
	"category": [
		{"description":"name"},
		{"descritpion":"name2"}
	]
}
```

## How long it took for you to get it done

Took about 8 hours of development

## What you would add/change if you had more time?
-   Refactor the serializers.py for readbility
-   Create endpoints to control category and URL separately
-   User authentication and restricted access to modify and create