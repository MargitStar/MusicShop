# Name
Music App

# Description
Music App is Django Rest Framework backend.
It allows you to:
1. Download music
2. Upload music
3. Make playlists
4. Add music to playlists
5. Filter music by artist, genre, release date and title


# Installation
2. Install `Python3`, `Docker`, `PostgreSQL`
4. Run `docker-compose up -d`
5. Add `.env` file, that has to include: `MUSIC_SHOP_DB_NAME`,
   `MUSIC_SHOP_DB_USER`, `MUSIC_SHOP_DB_PASSWORD`,
   `MUSIC_SHOP_DB_HOST`, `MUSIC_SHOP_DB_PORT`,
   `MUSIC_SHOP_SECRET_KEY`, `MUSIC_SHOP_ALLOWED_HOSTS`
6. Install `poetry` using `pip3 install poetry`
7. Install all project dependencies using `poetry install`
8. Apply all migrations using `poetry run python manage.py migrate`
9. Run project using `poetry run python manage.py runserver`
10. To see documentation of API go to `http://0.0.0.0:8000/swagger/`
11. Now you can start using MusicShop API

# Support
 You can contact me using email `sovenokbymargo@mail.ru`. I'd be happy to help you
