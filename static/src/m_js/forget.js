//处理profile.html的js
$(document).ready(function(){
        // initPage()
})

//登录成功后初始化页面
function initPage() {
    $.ajax({
        type: "GET",
        url: '/api/mgr/user?action=init_page',
        // data:'id='+id,
        dataType: "json",
        success: function (data) {
            if (data.ret == 302 && data.msg == '未登录') {
                // alert('未登录')
                url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
                alert('请登录')
            }

            user = data.user
            // document.getElementById('username').innerText = user.username
            // document.getElementById('useremail').innerText = user.email
            // document.getElementById('userid').value = user.id
            // document.getElementById('user_last_login').innerText = user.last_login
            $('.username').text(user.username)
            $('.useremail').text(user.email)
            $('.userid').text(user.id)
             $('.username').val(user.username)
            $('.useremail').val(user.email)
            $('.last_login').val(user.last_login)
            $('.date_joined').val(user.date_joined)
            // alert(data.retlist);
            // //console.log(data.retlist)

            //填充回收站列表
            // $('#deletelist').html('<h1>test</h1>')
            // $('#deletelist').append("<li id='new'> new Li </li>");
            var notelist = data.notelist;
            fillout(notelist)
            //填充左侧分类列表

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

//修改密码
function modify_password(){
    var code = $("#code").val()
    var psw = $("#psw").val()
    var msg = ''
    if (code == '' || code == null) {
            msg = '  验证码  '
            // b = false
        }
        if (psw == null || psw == '') {
            msg += '  新密码  '
            // b = false
        }
        else
        {
            if (psw.length<=8)
        {
            alert('密码长度过短，请设置8位以上的密码')
            return;
        }
        }

        if (msg != '') {
            var content = {};
            content.message = msg + '不能为空';
            content.title = '密码修改失败';
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
        return;
        }
        else
        {
        //    密码都不为空
     var jsonstr = {
        "action": 'modify_password',
        'data': { 'code': code, 'psw': psw}
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
                content.message = '请使用新密码登录';
                content.title = '密码修改成功';


            } else {
                content.message = data.msg;
                content.title = '密码修改失败';
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
            // alert(XMLHttpRequest.readyState);
            // alert(textStatus);
        }
    });
        }
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


//发送邮箱验证码
function sendcode() {

    var code = $("#code").val()
    var psw = $("#psw").val()
    var email = $("#email").val()
    var msg = ''
    if (email == '' || email == null) {
            msg = '  邮箱  '
            // b = false
        var content = {};
            content.message = msg + '不能为空';
            content.title = '密码修改失败';
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
    else{
        if (checkEmail(email))
        {
            //邮箱格式正确  发送邮件
            //    发送验证码
            $("#sendcodebtn").text("正在发送");
            $("#sendcodebtn").attr("disabled", true);//禁用按钮
            var content = {};
            $.ajax({
                type: "GET",  //这里退出不需要传参数。get和post都可以
                url: '/api/mgr/user?action=sendCode&email='+email,
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

        // var _username = document.getElementById('username1').value;
        // var _email = document.getElementById('email').value;
        // if (checkEmail(_email)) {
            //邮箱格式正确

        // }

}


function fillout(notelist){
    var deletelist = notelist.deletelist;
            var collectlist = notelist.collectlist;
            var usagelist = notelist.usagelist;
            // alert('deletelist-length'+deletelist.length)
            //设置长度
            // $('#deletenum').text('共有'+deletelist.length+'篇笔记')
            $('.deletenum').text(deletelist.length)
            // //console.log('deletelist-length:'+deletelist.lenth)
            for (var d in deletelist){
                if (d>=5){
                    break;
                }
                //console.log('d[id]:'+deletelist[d].id)
                var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+deletelist[d].title+" <button class='btn btn-link btn-xs btn-danger' onclick='recover2_note("+deletelist[d].id+")'  style='float: right;'><i class='fas fa-redo'></i> 恢复</button></span> <span class=time>"+deletelist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                $('#deletelist').append(str)
            }


            //填充回收站列表

            //填充我的收藏列表
             //设置长度
            // $('.collectnum').text('共有'+collectlist.length+'篇笔记')
            $('.collectnum').text(collectlist.length)
            // //console.log('deletelist-length:'+deletelist.lenth)
            for (var d in collectlist){
                if (d>=5){
                    break;
                }
                //console.log('d[id]:'+collectlist[d].id)
                var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+collectlist[d].title+" <button class='btn btn-link btn-xs' onclick='get_note("+collectlist[d].id+',0'+")'  style='float: right;'><i class='far fa-folder-open'></i> 查看</button></span> <span class=time>"+collectlist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                $('#collectlist').append(str)
            }
            //填充我的收藏列表


            //填充左侧分类列表
            //设置长度
            $('.totalnum').text(usagelist.length)
            // //console.log('deletelist-length:'+deletelist.lenth)
            var sortnum=[]
            for(var i=1;i<=13;i++){
                sortnum[i]=0;
            }
            // var sortnum1=0,sortnum2=0,sortnum3=0,sortnum4=0,sortnum5=0,sortnum6=0,sortnum7=0,sortnum8=0,sortnum9=0,sortnum10=0,sortnum11=0,sortnum12=0,sortnum13=0;
            for (var d in usagelist){
                //console.log('sort[id]:'+usagelist[d].sort_id)
                var sortId = 'sort'+usagelist[d].sort_id;
                //console.log(sortId)
                var str = "<li> <a onclick='get_note("+usagelist[d].id+",0)' style='cursor: pointer'> <span class='sub-item'>"+usagelist[d].title+"</span> </a> </li>"
                $('#'+sortId).append(str)
                // eval(sortnum+usagelist[d].sort_id)=1;
                sortnum[usagelist[d].sort_id]++;
            }
            for(var i=1;i<=13;i++){
                $('.sortnum'+i).text(sortnum[i])
            }
}



//从回收站恢复笔记
function recover2_note(nid){
     //console.log('nid:' + nid)
    // //console.log('this:' + obj)
    // var rowIndex = obj.parentElement.parentElement.rowIndex;
    // //console.log('rowIndex:' + rowIndex)
    // if (rowIndex < 0)
    //     return;
    // // alert(rowIndex)



    //
    swal({
            title: '是否确认从回收站恢复？?',
            text: "恢复后可以查看和编辑",
            type: 'warning',
            buttons: {
              cancel: {
                visible: true,
                text: '取消',
                className: 'btn btn-danger'
              },
              confirm: {
                text: '确认恢复',
                className: 'btn btn-success'
              }
            }
          }).then((willDelete) => {
            if (willDelete) {

              //  ajax
                   var tab = document.getElementById('recyclelist')
    // obj.parents().parents().remove();
    //             tab.deleteRow(rowIndex);  //测试成功  删除成功
    // var jsonstr = {"action": 'delete_note', "nid": nid,"n_type":n_type};


    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=recover_note&nid='+nid,
        // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0 && data.msg == '恢复成功') {
                //console.log('恢复成功')
                // var preDom = obj.previousElementSibling;
                // preDom.click();//成功  明天吧<i>隐藏了
                // var n = parseInt($('.deletenum').eq(0).text())
                // alert(n)
                // $('.deletenum').text(n-1)
var notelist = data.notelist;
            fillout(notelist)

                swal("恢复成功", {
                icon: "success",
                buttons: {
                  confirm: {
                    className: 'btn btn-success'
                  }
                }
              });
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
              //  ajax


            } else {
              swal("已取消恢复", {
                buttons: {
                  confirm: {
                    className: 'btn btn-success'
                  }
                }
              });
            }
          });
    //





    // obj.parents().parents().remove();
    //             tab.deleteRow(rowIndex);  //测试成功  删除成功
    // var jsonstr = {"action": 'recover_note', "id": nid};




}



//查看该分类的所有笔记列表
function get_sort_list(sid){
    if(sid == 0)
    {
        //0代表查看全部笔记  直接打开list.html就可以
        location.href = './list.html'
        return;
    }
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=get_sort_list&sid='+sid,
        // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0) {
                //console.log('传参成功')
                url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
            }



        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
}

//查看或者编辑笔记
function get_note(nid,n_type){
    // alert(1)
    //type = 0 为查看笔记    type=1 为编辑笔记
    //console.log('nid : '+nid+'  n_type: '+n_type);
    var jsonstr = {"action": 'get_note', "nid": nid,'n_type':n_type};
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=get_note&nid='+nid+'&n_type='+n_type,
        data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0) {
                // alert('传参成功')
                //console.log('传参成功')
                var url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
            }


            //获取触发函数的元素
            // let obj = this;
            // var tab = $('#notelist')
            // var rowIndex = obj.parentElement.parentElement.rowIndex;
            // //console.log('rowIndex:'+rowIndex)
            // // // alert(rowIndex)
            // tab.deleteRow(rowIndex);  //测试成功  删除成功
            // alert(obj.parent().parent())
            // obj.parent().parent().remove();

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
}

//    退出登录
function signout() {
    $.ajax({
        type: "GET",  //这里退出不需要传参数。get和post都可以
        url: '/api/mgr/signout',
        // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0) {
                alert('退出成功get')
            } else {
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


//查询笔记find_note
function find_note(){
    // alert(1)
    var keyword = $('#searchinput').val()
    // console.log(keyword)
    $.ajax({
        type: "GET",  //这里退出不需要传参数。get和post都可以
        url: '/api/mgr/note?action=find_note&keyword='+keyword,
        // data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0) {
                searchlist = data.retlist
                if (searchlist.length <= 0)
                {
                    $('#searchlist').text('未查询到结果')
                    return;
                }
                $('#searchnum').text(searchlist.length)
                for (var d in searchlist){
                //console.log('d[id]:'+collectlist[d].id)
                    if (!searchlist[d].deleted)
                    {
                        var str = "<li  onclick='get_note("+searchlist[d].id+',0'+")' style='cursor: pointer'> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+searchlist[d].title+" </span> <span class=time>"+searchlist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                        $('#searchlist').append(str)
                    }
            }
            } else{
                alert('查询失败')
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
}


//点击回收站  进入回收站
function open_page(id)
{
    if (id == 0)//打开我的收藏
    {
        location.href = './collection.html'
    }
    else if (id ==1)
    {
        //打开回收占】
        location.href = './recycle.html'

    }
}