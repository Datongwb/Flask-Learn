from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL监听的端口号，默认3306
PORT = '3306'
# 连接MySQL用户名，读者用自己设置的
USERNAME = 'root'
# 连接MySQL密码，读者用自己设置的
PASSWORD = '19491001'
# MySQL上创建的数据库名称
DATABASE = 'learn_database'

app.config['SQLALCHEMY_DATABASE_URI'] =f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

# 在app.config中设置好连接数据的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取zpp.config中连接数据库的信息

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# ORM模型映射成表三部
# 1. flask db init： 这步只需要执行一次
# 2. flask db migrate： 识别ORM模型的变化，生成迁移脚本
# 3. flask db upgrade： 运行迁移脚本，同步到数据库中


# 测试连接数据库是否成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())


# ORM模型和表的映射
class User(db.Model):
    # 定义数据库中对应的表名
    __tablename__='user'
    # id字段：整数类型，主键，自增
    # db.Column 用于定义表的列，第一个参数是数据类型，后续是列的属性
    # db.Integer 用于定义整数类型
    # autoincrement=True 指定该字段自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar, null=0
    # 定义username字段：字符串类型，非空，最大长度100
    # db.String 用于定义字符串类型
    # nullable=False 指定该字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

# user = User(username="运行ORM模型", password="123456")
# sql: insert user(username, password) volues("运行ORM模型", "123456")

# ORM模型外键与表的关系
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # backref：会自动的给User模型添加一个articles的属性，用来获取文章列表
    author = db.relationship("User", backref="articles")

  
# with app.app_context():
#     db.create_all()

@ app.route('/')
def hellp_world():
    return "hello world"


# 添加信息到数据中
@ app.route('/user/add')
def add_user():
    # 1. 创建ORM对象
    user1 = User(username="无敌的钢铁雄心", password="213")
    user2 = User(username="超级无敌的钢铁雄心", password="321")
    user3 = User(username="钢铁雄心", password="3312")
    # 2. 将ORM对象添加到db.sesssion中
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    # 3. 将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户添加成功"


# 查询数据
@ app.route('/user/query')
def query_user():
    # 1. get查找：根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}: {user.username}-{user.password}")
    # 2. filter_by查找：根据条件查找
    # Query：类数组
    users = User.query.filter_by(username="无敌的钢铁雄心")
    for user in users:
        print(f"{user.id}: {user.username}-{user.password}")
    return "查找成功"



# Read操作也是查询操作，只不过是只读的，不会修改数据库中的数据
@ app.route('/user/read')
def read_user():
    users = User.query.all()
    for user in users:
        print(f"{user.id}: {user.username}-{user.password}")
    return "查询成功"


# 查找到数据后，修改数据
@ app.route('/user/update')
def update_user():
    user = User.query.filter_by(username="超级无敌的钢铁雄心").first()
    user.password = '5749283'
    db.session.commit()
    return "数据修改成功"


# 删除数据
@ app.route('/user/delete')
def delete_user():
    # 1. 查找数据
    user = User.query.get(3)
    # 2. 删除数据
    db.session.delete(user)
    # 3. 将db.session中的修改，同步到数据库中
    db.session.commit()
    return "数据删除成功"


# 外键与表的关系
@ app.route('/article/add')
def add_article():
    article1 = Article(title="Flask学习大纲", content="Flaskxxxxxxx")
    article1.author = User.query.get(2)

    article2 = Article(title="Django学习大纲", content="Djangoyyyyyyy")
    article2.author = User.query.get(2)

    # 添加到session中
    db.session.add_all([article1, article2])
    # 同步session中的数据到数据库中
    db.session.commit()
    return "文章添加成功"

# 查询文章列表
@ app.route('/article/query')
def query_article():
    user = User.query.get(2)
    for article in user.articles:
        print(article.title)
    return "文章查找成功"

if __name__ == '__main__':
    app.run(debug=True)