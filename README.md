# Build a URL Shortener

## URL shortening service

Build a URL shortening service (like [bit.ly](https://bit.ly)).

## Backend
### Tech
- python
- pymongo
- pytest (for testing)

### How to start (non-Docker)
`cd /src` 

`py app.py`

### Alternatively (Docker)
There is already a Dockerfile in `/src`, we have to build and run the image. 
`cd /src` 

`docker build -t url-shortener .`

`docker run <insert your docker image id>` (This can by found by running `docker images`)


## Frontend
### Tech
- ReactJS
- Bootstrap

### How to start
`cd /client`

`npm start`
