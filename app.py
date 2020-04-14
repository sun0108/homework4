from flask import Flask
from flask import render_template, redirect,request,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
import os
from sqlalchemy import or_

dbuser=os.environ.get('DBUSER')
dbpass=os.environ.get('DBPASS')
dbhost=os.environ.get('DBHOST')
dbname=os.environ.get('DBNAME')

#conn="mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)
conn="mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser,dbpass,dbhost,dbname)

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
    InstanceID=IntegerField('InstanceID :')
    national_index=StringField('National index number:',validators=[DataRequired()])
    pokemon_name=StringField('name:',validators=[DataRequired()])
    generation=StringField('Generation:',validators=[DataRequired()])

@app.route('/')
def index():
    all_pokemons=ysun95_pokemonindex.query.all()
    return render_template('index.html',pokemontable=all_pokemons,pageTitle='Sun\'s favourite pokemons')



@app.route('/search',methods=['GET','POST'])
def search():
        if request.method=="POST":
            form=request.form
            search_value=form['search_string']
            search="%{}%".format(search_value)
            results=ysun95_pokemonindex.query.filter(or_(ysun95_pokemonindex.pokemon_name.like(search),
                                                          ysun95_pokemonindex.national_index.like(search),
                                                          ysun95_pokemonindex.generation.like(search))).all()
            return render_template('index.html',pokemontable=results,pageTitle="Sun's Pokemon index",legend="Search results")
        else:
            return redirect('/')

@app.route('/pokemonindex',methods=['GET','POST'])
def pokemonindex():
    form=Pokemonindex()
    if form.validate_on_submit():
        pokemon=ysun95_pokemonindex(national_index=form.national_index.data,pokemon_name=form.pokemon_name.data,generation=form.generation.data)
        db.session.add(pokemon)
        db.session.commit()
        return redirect('/')
    return render_template('pokemonindex.html',form=form,pageTitle='Add pokemons')



@app.route('/delete_pokemon/<int:InstanceID>',methods=['GET','POST'])
def delete_pokemon(InstanceID):
    if request.method=='POST':    
        pokemon=ysun95_pokemonindex.query.get_or_404(InstanceID)
        db.session.delete(pokemon)
        db.session.commit()
        return redirect('/')
    else: 
        return redirect('/')


@app.route('/pokemons/<int:InstanceID>',methods=['GET','POST'])
def get_pokemon(InstanceID):
    pokemons=ysun95_pokemonindex.query.get_or_404(InstanceID)
    return render_template('pokemons.html',form=pokemons,pageTitle="Pokemons details", legend='Pokemon Details')

@app.route('/pokemons/<int:InstanceID>/update',methods=['GET','POST'])
def update_pokemon(InstanceID):
    pokemons=ysun95_pokemonindex.query.get_or_404(InstanceID)
    form=Pokemonindex()
    
    if form.validate_on_submit():
        pokemons.national_index=form.national_index.data
        pokemons.pokemon_name=form.pokemon_name.data
        pokemons.generation=form.generation.data
        db.session.commit()
        return redirect(url_for('get_pokemon',InstanceID=pokemons.InstanceID))
    form.InstanceID.data=pokemons.InstanceID
    form.pokemon_name.data=pokemons.pokemon_name
    form.national_index.data=pokemons.national_index
    form.generation.data=pokemons.generation
    return render_template('update_pokemon.html',form=form,pageTitle='Update pokemon',legend='Updata a pokemon')




if __name__ == '__main__':
    app.run(debug=True)
