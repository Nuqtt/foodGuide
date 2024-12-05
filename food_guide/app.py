from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import login_required
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 設定密鑰
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 未登入時重定向到的頁面


# 美食資料模型
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
# 使用者模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_login = db.Column(db.DateTime)  # 新增欄位來記錄最後一次登入時間

# 註冊表單
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# 登入表單
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# 首頁
@app.route('/')
def index():
    foods = Food.query.all()  # 從資料庫提取所有美食數據
    return render_template('index.html', foods=foods)

# 美食詳情頁
@app.route('/food/<int:food_id>')
def food_detail(food_id):
    food = Food.query.get_or_404(food_id)
    return render_template('food_detail.html', food=food)

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('成功註冊！即將跳轉到登入頁面...', 'success')  # 修改提示消息
        return redirect(url_for('login'))  # 導向登入頁面
    return render_template('register.html', form=form)


# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登出功能
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))

# 美食管理表單
class FoodForm(FlaskForm):
    name = StringField('Food Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')
    
# 管理頁面路由
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    foods = Food.query.all()  # 查詢所有美食數據
    form = FoodForm()
    if form.validate_on_submit():
        food = Food(name=form.name.data, description=form.description.data)
        db.session.add(food)
        db.session.commit()
        flash('Food added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', foods=foods, form=form)

# 刪除功能
@app.route('/food/delete/<int:food_id>', methods=['POST'])
@login_required
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Food deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 建立資料庫
    app.run(debug=True)
