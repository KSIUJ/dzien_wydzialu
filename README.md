# Initial environment setup
```
mkvirtualenv -p /usr/bin/python3.4 dzien_wydzialu
cd /vagrant
pip install -r requirements.txt
```

# Development deployment
```
cd /vagrant
workon dzien_wydzialu
./manage.py migrate
./manage.py runserver_plus 0.0.0.0:8000
```