"""
### 先做注册这个模块：
from django.http import request

登录注册后跳转到首页：

首页：先不做，先返回一个静态的首页，先做登录
登录用html做，通过表单的形式，然后后端用POST接收，再往数据库增加一个用户信息，再return redict到首页。
一点一登录，弹出登录框，是前端ajax实现的。
看了发现不是通过ajax，页是通过网页。
这个网页的的url,可以是user/register,一个是get,一个是POST，
##### 开始写前端：
就像小猪猫项目的个人中心-个人基本信息修改，不同是这里不用显示用户信息，if 而且表单各项已经加了name:
    ?问题：如何返回一个静态页面，以及重定向有什么不同？
    写return redirect for user/register,不行啊，你这个域名的返回还没做好呢？
    ?纠错 ？问题：为什么要加下面这段呢？
    <form method="post" action="/user/register">
{% csrf_token %}


##### 写后端：
def register():
    if request.method == "GET":
        return template(register.html)
    if request.method == "POST":
        接收
        user_name = request.POST.get("user_name")
        pwd = request.POST.get("pwd")
        email = request.POST.get("email")
        有效
        数据库
        user = User()
        user.password = pwd
        user.email = email
        user.is_active = False
        ...
        返回什么
        # 发送邮件函数：
        return (user,index.html)
?纠错：上面写错了，上面要传给模板的方法，是首页后端逻辑的事。你这里只需要
# return redirect('/index')
##### 还要加入激活账号的功能
1发邮件
2用户点邮件链接，后端把
def activeView(request, b):
    user/active/9

        a = decode(b)  b是密码
    user = User.objects.get(User.id = a)
    user.is_active = True

##### 现在想着如何用类来实现：
class registerView():
    def get(self):

        # 显示注册页面
        return render(request, 'register.html')

    def post(self)):

        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
        # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答, 跳转到首页
        return redirect(reverse('goods:index'))

"""

###现在开始听课，以及，调试程序，把celery功能去掉。
from django.http import HttpResponse
from django.shortcuts import render, redirect
？问题：redis在新经资讯项目中主要用来做什么
暂时的存储数据，为什么要用redis?
比如你登录了一个用户，你直接访问那个网站的主页的时候，你不用再去登录了。直接给你一个登录的显示页面。比如登录首页。你输入首页的网址，为什么会自动给你显示右上角的用户信息呢？后端一定是拿到了用户的id。从数据库中读出分类信息，那它是怎么知道是哪个用户Id呢？
其实用户不光输入了网址，还带上了cookie文件。
cookie文件里放的是什么，是怎么来的？

这就要回到你登录网站的时候了。你登录的时候，Post用户名和密码，后端发现对了。给你跳转到首页，还给你返回了一个cookie,这个cookie里有你的用户信息。而且有时效性。过了一段时间它会消失。当你下次再登录的时候，虽然你没有输入用户信息，但浏览器已经悄悄给你带上了包含用户的cookie,拿着这个信息，后台就知道是哪个用户了。

？思想：大量用户都要访问首页，而且首页的信息都是一样的，为了加快速度，我们可以设置缓存。提高速度。

###现在实现登录：
#####点登录，返回一个前端登录页，以及cookie中存放的用户信息，这样才能在输入框中显示用户的信息。类似于新经资讯项目个人中心里修改用户信息。
前端：
后端一个函数，/user/login
返回模板，还有用户的信息
前端：见static/login.html

#####后端：
/user/login
class loginView():
    def get(self, request):
        user = ？问题：从session中取出，如何取呢？sessionid:拿到用户信息，通过cookie拿到sessionid,以前在flask中，直接user = g.user就拿到，flask中是怎样封闭的呢？
        username = user.user.username
        return render(request, username:username)

    def post(self, request):
        拿到数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        有效性
        user = User.objects.get(username = username)
        if not user
            ?问题：如何输出错误信息？
            errmsg = "数据查询错误"
        设置cookies:
        response = HttpResponse()
        response.content =  ？纠错：这里返回redirect不用加content
        ？纠错：如果点记住用户，是用来判断是否设置cookie,而验证用户名密码正确后，且是激活状态后，就要把这个user加入到session会话中。django不过是把这一步封装在了login函数中。
        response.set_cookie('username', username)

        数据库

        用户信息有效性检验
        ?问题：如何设置cookie，session,并且返回给浏览器？
        response = cookies.set()
        return response
        返回到首页
        return redirect(url"goods:index")

###提取模板：
        ？问题：搜索框，购物车与首页的搜索框有什么不同吗？其实可以直接查看网页源代码，把代码复制过来。

######先做user/user_info

        user/user_info

class user_infoView(View):
    def get(self, request):

    def post(self, request):

？问题：浏览过的商品，如果展示，它是一个集合
