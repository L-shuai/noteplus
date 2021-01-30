function login(){
        // alert('登录')
        var _username = document.getElementById('username').value
        var _password = document.getElementById('password').value
        var jsonstr = {'username':_username,'password':_password};
        var msg=''
        if (_username=='' || _username==null)
        {
            msg = '请输入用户名    '
        }
        if (_password=='' || _password==null)
        {
            msg += '请输入密码'
        }

        if (msg!='')
        {
             var content = {};
            content.message = msg;
			        content.title = '登录失败';
				content.icon = 'fa fa-bell';

			// content.url = 'login.html';
			// content.target = '_blank';

			$.notify(content,{
				type: 'default',
				placement: {
					from: 'top',
					align: 'right'
				},
				time: 300,
				delay: 0,
			});
			return
        }

        $.ajax({
            type: "POST",
            url: '/api/mgr/signin',
            // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送

            //登录使用的是django内置的方法  http 请求消息 body 中 参数以 格式 x-www-form-urlencoded 存储    必须是'username='+_username+'&password='+_password,这种
            data: 'username='+_username+'&password='+_password,
            dataType: "json",
            success: function (data) {
                  var content = {};
                if (data.ret == 0)
                {
                    // alert('登录成功')

            //    注册成功


                    var url = data.redirect
                    location.href=url
                }
                else
                {
                    // alert('登录失败')

                     content.message = data.msg;
			        content.title = '登录失败';
				content.icon = 'fa fa-bell';

			// content.url = 'login.html';
			// content.target = '_blank';

			$.notify(content,{
				type: 'default',
				placement: {
					from: 'top',
					align: 'right'
				},
				time: 300,
				delay: 0,
			});


                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            }
        });
    }



    //用户注册
    function register(){
//    获取表单的数据
        var _username = document.getElementById('username1').value;
        var _email = document.getElementById('email').value;
        var _password = document.getElementById('password1').value;
        var _confirmpassword = document.getElementById('password2').value;
        //console.log('_password = '+_password)
        //console.log('_confirmpassword = '+_confirmpassword)
        if (_password != _confirmpassword)
        {
            alert('两次密码不匹配！')
            return;
        }
        // alert(_name)
        // return
        var jsonstr = {"action": 'register', 'data': {'username': _username, 'email': _email, 'password': _password}};
        $.ajax({
            type: "POST",
            url: '/api/mgr/user',
            data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
            dataType: "json",
            success: function (data) {
                // alert('注册  id=' + data.id)
                // alert(data.id)
                var content = {};
            //    注册成功
                if (data.ret==0)
                {
                    content.message = '请点击登录';
			        content.title = '注册成功';
			        document.getElementById('show-signin').click()
                    document.getElementById('username').value=_username
                    document.getElementById('password').value=_password

                }
                else
                {
                     content.message = data.msg;
			        content.title = '注册失败';
                }



				content.icon = 'fa fa-bell';

			// content.url = 'login.html';
			// content.target = '_blank';

			$.notify(content,{
				type: 'default',
				placement: {
					from: 'top',
					align: 'right'
				},
				time: 300,
				delay: 0,
			});

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            }
        });
    }


//监听按键  回车键登录
function keyLogin(){
 if (event.keyCode==13)  //回车键的键值为13
 {

     document.getElementById("login-btn").click(); //调用登录按钮的登录事件
 }

}