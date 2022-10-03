purpose:
        web application for handling database of restaurants and its menus

engine: python==3.7
        flask==2.2.2 (+ jinja2==3.1.2)
        sqlalchemy==1.4.41

initialization (first time):
        not needed, application check create, initialized DB

running (all times):
        python webserver_flask.py

features:
        functionality to upload logo file (only manual mode)
        default folder static/logos

        API interface for JSON data for following paths:
        /api.restaurants
        /api.restaurants/rst_idN, N - restaurant id
        /api.restaurants/menu_items
        /api.restaurants/news_promo

        in folder there are scripts for local CLI interfaces
         - read_db_rec.py - to read data
         - update_db_rec.py - to update fields by filter criteria
         - delete_db_rec.py - to delete records by filter criteria

known issues:
        5) at upload form button with 'wrong' locale (not English)
        solution: to be found later
        6) no solution to batch input for records and logo file
        solutio: develop functionality later
        *) no JS in HTML templates and application
        solution: to be added on demand and during education

url for using application:
        heroku hosting: http://fm-restaurants.herokuapp.com/restaurants
        localhost:      http://localhost:5000/restaurants

git remote:
        heroku: https://git.heroku.com/fm-restaurants.git
        github: git@github.com:fantom2208/full-stack-rest.git



heroku application setting files:
------------------------------------------------------------------------------
Procfile:
web: python webserver_flask.py

requirements.txt:
flask>=2.2.2
sqlalchemy>=1.4.41

runtime.txt:
python-3.9.14



conde environment list:
------------------------------------------------------------------------------
name: udcty_web37
channels:
  - defaults
dependencies:
  - _libgcc_mutex=0.1=main
  - _openmp_mutex=5.1=1_gnu
  - ca-certificates=2022.07.19=h06a4308_0
  - certifi=2022.9.14=py37h06a4308_0
  - ld_impl_linux-64=2.38=h1181459_1
  - libffi=3.3=he6710b0_2
  - libgcc-ng=11.2.0=h1234567_1
  - libgomp=11.2.0=h1234567_1
  - libstdcxx-ng=11.2.0=h1234567_1
  - ncurses=6.3=h5eee18b_3
  - openssl=1.1.1q=h7f8727e_0
  - pip=22.1.2=py37h06a4308_0
  - python=3.7.13=h12debd9_0
  - readline=8.1.2=h7f8727e_1
  - setuptools=63.4.1=py37h06a4308_0
  - sqlite=3.39.2=h5082296_0
  - tk=8.6.12=h1ccaba5_0
  - wheel=0.37.1=pyhd3eb1b0_0
  - xz=5.2.5=h7f8727e_1
  - zlib=1.2.12=h5eee18b_3
  - pip:
    - charset-normalizer==2.1.1
    - click==8.1.3
    - flask==2.2.2
    - flask-sqlalchemy==2.5.1
    - greenlet==1.1.3
    - idna==3.4
    - importlib-metadata==4.12.0
    - itsdangerous==2.1.2
    - jinja2==3.1.2
    - markupsafe==2.1.1
    - requests==2.28.1
    - sqlalchemy==1.4.41
    - typing-extensions==4.3.0
    - urllib3==1.26.12
    - werkzeug==2.2.2
    - zipp==3.8.1
prefix: /home/fantom_m19/miniconda3/envs/udcty_web37

