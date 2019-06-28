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

?笔记：用户中心跟新经资讯不同，新经资讯你不登录你都进入不了用户中心。而这个项目不同，最上排号右边有个"个人中心"按钮。

    ### 登录后欢迎信息：
    if data.user:
        欢迎你：data.user.username:退出：链接：<a her = "url(user/logout)">退出</a>
    else:
        <a her = "url(user/login)"><a her = "user/register"
        <a href = "{% url'user:login'%}">

        ? 对比：在新经资讯项目中,后端是通过ajax实现的。

### 今天把后端的逻辑写一遍
    点登录按钮，显示登录的页面
        用get
    再点登录的提交，显示首页
    用Post
先做出登录用的页面出来

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html',)

    def post(self, request):
        # 先做最简单的提交
         # 拿到数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')


        # 核对数据
        user = authenticate(username=username, password=password)
        # 要判断user是否是激活的，如果是，那么
        # 要往session中写东西：
        if user:
            if user.is_active == True:
                login(request, user)

        # 如果不是激活，就不管
        # 判断remember是否是On,如果是，那么要返回cookies,
               if remember is on:
                    response = response.set_cookie('username', username)
                    # ？问题：如何把cookie和模板一起传过去呢？
                    # ？纠错：没有考虑到如果密码和用户不正确，那么返回"密码不正确，也没有考虑如果没有激活，返回"没有激活",也没有考虑如果remember不存在：那么：也没有考虑如果地址中有？=的情况。
                    # ?笔记：render,redirect,都是一个response对象，可以直接return,也可以赋值给一个变量后再return,比如：
                else:
                    response.delete_cookie('username')
                # 返回到首页，或者自定义的首页：
                return redirect(reverse(goods:index))
                # 拿到参数，返回到参数的页面：比如/user/
                next = request.GET.get("next")
                return redirect(url"next")

            else:
                return render(request, 'login.html', {'errmsg':"没有激活"})

        else:
            # 用户密码都不正确：
            # 输出，返回登录模板加一个errmsg:
            return render(request, 'login.html', {'errmsg':"密码输入错误"})
        # 返回数据
        return render(request, 'index.html',)


### 现在写用户地址那一块：
先做前端：
<div class="right_content clearfix">
				<h3 class="common_title2">收货地址</h3>
				<div class="site_con">
					<dl>
						<dt>当前地址：</dt>
						<dd>北京市 海淀区 东北旺西路8号中关村软件园 （李思 收） 182****7528</dd>
					</dl>
				</div>
				<h3 class="common_title2">编辑地址</h3>
				<div class="site_con">
					<form>
						<div class="form_group">
							<label>收件人：</label>
							<input type="text" name="receiver">
						</div>
						<div class="form_group form_group2">
							<label>详细地址：</label>
							<textarea class="site_area" name='address'></textarea>
						</div>
						<div class="form_group">
							<label>邮编：</label>
							<input type="text" name="no">
						</div>
						<div class="form_group">
							<label>手机：</label>
							<input type="text" name="phone_no">
						</div>

						<input type="submit" name="" value="提交" class="info_submit">
					</form>
				</div>
		</div>
	</div>

# ?问题：为什么个人中心模块要从地址写起而不从个人信息写起呢？
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html',)

    def post(self, request):
        # 先做最简单的提交
        # 拿到数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')


        # 核对数据
        user = authenticate(username=username, password=password)
        # 要判断user是否是激活的，如果是，那么
        # 要往session中写东西：
        if user:
            if user.is_active == True:
                login(request, user)

                # 如果不是激活，就不管
                # 判断remember是否是On,如果是，那么要返回cookies,
            if remember is on:
                response = response.set_cookie('username', username)
                # ？问题：如何把cookie和模板一起传过去呢？
                # ？纠错：没有考虑到如果密码和用户不正确，那么返回"密码不正确，也没有考虑如果没有激活，返回"没有激活",也没有考虑如果remember不存在：那么：也没有考虑如果地址中有？=的情况。
                # ?笔记：render,redirect,都是一个response对象，可以直接return,也可以赋值给一个变量后再return,比如：
            else:
                response.delete_cookie('username')
                # 返回到首页，或者自定义的首页：
            return redirect(reverse(goods:index))
            # 拿到参数，返回到参数的页面：比如/user/
            next = request.GET.get("next")
            return redirect(url"next")

            else:
            return render(request, 'login.html', {'errmsg':"没有激活"})

    else:
    # 用户密码都不正确：
    # 输出，返回登录模板加一个errmsg:
    return render(request, 'login.html', {'errmsg':"密码输入错误"})
# 返回数据
return render(request, 'index.html',)




class AddressView():
    def get(self,request):
        context = {

        }
        return render(request, 'user_center_site.html', context)
    def post(self,request):
        # 要在数据库中增加地址
        # 得到数据
        receiver = request.POST.get('receiver')
        address = request.POST.get('address')
        no = request.POST.get('no')
        phone_no = request.POST.get('phone_no')

        # 有效性
        if not all[receiver, address, no, phone_no]

        # 写入数据库
        address = Address()
        address.
        # 返回页面：
        return redirect('user/address')

# 最前面显示默认地址，后面不过是往数据库里加地址，
就像创建用户对象一样，django里面也有一个封闭的函数可供调用。
就是要判断创建的用户user.is_defalt是设置成True还是什么了。如果数据库里有地址是defalt,那么设成false,如果没有，那么设
class Logout_infoView(View):
    def get(self, request):

        #退出到登录页面前要进行处理：
        # 删除session数据
        logout(request, user)
        #返回登录页面：
        return render(request, 'login.html')




###