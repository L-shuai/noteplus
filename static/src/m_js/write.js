// 处理创建笔记
// alert('write.js')

$(document).ready(function(){
        initPage()
})

var testEditor;
$(function () {
    testEditor = editormd("test-editormd", {
        width: "100%",  //宽度
        height: 640,  //高度
        syncScrolling: "single",  //
        // 一定要改
        path: "../static/src/assets/editor.md-master/lib/",
        autoFocus: true,  //页面打开时自动获取焦点
        //这个配置可以让构造出来的HTML代码直接在第二个隐藏的textarea域中，方便post提交表单。
        saveHTMLToTextarea: true,
    });
    // 这里必须先声明，上面的js按钮才能用
    testEditor.getMarkdown();       // 获取 Markdown 源码
    testEditor.getHTML();           // 获取 Textarea 保存的 HTML 源码
    testEditor.getPreviewedHTML();  // 获取预览窗口里的 HTML，在开启 watch 且没有开启 saveHTMLToTextarea 时使用
});

// 点击右上角的预览按钮

function preview() {
    // alert(1)
    // 获取html值
    var html = testEditor.getHTML()
    $('#preview').html(html)

        //显示出编辑按钮
        document.getElementById('pills-home-tab').style.display='inline'
    //隐藏预览按钮
    document.getElementById('pills-profile-tab').style.display='none'
}

function getMD() {
    // 获取markdown值
    var md = testEditor.getMarkdown()
    // alert(md)
    console.log('获取到的md:'+md)
    testEditor.value = ""
    return md;
}

function getHtml() {
    // 获取html值
    var html = testEditor.getHTML()
    // alert(html)
    console.log('获取到的html:'+html)
    return html;
}

function setMD() {
    var cont = "为Editor赋值..."
    // testEditor.setMarkdown();
    // document.getElementById("editormd").value="这是editormd"
    // cont = document.getElementById("textarea").value;
    // alert(cont)
    // 直接从数据库中读出   可以得
    testEditor.setMarkdown(cont)
}

//点击编辑按钮
function edit_note()
{

    document.getElementById('pills-home-tab').style.display='none'
    document.getElementById('pills-profile-tab').style.display='inline'
}

//初始化页面
function initPage() {
    //默认在编辑框页面时   编辑按钮隐藏
    document.getElementById('pills-home-tab').style.display='none'
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=init_page_note',
        // data:'id='+id,
        dataType: "json",
        success: function (data) {
            if (data.ret == 302 && data.msg == '未登录') {
                alert('未登录')
                url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
            }
            // alert('ok')
            user = data.user
            document.getElementById('username').innerText = user.username
            document.getElementById('useremail').innerText = user.email
            document.getElementById('userid').value = user.id
            // document.getElementById('user_last_login').innerText = user.last_login

            //填充回收站列表
            // $('#deletelist').html('<h1>test</h1>')
            // $('#deletelist').append("<li id='new'> new Li </li>");
            var notelist = data.notelist;
            fillout(notelist)
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
}


function addnote(){
    console.log('add_note')
//    添加笔记
    var title = document.getElementById('title').value
    var content_md = getMD()
    var content_html = getHtml()
    var userid = document.getElementById('userid').value
    if (title=='' || title==null)
    {
        swal("warning", "笔记标题不能为空", {
                    icon: "warning",
                    buttons: {
                        confirm: {
                            className: 'btn btn-warning'
                        }
                    },
                });
        return;
    }
    if (content_md=='' || content_md==null)
    {
        swal("warning", "笔记内容不能为空", {
                    icon: "warning",
                    buttons: {
                        confirm: {
                            className: 'btn btn-warning'
                        }
                    },
                });
        return;
    }
    var jsonstr = {"action": 'add_note', 'data': {'userid':userid,'note':{'title':title,'content_md':content_md,'content_html':content_html}}};
        $.ajax({
            type: "POST",
            url: '/api/mgr/note',
            data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
            dataType: "json",
            success: function (data) {
                // alert('添加成功  id=' + data.id)
                // alert(data.id)
                var sort = data.sort
                 //选中select
                $("#sortSelect").val(data.note.sort);
                // alert(data.note.sort)
                // alert(data.sort)
                 var notelist = data.notelist;
                 fillout(notelist);

                //填充底部的笔记摘要和关键字 以及词云图
                // //console.log('data.note:'+data.note)
                fill_abstract(data.note);

                swal("保存成功", "为您预测的笔记分类为："+data.sort, {
                    icon: "success",
                    buttons: {
                        confirm: {
                            className: 'btn btn-success'
                        }
                    },
                });

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.status);
                alert(XMLHttpRequest.readyState);
                alert(textStatus);
            }
        });
}

// alert('write.js  over')
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




//填充底部的摘要和关键字以及词云图
function fill_abstract(note){
    abs_list = note['abstract']
    key_list = note['keyword']
    //console.log("abs_list:"+abs_list)
    //console.log("key_list:"+key_list)
    $('#abstract_list').html(null)
//    填充笔记摘要
    for (var d in abs_list){
        //console.log(abs_list[d])
        // var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+deletelist[d].title+" <button class='btn btn-link btn-xs btn-danger' onclick='recover2_note("+deletelist[d].id+")'  style='float: right;'><i class='fas fa-redo'></i> 恢复</button></span> <span class=time>"+deletelist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
        var str = "<li> <p>"+abs_list[d]+"</p> </li>"
        $('#abstract_list').append(str)
    }
    $('#keyword_list').html(null)
    //    填充关键字
    for (var d in key_list){
        //console.log(key_list[d])
        // var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+deletelist[d].title+" <button class='btn btn-link btn-xs btn-danger' onclick='recover2_note("+deletelist[d].id+")'  style='float: right;'><i class='fas fa-redo'></i> 恢复</button></span> <span class=time>"+deletelist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
        var str = "<li class='d-flex justify-content-between pb-1 pt-1' style='float: left;margin-left: 10px;'> <button class='btn btn-default btn-round  btn-xs'>"+key_list[d]+"</button> </li>"
        $('#keyword_list').append(str)
    }
//    设置词云图src
    $('#wordcloud').attr('src',note.img_url)

}

function fillout(notelist){
    var deletelist = notelist.deletelist;
            var collectlist = notelist.collectlist;
            var usagelist = notelist.usagelist;
            // alert('deletelist-length'+deletelist.length)
            //设置长度
            // $('#deletenum').text('共有'+deletelist.length+'篇笔记')
            $('.deletenum').text(deletelist.length)
    $('#deletelist').html(null)
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
    $('#collectlist').html(null)
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
                $('#sort'+i).html(null)
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


//查看或者编辑笔记
function get_note(nid,n_type){
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
                //console.log('传参成功')
                url = data.redirect; //获取服务端返回的要重定向的页面
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

