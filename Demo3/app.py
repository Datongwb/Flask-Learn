from flask import Flask, render_template # 渲染模板
from datetime import datetime

app = Flask(__name__)


# 自定义过滤器
def datetime_format(value, format="%Y年%m月%d日 %H:%M"):
    return value.strftime(format)
app.add_template_filter(datetime_format, "dformat")

class User:  # 定义一个博客类
    def __init__(self, username, email):
        self.username = username
        self.email = email


# 模板访问对象属性 # index.html
@app.route('/')
def hello_world():
    user = User(username="钢铁雄心", email="123456@qq.com")
    persion = {
        "username": "users",
        "email": "123456@qq.com"
    }
    return render_template("index.html  ", user=user, persion=persion)


# 带参数的url # blog_detail.html
@ app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template("blog_detail.html", blog_id=blog_id, username="钢铁雄心")


# 过滤器的使用 # filter_demo.html
@ app.route('/filter')
def filter_demo():
    user = User(username="钢铁雄心", email="123456@qq.com")
    mytime = datetime.now()
    return render_template("filter_demo.html", user=user, mytime=mytime)


# 控制语句 # control.html
@ app.route('/control')
def control_statement():
    age = 10
    books = [
        { "name": "西游记", "author": "吴承恩" },
        { "name": "三国演义", "author": "罗贯中"}
    ]
    return render_template("control.html", age=age, books=books)


# 模板继承 # bse.html, child1.html, child2.html
@ app.route('/child1')
def child1():
    return render_template("child1.html")
@ app.route('/child2')
def child2():
    return render_template("child2.html")


# 加载静态文件 # static.html, style.css, my.js, lizijia.png
@ app.route('/static')
def static_demo():
    return render_template("static.html")

if __name__ == '__main__':
    app.run(debug=True)