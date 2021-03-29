# REST_api_yandex


## 1) activate venv 
> source yandex_linux/bin/activate
___
## 2) install required libraries
> pip install -r /path/to/requirements.txt
### run deploy databases script
> python deploy.py
___
## 3) deactivate venv
> deactivate
___
## 4) wsgi entry point setup
> nano ~/REST_api_yandex/app.ini
### write:
```
[uwsgi]
module = wsgi:app

master = true
processes = 4

socket = app.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```
### Save and close.
___
## 4) create service for wsgi
> sudo nano /etc/systemd/system/app.service

### write:
```
[Unit]
Description=uWSGI instance to serve app
After=network.target

[Service]
User=entrant
Group=www-data

WorkingDirectory=/home/entrant/REST_api_yandex
Environment="PATH=/home/entrant/REST_api_yandex/yandex_linux/bin"
ExecStart=/home/entrant/REST_api_yandex/yandex_linux/bin/uwsgi --ini app.ini


[Install]
WantedBy=multi-user.target
```
### Save and close.
___

## 5) run and activate service
> sudo systemctl start app
> sudo systemctl enable app
___
### check app service(must be active)
> sudo systemctl status
___
## 6) install ngix
> sudo apt update
> sudo apt install nginx
> sudo ufw app list
> sudo ufw allow 'Nginx HTTP'
> sudo ufw status
___
## 7) setup ngix
> sudo nano /etc/nginx/sites-available/app

### write:
```
server {
listen 0.0.0.0:8080;

location / {
    include uwsgi_params;
    uwsgi_pass unix:/home/entrant/REST_api_yandex/app.sock;
           }
}
```
### Save and close.
> sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

### errors check:
> sudo nginx -t
### if no errosrs:
> sudo systemctl restart nginx
> netstat 0.0.0.0:8080
