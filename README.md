# Nirvana Health API

This API has one endpoint that allows the user send a member id and get a response with insurance data from that member.

It is built in python with FastAPI, in a docker container and loaded with docker-compose.

The API performs a GET request to three different APIs to get insurance informacion from a member id. Then, the information is processed and if the values that result from the APIs are different, the most common or repeated value for each key (deductible, stop loss and oop max), is selected and returned.

Validation is also performed on each field, per business rules, we want to reject deductible values higher thant oop max and oop max higher thant stop loss.

Ideally, I would have made the data gotten from the APIs persistent with a mongo.db database; this would allow me to make a function to determine a coefficient for each API. This coefficient would have been calculated on each response, and averaged with all previous results, allowing me to set a confidance level on each API. This would allow me, over time, to select the "most trusted" API to get results from.

## Repository structure

```
.
├── app
│   ├── config.py
│   ├── controller.py
│   ├── __init__.py
│   ├── logging.conf
│   ├── main.py
│   ├── models.py
│   ├── routers.py
│   └── test_main.py
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation
### Install Docker and Docker Compose

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Run FastAPI

Linux: From nirvana folder

```sh
sudo docker-compose up -d
```

## Usage example

http://localhost:8000/insurance/?id=1

## Testing

```sh
pytest


## License

This project is licensed under the terms of the MIT license.
