# serverBKU
deploy heroku
pip install --upgrade --force virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
New-Item .gitignore Procfile README.md requirements.txt runtime.txt
pip install Flask
Procfile:web: gunicorn app:app
.gitignore:*.pyc
runtime.txt:python-3.7.4
pip install gunicorn
pip freeze > requirements.txt

Deploy heroku

git init
git add .
git commit -m "complete"
heroku create
heroku config:set MONGO_URL=mongodb+srv://tuantran:chinhlatoi1@cluster0-gtudj.mongodb.net/test?retryWrites=true&w=majority
git push heroku master
heroku ps:scale web=1
heroku ps
heroku open
