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

if __name__ == '__main__':
    app.run(debug=True)