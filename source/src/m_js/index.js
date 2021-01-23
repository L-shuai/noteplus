//处理index.html的js

//登录成功后初始化页面
function initPage(){
    $.ajax({
            type: "GET",
            url: '/api/mgr/user?action=init_page',
            // data:'id='+id,
            dataType: "json",
            success: function (data) {
                if (data.ret==302 && data.msg=='未登录')
                {
                    alert('未登录')
                    url = data.redirect; //获取服务端返回的要重定向的页面
                    location.href=url
                }

                user = data.user
                document.getElementById('username').innerText=user.username
                document.getElementById('useremail').innerText=user.email
                document.getElementById('userid').value=user.id
                document.getElementById('user_last_login').innerText=user.last_login
                // alert(data.retlist);
                // console.log(data.retlist)

                // $.each(data.retlist, function (index, val) {
                //     //this必须加引号，否则报错
                //     $('#tbl').append("<tr><td>" + val.id + "</td><td>" + val.name + "</td><td>" + val.phonenumber + "</td><td>" + val.address + "</td><td>" + "<button onclick=edit_customer(" + val.id + ")>编辑</button>" + "<button onclick=delete_customer(" + val.id + ",this" + ")>删除</button>" + "</td></tr>")
                // });
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            }
        });
}


//    退出登录
    function signout(){
        $.ajax({
            type: "GET",  //这里退出不需要传参数。get和post都可以
            url: '/api/mgr/signout',
            // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
            dataType: "json",
            success: function (data) {
                if(data.ret == 0){
                    alert('退出成功get')
                }
                else{
                    alert('退出失败')
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            }
        });
    }