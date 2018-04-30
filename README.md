# Quizzing_webapp
An online quizing web app, including single challenging mode, as well as 1 v 1 challenging mode.

Instructions to run this app:

## 1. Through AWS

I have deployed this application to AWS platform, users can access the app by inputting URL: http://ec2-35-173-229-36.compute-1.amazonaws.com. And this is also the suggested way to check the project result.

## 2. Run on the localhost:

There are several modules should be installed before run:
#### Install flask, pymongo, flask_socketio, operator :

```
pip install flask
pip install pymongo
pip install flask_socketio
pip install operator
```

#### Install asynchronous framework: eventlet
```
pip install eventlet
```

#### Prepare the mongoDB environment:

```
export PATH=<path of project file>/Quizing_webapp/mongodb/bin:$PATH
mongod --dbpath <path of project file>/Quizing_webapp/mongodb/data/db
```

#### Run the app using flask web server (Note):
```
python3 <path of project file>/Quizing_webapp/www/app.py
```


Note: attach the config file if running on Nginx if you need.
```
#user  nobody;
worker_processes  1;

events {
worker_connections  1024;
}

http {
include       mime.types;
default_type  application/octet-stream;
sendfile        on;
keepalive_timeout  65;
server {
listen       80;
server_name  localhost;

location / {
include proxy_params;
proxy_pass http://127.0.0.1:8000;
}
location /socket.io {
include proxy_params;
proxy_http_version 1.1;
proxy_buffering off;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "Upgrade";
proxy_pass http://127.0.0.1:8000/socket.io;
}
}
include servers/*;
}
```

Again, aws url is more recommended, because it is well deployed with nginx and gunicorn, as well as supervisor.

