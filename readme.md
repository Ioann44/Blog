# Blog flask+postgreSQL site

## Start up
To start this project you need:
- create `.env` form `.env.example` and fill empty fields (The DEBUG field better left blank)
- (optional) `docker build -t blog-flask-app . --network host`, may help if something wrong with docker DNS
- in project directory run `docker-compose up`

By default, site will be available on `localhost:5000`

## Author
Made by Yashin Ivan
