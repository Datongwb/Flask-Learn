from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Integer, String
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# 定义命名为约定的Base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        # ix: index. 索引
        "ix": 'ix_%(column_0_label)s',
        # un: unique. 唯一约束
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # ck: Check. 检查约束
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # fk: Foreign Key. 外键约束
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # pk: Primary Key. 主键约束
        "pk": "pk_%(table_name)s"
    })
db = SQLAlchemy(app=app, model_class=Base)
migrate = Migrate(app, db)

class User(db.Model):
    # 定义数据库表名为 'user'
    __tablename__ = 'user'
    # 定义用户ID为主键，自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 定义用户名字段，最大长度为50，不允许为空
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    # 定义密码字段，最大长度为200，不允许为空
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/create')
def create():
    user1 = User(username="张三", password="123456")
    user2 = User(username="李四", password="654321")
    user3 = User(username="王五", password="543254")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    return "数据添加成功"

@app.route('/read')
def read():
    # 1.获取User中所有的数据
    # user = User.query.all()
    # print(user)
    # 2.获取主键位1的User对象
    # user1 = User.query.get(1)
    # user = db.session.scalars(db.select(User).where(User.id == 1)).first()
    # user2 = User.query.filter_by(username = "张三").first()
    # print(user1)
    # print(user)
    # print(user2)
    # 3.根据username排序,默认情况下是从小到大排序（升序），如果想从大到小排序（倒序），可以传入desc()函数
    users = User.query.order_by(User.username).all()
    users1 = User.query.order_by(User.username.desc()).all()
    print(users)
    print(users1)
    return "数据提取成功"

@app.route('/update')
def update():
    # 1.查找出来再修改
    # user = db.session.scalars(db.select(User).where(User.username == "张三")).first()
    # user.username = "zhangsan"
    # 同步到数据库中
    # db.session.commit()

    # 2.直接修改
    user = User.query.filter_by(username="王五").first()
    user.username = 'wangwu'
    db.session.commit()
    return "数据修改成功"

@app.route('/delete')
def delete():
    # 1.查找出来再删除
    # user = db.session.scalars(db.select(User).where(User.username == "zhangsan")).first()
    # db.session.delete(user)
    # db.session.commit()
    # 2.直接删除
    user = User.query.filter_by(username="wangwu").first()
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功"

if __name__ == '__main__':
    app.run(debug=True)