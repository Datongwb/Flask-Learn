from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# url与视图：path与视图

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/profile')
def profile():
    return "我是个人中心"

# 带参数的url:将参数固定到了path中
@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    return "您访问的博客升是： %s" % blog_id

# 查询字符串的方式传参
# /book/list: 会返回第一页的数据
# /book/list?page=2: 获取第二页的数据
@app.route('/book/list')
def book_list():
    # args=arguments: 参数
    # request.args: 类字典类型
    page = request.args.get('page', default=1, type=int)
    return f"您获取的是第{page}的图书列表！"

@app.get('/login')
def login():
    return "登录页面"


@app.get('/pub')
def pub():
    # 现在把功能简化，传了name参数就是登录，没有传就是没有登录
    name = request.args.get('name')
    if not name:
        return redirect('/login')
    else:
        return "发布页面"
    
@app.route('/list')
def article_lsit():
    return render_template('lsit.html')

@app.route('/detail')
def article_detail():
    return render_template('detail.html')

@app.route('/template/static')
def static_template():
    return render_template('static.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)