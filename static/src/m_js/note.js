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
        autoFocus: true,  //页面打开时不自动获取焦点
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
    var b = document.getElementById('preview-input').value
    if (b!=1)
    {
            // 获取html值
    var html = testEditor.getHTML()
    console.log('html-preview:'+html)
        $('#preview').html(html)
    }


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

function setMD(cont) {
    // var cont = "为Editor赋值..."
    // testEditor.setMarkdown();
    // document.getElementById("editormd").value="这是editormd"
    // cont = document.getElementById("textarea").value;
    // alert(cont)
    // 直接从数据库中读出   可以得
    testEditor.setMarkdown(cont)
}


//初始化页面
function initPage() {
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=get_note_byid',
        // data:'id='+id,
        dataType: "json",
        success: function (data) {
            if (data.ret == 302 && data.msg == '未登录') {
                alert('未登录')
                var url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
            }


            // alert('ok')
            if (data.ret == 0)
            {
                var user = data.user
            document.getElementById('username').innerText = user.username
            document.getElementById('useremail').innerText = user.email
            document.getElementById('userid').value = user.id
            var note = data.note
            setMD(note.content_md)
                document.getElementById('title').value = note.title
                document.getElementById('preview-input').value = 1
            //选中sort select
                console.log('note.sort_id:'+note.sort)
                $('#sortSelect').val(note.sort)
            //判断是查看还是编辑   n_type=0 | 1
            if (data.n_type==0)//是查看   需进入预览
            {
                // alert('0')
                // preview()
                document.getElementById('preview').innerHTML = note.content_html
                console.log('note.content_html:'+note.content_html)
                document.getElementById('pills-profile-tab').click()
                // preview()
            }
            }

            var notelist = data.notelist;
            fillout(notelist)

            // document.getElementById('user_last_login').innerText = user.last_login
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


function addnote(){
//    添加笔记
    var title = document.getElementById('title').value
    var content_md = getMD()
    var content_html = getHtml()
    var userid = document.getElementById('userid').value

    var jsonstr = {"action": 'add_note', 'data': {'userid':userid,'note':{'title':title,'content_md':content_md,'content_html':content_html}}};
        $.ajax({
            type: "POST",
            url: '/api/mgr/note',
            data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
            dataType: "json",
            success: function (data) {
                alert('添加成功  id=' + data.id)
                // alert(data.id)
                swal("保存成功", "You clicked the button!", {
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

function fillout(notelist){
    var deletelist = notelist.deletelist;
            var collectlist = notelist.collectlist;
            var usagelist = notelist.usagelist;
            // alert('deletelist-length'+deletelist.length)
            //设置长度
            // $('#deletenum').text('共有'+deletelist.length+'篇笔记')
            $('.deletenum').text(deletelist.length)
            // console.log('deletelist-length:'+deletelist.lenth)
            $('#deletelist').html(null)
            for (var d in deletelist){
                if (d>=5){
                    break;
                }
                console.log('d[id]:'+deletelist[d].id)
                var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+deletelist[d].title+" <button class='btn btn-link btn-xs btn-danger' onclick='recover2_note("+deletelist[d].id+")'  style='float: right;'><i class='fas fa-redo'></i> 恢复</button></span> <span class=time>"+deletelist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                $('#deletelist').append(str)
            }


            //填充回收站列表

            //填充我的收藏列表
             //设置长度
            // $('.collectnum').text('共有'+collectlist.length+'篇笔记')
            $('.collectnum').text(collectlist.length)
            // console.log('deletelist-length:'+deletelist.lenth)
    $('#collectlist').html(null)
            for (var d in collectlist){
                if (d>=5){
                    break;
                }
                console.log('d[id]:'+collectlist[d].id)
                var str = "<li> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+collectlist[d].title+" <button class='btn btn-link btn-xs' onclick='get_note("+collectlist[d].id+',0'+")'  style='float: right;'><i class='far fa-folder-open'></i> 查看</button></span> <span class=time>"+collectlist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                $('#collectlist').append(str)
            }
            //填充我的收藏列表


            //填充左侧分类列表
            //设置长度
            $('.totalnum').text(usagelist.length)
            // console.log('deletelist-length:'+deletelist.lenth)
            var sortnum=[]
            for(var i=1;i<=13;i++){
                sortnum[i]=0;
            }
            // var sortnum1=0,sortnum2=0,sortnum3=0,sortnum4=0,sortnum5=0,sortnum6=0,sortnum7=0,sortnum8=0,sortnum9=0,sortnum10=0,sortnum11=0,sortnum12=0,sortnum13=0;
            for (var d in usagelist){
                console.log('sort[id]:'+usagelist[d].sort_id)
                var sortId = 'sort'+usagelist[d].sort_id;
                console.log(sortId)
                var str = "<li> <a onclick='get_note("+usagelist[d].id+",0)' style='cursor: pointer'> <span class='sub-item'>"+usagelist[d].title+"</span> </a> </li>"
                $('#'+sortId).append(str)
                // eval(sortnum+usagelist[d].sort_id)=1;
                sortnum[usagelist[d].sort_id]++;

            }
            for(var i=1;i<=13;i++){
                $('.sortnum'+i).text(sortnum[i])
                // alert(sortnum[i])
            }
}
