from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn="mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db=SQLAlchemy(app)

class ysun95_pokemonindex(db.Model):
    InstanceID = db.Column(db.Integer,primary_key=True)
    national_index=db.Column(db.String(255))
    pokemon_name=db.Column(db.String(255))
    generation=db.Column(db.String(255))

    def __repr__(self):
        return "InstanceID: {0} | national_index: {1} | pokemon_name: {2} | generation: {3}".format(self.InstanceID,self.national_index,self.pokemon_name,self.generation)


class Pokemonindex(FlaskForm):
    national_index=StringField('National index number:',validators=[DataRequired()])
    pokemon_name=StringField('name:',validators=[DataRequired()])
    generation=StringField('Generation:',validators=[DataRequired()])

@app.route('/')
def index():
    all_pokemons=ysun95_pokemonindex.query.all()
    return render_template('index.html',pokemontable=all_pokemons ,pageTitle='Sun\'s favourite pokemons')

@app.route('/pokemonindex',methods=['GET','POST'])
def pokemonindex():
    form=Pokemonindex()
    if form.validate_on_submit():
        pokemon=ysun95_pokemonindex(national_index=form.national_index.data,pokemon_name=form.pokemon_name.data,generation=form.generation.data)
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')
    return render_template('pokemonindex.html',form=form,pageTitle='Add pokemons')


if __name__ == '__main__':
    app.run(debug=True)
