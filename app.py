from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLALchemy
import pymysql
import secrets

conn="mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db=SQLALCHEMY(app)

class Pokemonindex(FlaskForm):
    national_index=StringField('National index number:',validators=[DataRequired()])
    name=StringField('name:',validators=[DataRequired()])
    generation=StringField('Generation:',validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', pageTitle='Sun\'s Friends')

@app.route('/pokemonindex',methods=['GET','POST'])
def pokemonindex():
    form=Pokemonindex()
    if form.validate_on_submit():
        return"<h2> One of my favourite pokemons are {1}, national index number is {0}, it's from generation {2}".format(form.national_index.data,form.name.data,form.generation.data)
    return render_template('pokemonindex.html',form=form,pageTitle='favourite pokemons')


if __name__ == '__main__':
    app.run(debug=True)
