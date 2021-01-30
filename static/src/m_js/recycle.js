//处理index.html的js
$(document).ready(function () {
    // alert(0)
    // initPage()
    var table = $('#recyclelist').DataTable({
        // "ajax": '/api/mgr/note?action=list_note',
        responsive: true,
        "columns": [
            {data: "title"},
            {data: "content"},
            {data: "keyword"},
            {data: "abstract"},
            {data: "publish_date"},
            // {data: "title"},
        ],

        // 通过ajax向后台controller请求数据
        ajax: {
            url: "/api/mgr/note?action=list_note",
            dataSrc: "data",
            data: function (d) {
                var sid = -1;//传入参数-1   代表查询回收站的列表
// 添加额外的参数传给服务器
                d.sid = sid;
            }
        },
        "columnDefs": [{
// 定义操作列,######以下是重点########
            "targets": 5,//操作按钮目标列
            "data": null,
            "render": function (data, type, row) {
                var id = '"' + row.id + '"';
                var html = "<i class='delete' style='display: none'></i><a href='javascript:void(0);' onclick='recover_note(" + id + ',this' + ")'  class='btn btn-link btn-xs'  ><i class='fas fa-redo'></i> 恢复</a>"
                html += "<i class='delete' style='display: none'></i><a href='javascript:void(0);'    class='btn btn-link btn-danger btn-xs' onclick='delete_note(" + id + ',this' +',1' +")' ><i class='fa fa-times'></i> 彻底删除</a>"
                //                 html += "<i class='delete' style='display: none'></i><a href='javascript:void(0);'    class='btn btn-link btn-danger btn-xs' onclick='recover_note(" + id + ',this' + ")' ><i class='fa fa-times'></i> 删除</a>"

                return html;
            }
        }],


        language: {
            "processing": "处理中...",
            "lengthMenu": "显示 _MENU_ 项结果",
            "zeroRecords": "没有匹配结果",
            "info": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "infoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "infoFiltered": "(由 _MAX_ 项结果过滤)",
            "infoPostFix": "",
            "search": "搜索:",
            "url": "",
            "emptyTable": "表中数据为空",
            "loadingRecords": "载入中...",
            "infoThousands": ",",
            "paginate": {
                "first": "首页",
                "previous": "上页",
                "next": "下页",
                "last": "末页"
            },
            "aria": {
                "sortAscending": ": 以升序排列此列",
                "sortDescending": ": 以降序排列此列"
            }
        }

    });

    //获取其他数据

    initPage()
    //获取其他数据


    // 初始化刪除按钮
    $('#recyclelist tbody').on('click', 'i.delete', function (e) {
        // alert('del')
        e.preventDefault();

        // if (confirm("确定要删除该属性？")) {
        var table = $('#recyclelist').DataTable();
        table.row($(this).parents('tr')).remove().draw();
        // //console.log(table.row($(this).parents('tr')).data())

        // }


    });

    // alert(1)
})


//从回收站恢复笔记
function recover_note(nid,obj){
     //console.log('nid:' + nid)
    //console.log('this:' + obj)
    var rowIndex = obj.parentElement.parentElement.rowIndex;
    //console.log('rowIndex:' + rowIndex)
    if (rowIndex < 0)
        return;
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
                var preDom = obj.previousElementSibling;
                preDom.click();//成功  明天吧<i>隐藏了

                 var notelist = data.notelist;
            fillout(notelist);

                
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

//删除该笔记
function delete_note(nid, obj,n_type) {
    // alert('del2')
    // var table = $('#notelist').DataTable();
    //                     table.row($(this).parents('tr')).remove().draw();
    //console.log('nid:' + nid)
    //console.log('this:' + obj)
    var rowIndex = obj.parentElement.parentElement.rowIndex;
    //console.log('rowIndex:' + rowIndex)
    if (rowIndex < 0)
        return;
    // // alert(rowIndex)

    swal({
            title: '是否确认将该笔记彻底删除?',
            text: "彻底删除后无法恢复",
            type: 'warning',
            buttons: {
              cancel: {
                visible: true,
                text: '取消',
                className: 'btn btn-danger'
              },
              confirm: {
                text: '确认删除',
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
   var jsonstr = {"action": 'delete_note', "nid": nid,"n_type":n_type};

     $.ajax({
        type: "DELETE",
        url: '/api/mgr/note',
        data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
        dataType: "json",
        success: function (data) {
            if (data.ret == 0 && data.msg == '删除成功') {
                //console.log('删除成功')
                var preDom = obj.previousElementSibling;
                preDom.click();//成功  明天吧<i>隐藏了


                  var notelist = data.notelist;
            fillout(notelist);


                swal("删除成功", {
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
              swal("已取消删除", {
                buttons: {
                  confirm: {
                    className: 'btn btn-success'
                  }
                }
              });
            }
          });
    //


    // var tab = document.getElementById('notelist')
    // obj.parents().parents().remove();
    //             tab.deleteRow(rowIndex);  //测试成功  删除成功





}

// $("#basic-datatables").dataTable({
//                 // "language": lang,
//                 "destroy":true, //这个如果不加的话不能够再次调用这个函数
//                 "ajax":function (data,callback,setting) {
//                     $.ajax({
//                         url:"/api/mgr/note?action=list_note",
//                         success:function (returnData) {
//                             //这边只是为了修改数据的格式使其符合datatable的数据格式
//                             //console.log(data);
//                             var result={};
//                             result.data=returnData.retlist;
//                             callback(result)
//                         }
//                     })
//                 },
//                 "columns": [
//                     {
//                         "data": "title",
//                         "title":"标题"
//                     },
//                     {
//                         "data": "content",
//                         "title":"内容"
//                     },
//                     {
//                         "data": "关键字",
//                         "title":"keyword"
//                     },
//                     {
//                         "data": "摘要",
//                         "title":"abstract"
//                     }
//                 ]
//             });
//


//初始化页面
function initPage() {
    // alert('ii')
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=init_nav',
        // data:'id='+id,
        dataType: "json",
        success: function (data) {
            if (data.ret == 302 && data.msg == '未登录') { //查询成功
                alert('未登录')
                url = data.redirect; //获取服务端返回的要重定向的页面
                location.href = url
            }

            user = data.user
            document.getElementById('username').innerText = user.username
            document.getElementById('useremail').innerText = user.email
            document.getElementById('userid').value = user.id
            // document.getElementById('user_last_login').innerText = user.last_login
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


function fillout(notelist){
    var deletelist = notelist.deletelist;
            var collectlist = notelist.collectlist;
            var usagelist = notelist.usagelist;
            // alert('deletelist-length'+deletelist.length)
            //设置长度
            // $('#deletenum').text('共有'+deletelist.length+'篇笔记')
            $('.deletenum').text(deletelist.length)
            // //console.log('deletelist-length:'+deletelist.lenth)
            $('#deletelist').html(null)
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
    $('#collectlist').html(null)
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
                // alert(sortnum[i])
            }
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
                var str = "<li  onclick='get_note("+searchlist[d].id+',0'+")' style='cursor: pointer'> <a> <div class='notif-content' style='width: 100%'> <span class=subject>"+searchlist[d].title+" </span> <span class=time>"+searchlist[d].content.substring(0,14)+"...</span> </div> </a> </li>";
                $('#searchlist').append(str)
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
