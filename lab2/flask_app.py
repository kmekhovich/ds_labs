from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.random())

db = SQLAlchemy(app)

class ProgrammingLanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date)
    rank = db.Column(db.Integer, unique=True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    created_at = db.Column(db.Date)
    user_count = db.Column(db.BigInteger)
    programming_language_id = db.Column(db.Integer, db.ForeignKey('programming_languages.id'))
    programming_languages = db.relationship('ProgrammingLanguages')

@app.route('/language_add', methods=['GET', 'POST'])
def language_add():
    if request.method == 'POST':
        name = request.form['name']
        created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        rank = int(request.form['rank'])
        existing_rank = ProgrammingLanguages.query.filter_by(rank=rank).first()
        if existing_rank is not None:
            flash(f'Rank {rank} is already taken. Please choose another one.', 'error')
        else:
            new_language = ProgrammingLanguages(name=name, created_at=created_at, rank=rank)
            db.session.add(new_language)
            try:
                db.session.commit()
                return redirect(url_for('languages'))
            except Exception:
                db.session.rollback()
                flash('There was an error adding the programming language. Please try again.', 'error')
    return render_template('language_add.html')

@app.route('/language_edit/<int:language_id>', methods=['GET', 'POST'])
def language_edit(language_id):
    language = ProgrammingLanguages.query.get_or_404(language_id)
    if request.method == 'POST':
        language.name = request.form['name']
        language.created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        language.rank = int(request.form['rank'])

        # Проверка на уникальность rank прежде чем сохранять
        duplicate_rank = ProgrammingLanguages.query.filter(
            ProgrammingLanguages.id != language_id,
            ProgrammingLanguages.rank == language.rank
        ).first()

        if duplicate_rank:
            flash(f'Rank {language.rank} is already taken. Please choose another one.', 'error')
        else:
            try:
                db.session.commit()
                flash('Programming Language updated successfully!', 'success')
                return redirect(url_for('languages'))
            except Exception:
                db.session.rollback()
                flash('There was an error updating the programming language. Please try again.', 'error')

    return render_template('language_edit.html', language=language)

@app.route('/language_delete/<int:language_id>', methods=['GET'])
def language_delete(language_id):
    language = ProgrammingLanguages.query.get_or_404(language_id)
    products = Products.query.filter_by(programming_language_id=language.id).all()
    if products:
        # Невозможно удалить язык, так как существуют связанные с ним продукты
        flash(f'Cannot delete language {language.name} because there are products that use it.', 'error')
        return redirect(url_for('languages'))  # Перенаправляем на страницу с языками
    db.session.delete(language)
    db.session.commit()
    return redirect(url_for('languages'))

@app.route('/')
def languages():
    languages = ProgrammingLanguages.query.all()
    highlight = request.args.get('highlight')
    return render_template('languages.html', languages=languages, hightlight=highlight)

@app.route('/products')
def products():
    products = Products.query.all()
    languages = ProgrammingLanguages.query.all()
    return render_template('products.html', products=products, languages=languages)

@app.route('/product_add', methods=['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        user_count = int(request.form['user_count'])
        programming_language_id = int(request.form['programming_language_id'])

        # Проверьте, что programming_language_id выбран
        if programming_language_id:
            new_product = Products(
                name=name,
                company=company,
                created_at=created_at,
                user_count=user_count,
                programming_language_id=programming_language_id
            )
            db.session.add(new_product)
            try:
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('products'))
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
        else:
            flash('Programming language must be selected.', 'error')
    languages = ProgrammingLanguages.query.all()
    return render_template('product_add.html', languages=languages)

@app.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])
def product_edit(product_id):
    product = Products.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.company = request.form['company']
        product.created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        product.user_count = int(request.form['user_count'])
        product.programming_language_id = int(request.form['programming_language_id'])

        # Проверьте, что programming_language_id выбран
        if product.programming_language_id:
            try:
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('products'))
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
        else:
            flash('Programming language must be selected.', 'error')
    languages = ProgrammingLanguages.query.all()
    return render_template('product_edit.html', product=product, languages=languages)

@app.route('/product_delete/<int:product_id>', methods=['GET'])
def product_delete(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))

# Создаем таблицы
db.create_all()

# запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)
