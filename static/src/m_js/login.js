function login() {
    // alert('登录')
    var _username = document.getElementById('username').value
    var _password = document.getElementById('password').value
    var jsonstr = {'username': _username, 'password': _password};
    var msg = ''
    if (_username == '' || _username == null) {
        msg = ' 用户名 '
    }
    if (_password == '' || _password == null) {
        msg += ' 密码 '
    }

    if (msg != '') {
        var content = {};
        content.message = msg + '不能为空';
        content.title = '登录失败';
        content.icon = 'fa fa-bell';

        // content.url = 'login.html';
        // content.target = '_blank';

        $.notify(content, {
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
        data: 'username=' + _username + '&password=' + _password,
        dataType: "json",
        success: function (data) {
            var content = {};
            if (data.ret == 0) {
                // alert('登录成功')

                //    注册成功


                var url = data.redirect
                location.href = url
            } else {
                // alert('登录失败')

                content.message = data.msg;
                content.title = '登录失败';
                content.icon = 'fa fa-bell';

                // content.url = 'login.html';
                // content.target = '_blank';

                $.notify(content, {
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


//发送邮箱验证码
function sendcode() {
    if (check(0)) {
        var _username = document.getElementById('username1').value;
        var _email = document.getElementById('email').value;
        if (checkEmail(_email)) {
            //邮箱格式正确
            //    发送验证码
            $("#sendcodebtn").text("正在发送");
            $("#sendcodebtn").attr("disabled", true);//禁用按钮
            var content = {};
            $.ajax({
                type: "GET",  //这里退出不需要传参数。get和post都可以
                url: '/api/mgr/user?action=sendEmail&username=' + _username + '&email=' + _email,
                // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
                dataType: "json",
                success: function (data) {
                    if (data.ret == 0) {
                        // alert('发送成功')

                        content.message = data.msg;
                content.title = '发送成功';
                content.icon = 'fa fa-bell';

                // content.url = 'login.html';
                // content.target = '_blank';

                $.notify(content, {
                    type: 'default',
                    placement: {
                        from: 'top',
                        align: 'right'
                    },
                    time: 300,
                    delay: 0,
                });

                        var btn = document.getElementById('sendcodebtn')
                        var count = 60
                        var timer = setInterval(function () {
                            count--;
                            $("#sendcodebtn").text(count + "秒");
                            if (count == 0) {
                                clearInterval(timer);
                                $("#sendcodebtn").attr("disabled", false);//启用按钮
                                $("#sendcodebtn").text("重新发送验证码");
                                // code = "";//清除验证码。如果不清除，过时间后，输入收到的验证码依然有效
                            }
                        }, 1000);


                        btn.innerText = count + '秒'
                    } else {
                         $("#sendcodebtn").attr("disabled", false);//启用按钮
                                $("#sendcodebtn").text("重新发送验证码");
                        // alert('发送')
                        content.message = data.msg;
                content.title = '发送失败';
                content.icon = 'fa fa-bell';

                // content.url = 'login.html';
                // content.target = '_blank';

                $.notify(content, {
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
    }
}

//检查表单是否全部填写完成
function check(step) {
    var _username = document.getElementById('username1').value;
    var _email = document.getElementById('email').value;
    var msg = ''
    var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/; //正则表达式
    var b = true
    if (step == 0)//获取验证码时  检查用户名和邮箱
    {
        if (_username == '' || _username == null) {
            msg = '  用户名  '
            b = false
        }
        if (_email == null || _email == '') {
            msg += '  邮箱  '
            b = false
        }


        if (msg != '') {
            var content = {};
            content.message = msg + '不能为空';
            content.title = '获取验证码失败';
            content.icon = 'fa fa-bell';

            // content.url = 'login.html';
            // content.target = '_blank';

            $.notify(content, {
                type: 'default',
                placement: {
                    from: 'top',
                    align: 'right'
                },
                time: 300,
                delay: 0,
            });

        }

        //
    } else {
        //注册时，检查全部字段
        var _password = document.getElementById('password1').value;
        var _confirmpassword = document.getElementById('password2').value;
        var code = document.getElementById('code').value;
        if (_username == '' || _username == null) {
            msg = '  用户名  '
            b = false
        }
        if (_email == null || _email == '') {
            msg += '  邮箱  '
            b = false
        }
        else{
            checkEmail(_email)
        }
        if (code == null || code == '') {
            msg += '  验证码  '
            b = false
        }
         if (_password == null || _password == '') {
            msg += '  密码  '
            b = false
        }

        // 检查是否勾选同意使用条款
        if (!$('#agree').is(':checked'))
        {
            var content2 = {};
            content2.message = '请勾选同意网站使用条款';
            content2.title = '注册失败';
            content2.icon = 'fa fa-bell';

            // content.url = 'login.html';
            // content.target = '_blank';

            $.notify(content2, {
                type: 'default',
                placement: {
                    from: 'top',
                    align: 'right'
                },
                time: 300,
                delay: 0,
            });
        }




        if (msg != '') {
            var content = {};
            content.message = msg + '不能为空';
            content.title = '注册失败';
            content.icon = 'fa fa-bell';

            // content.url = 'login.html';
            // content.target = '_blank';

            $.notify(content, {
                type: 'default',
                placement: {
                    from: 'top',
                    align: 'right'
                },
                time: 300,
                delay: 0,
            });

        }
    }
    return b
}

//校验邮箱
function checkEmail(email) {
    var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/; //正则表达式

    if (!reg.test(email)) { //正则验证不通过，格式不对
        var content = {};
        content.message = '邮箱格式错误';
        content.title = '获取验证码失败';
        content.icon = 'fa fa-bell';

        // content.url = 'login.html';
        // content.target = '_blank';

        $.notify(content, {
            type: 'default',
            placement: {
                from: 'top',
                align: 'right'
            },
            time: 300,
            delay: 0,
        });


        return false;
    } else {
        // alert("通过！");
        return true;
    }
}


//用户注册
function register() {
    if (!check(1))
    {
    //    表单未填写完整
        return;
    }
//    获取表单的数据
    var _username = document.getElementById('username1').value;
    var _email = document.getElementById('email').value;
    var _password = document.getElementById('password1').value;
    var _confirmpassword = document.getElementById('password2').value;
    var code = document.getElementById('code').value;

    //console.log('_password = '+_password)
    //console.log('_confirmpassword = '+_confirmpassword)
    if (_password != _confirmpassword) {
        alert('两次密码不匹配！')
        return;
    }
    else
    {
        if (_password.length<=8)
        {
            alert('密码长度过短，请设置8位以上的密码')
        }
    }
    // alert(_name)
    // return
    var jsonstr = {
        "action": 'register',
        'data': {'username': _username, 'email': _email, 'password': _password, 'code': code}
    };
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
            if (data.ret == 0) {
                content.message = '请点击登录';
                content.title = '注册成功';
                document.getElementById('show-signin').click()
                document.getElementById('username').value = _username
                document.getElementById('password').value = _password

            } else {
                content.message = data.msg;
                content.title = '注册失败';
            }


            content.icon = 'fa fa-bell';

            // content.url = 'login.html';
            // content.target = '_blank';

            $.notify(content, {
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
function keyLogin() {
    if (event.keyCode == 13)  //回车键的键值为13
    {

        document.getElementById("login-btn").click(); //调用登录按钮的登录事件
    }

}