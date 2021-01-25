// 处理创建笔记
// alert('note.js')

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
        path: "./src/assets/editor.md-master/lib/",
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
    // 获取html值
    var html = testEditor.getHTML()
    $('#preview').html(html)
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


//初始化页面
function initPage() {
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

// alert('note.js  over')

