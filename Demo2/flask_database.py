# 导入所需的库和模块
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import config
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, Date
from flask_migrate import Migrate
from typing import List
from datetime import date

# 创建 Flask 应用实例
app = Flask(__name__)
# 从 config 模块加载配置
app.config.from_object(config)

# 定义命名约定的 Base 类，用于 SQLAlchemy 模型
class Base(DeclarativeBase):
    # 设置数据库命名约定，用于自动生成约束名称
    metadata = MetaData(naming_convention={
        # ix: index. 索引命名约定
        "ix": 'ix_%(column_0_label)s',
        # uq: unique. 唯一约束命名约定
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # ck: Check. 检查约束命名约定
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # fk: Foreign Key. 外键约束命名约定
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # pk: Primary Key. 主键约束命名约定
        "pk": "pk_%(table_name)s"
    })

# 初始化 SQLAlchemy 扩展，使用自定义的 Base 类
db = SQLAlchemy(app=app, model_class=Base)
# 初始化 Flask-Migrate 扩展，用于数据库迁移
migrate = Migrate(app, db)

# 定义 User 用户模型
class User(db.Model):
    # 定义数据库表名为 'user'
    __tablename__ = 'user'
    # 定义用户ID为主键，自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 定义用户名字段，最大长度为50，不允许为空
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    # 定义密码字段，最大长度为200，不允许为空
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    # 定义邮箱字段，最大长度为200，允许为空
    email: Mapped[str] = mapped_column(String(200), nullable=True)

    # 定义外键 department_id，关联到 department 表的 id 字段，允许为空
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'), nullable=True)
    # 定义与 Department 模型的关系，建立双向关联
    department: Mapped["Department"] = relationship("Department", back_populates="users")

    # 定义与 UserExtension 模型的一对一关系
    user_extension: Mapped["UserExtension"] = relationship("UserExtension", back_populates="user", uselist=False)

# 定义 UserExtension 用户扩展信息模型（与 User 一对一关系）
class UserExtension(db.Model):
    # 定义数据库表名为 'user_extension'
    __tablename__ = "user_extension"
    # 定义主键 ID，自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 定义生日字段，类型为日期，不允许为空
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    # 定义大学字段，最大长度100，不允许为空
    university: Mapped[str] = mapped_column(String(100), nullable=False)

    # 定义外键 user_id，关联到 user 表的 id 字段，且必须唯一（实现一对一关系的关键）
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    # 定义与 User 模型的关系，建立双向关联
    user: Mapped["User"] = relationship("User", back_populates="user_extension")

# 定义部门与权限的多对多关联表
department_permission_table = Table(
    "department_permission",  # 表名
    db.metadata,  # 使用 db 的元数据
    Column("department_id", Integer, ForeignKey('department.id'), primary_key=True),  # 部门ID外键，作为联合主键的一部分
    Column("permission_id", Integer, ForeignKey('permission.id'), primary_key=True)   # 权限ID外键，作为联合主键的一部分
)

# 定义 Department 部门模型
class Department(db.Model):
    # 定义数据库表名为 'department'
    __tablename__ = "department"
    # 定义主键 ID，自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 定义部门名称字段，最大长度50，不允许为空
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # 定义与 User 模型的一对多关系（一个部门可以有多个用户）
    users: Mapped[List[User]] = relationship("User", back_populates="department")

    # 定义与 Permission 模型的多对多关系，通过 department_permission_table 关联表实现
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission",
        secondary=department_permission_table,  # 指定关联表
        back_populates="departments"  # 建立反向关系
    )

# 定义 Permission 权限模型
class Permission(db.Model):
    # 定义数据库表名为 'permission'
    __tablename__ = "permission"
    # 定义主键 ID，自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # 定义权限名称字段，最大长度50，不允许为空
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # 定义与 Department 模型的多对多关系，通过 department_permission_table 关联表实现
    departments: Mapped[List[Department]] = relationship(
        "Department",
        secondary=department_permission_table,  # 指定关联表
        back_populates="permissions"  # 建立反向关系
    )

# 定义根路由，返回简单的问候语
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 一对多数据库操作示例路由
@app.route('/one2many')
def one2many():
    # 1.通过user添加department
    # department = Department(name="技术部")
    # user1 = User(username="zhangsan", password="123456", email="zhangsan@123.com", department=department)
    # user2 = User(username="lisi", password="654321", email="lisi@123.com", department=department)
    # user3 = User(username="wangwu", password="abc123", email="wangwu@123.com", department=department)
    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.add(user3)
    # db.session.commit()

    # 2.通过department添加user
    # department = db.session.scalar(db.select(Department).where(Department.id ==1))
    # user = User(username='liuzhen', password='123456', email='liuzhen@123.com', department=department)
    # department.users.append(user)
    # db.session.commit()

    # 3.通过user访问department
    # user = db.session.scalar(db.select(User).where(User.id==1))
    # department = user.department
    # print(f"部门名称：{department.name}")
    
    # 4.通过department获取所有当前部门下的用户
    department = db.session.scalar(db.select(Department).where(Department.id==1))
    users = department.users
    for user in users:
        print(user.id, user.username, user.password,user.email)

    return "一对多数据操作成功"

# 多对多数据库操作示例路由
@app.route('/many2many')
def many2many():
    # 1.通过department添加permission
    # department = db.session.scalar(db.select(Department).where(Department.id==1))
    # permissions = [
    #     Permission(name="访问首页"),
    #     Permission(name="访问用户管理"),
    #     Permission(name="访问部门管理")
    # ]
    # # 可以将department.permissions当做一个列表
    # department.permissions.extend(permissions)
    # db.session.commit()
    
    # 2.移除多对多关系的数据
    department = db.session.scalar(db.select(Department).where(Department.id==1))
    permission = db.session.scalar(db.select(Permission).where(Permission.id==1))
    department.permissions.remove(permission)
    db.session.commit()

    return "多对多数据操作成功"

# 一对一数据库操作示例路由
@app.route('/one2one')
def one2one():
    # 查询 ID 为 1 的用户
    user: User = db.session.scalar(db.select(User).where(User.id==1))
    # 为该用户创建扩展信息
    user.user_extension = UserExtension(birthday=date(2005,5,5), university="太原工业学院")
    # 提交更改到数据库
    db.session.commit()
    return "一对一数据操作成功"

# 应用程序入口点
if __name__ == '__main__':
    # 以调试模式运行应用
    app.run(debug=True)