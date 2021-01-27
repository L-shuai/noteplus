//处理index.html的js
$(document).ready(function () {
    // alert(0)
    // initPage()
    var table = $('#notelist').DataTable({
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
//             data: function (d) {
//                 var searchContent = $(
//                     '#searchContent').val();
// // 添加额外的参数传给服务器
//                 d.extra_search = searchContent;
//             }
        },
        "columnDefs": [{
// 定义操作列,######以下是重点########
            "targets": 5,//操作按钮目标列
            "data": null,
            "render": function (data, type, row) {
                var id = '"' + row.id + '"';
                var html = "<a href='javascript:void(0);'  class='delete btn btn-link btn-xs'  ><i class='far fa-folder-open'></i> 查看</a>"
                html += "<a href='javascript:void(0);' class='up btn btn-link btn-xs'><i class='fas fa-edit'></i> 编辑</a>"
                html += "<i class='delete'></i><a href='javascript:void(0);'    class='btn btn-link btn-danger btn-xs' onclick='delete_note(" + id +',this'+ ")' ><i class='fa fa-times'></i> 删除</a>"
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

    // 初始化刪除按钮
    //             $('#notelist tbody').on('click', 'a.delete', function(e) {
    //                 alert('del')
    //                 e.preventDefault();
    //                 console.log('$(this):'+$(this).innerText)
    //                 console.log('e:'+e.innerHtml)
    //                 console.log('$e:'+$(e))
    //                 // if (confirm("确定要删除该属性？")) {
    //                     var table = $('#notelist').DataTable();
    //                     table.row($(this).parents('tr')).remove().draw();
    //                     // console.log(table.row($(this).parents('tr')).data())
    //
    //                 // }
    //
    //
    //             });

    // alert(1)
})


//删除该笔记
function delete_note(nid,obj){
    alert('del2')


    // delDT(table,DT)
    // var table = $('#notelist').DataTable();
    //                     table.row($(this).parents('tr')).remove().draw();
    console.log('nid:'+nid)
    console.log('this:'+obj)
    var rowIndex = obj.parentElement.parentElement.rowIndex;
                console.log('rowIndex:'+rowIndex)
    if (rowIndex<0)
        return;
                // // alert(rowIndex)
    var tab = document.getElementById('notelist')
    // obj.parents().parents().remove();
    //             tab.deleteRow(rowIndex);  //测试成功  删除成功
    var jsonstr = {"action": 'del_note', "id": nid};


        $.ajax({
            type: "DELETE",
            url: '/api/mgr/note',
            data: JSON.stringify(jsonstr),//将json对象转换成json字符串发送
            dataType: "json",
            success: function (data) {
                console.log('删除成功')


                 // 初始化刪除按钮
                $('#notelist tbody').on('click', 'i.delete', function(e) {
                    alert('del')
                    e.preventDefault();
                    console.log('$(this):'+$(this).innerText)
                    console.log('e:'+e.innerHtml)
                    console.log('$e:'+$(e))
                    // if (confirm("确定要删除该属性？")) {
                        var table = $('#notelist').DataTable();
                        table.row($(this).parents('tr')).remove().draw();
                        // console.log(table.row($(this).parents('tr')).data())

                    // }


                });

                var preDom = obj.previousElementSibling;
                preDom.click();//成功  明天吧<i>隐藏了

                //获取触发函数的元素
                // let obj = this;
                // var tab = $('#notelist')
                // var rowIndex = obj.parentElement.parentElement.rowIndex;
                // console.log('rowIndex:'+rowIndex)
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

// $("#basic-datatables").dataTable({
//                 // "language": lang,
//                 "destroy":true, //这个如果不加的话不能够再次调用这个函数
//                 "ajax":function (data,callback,setting) {
//                     $.ajax({
//                         url:"/api/mgr/note?action=list_note",
//                         success:function (returnData) {
//                             //这边只是为了修改数据的格式使其符合datatable的数据格式
//                             console.log(data);
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
    alert('ii')
    $.ajax({
        type: "GET",
        url: '/api/mgr/note?action=list_note',
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

            console.log(data.retlist)
            $('#tbody').html("<tr><td>" + "jfp" + "</td><td>" + "fiob" + "</td><tr>")
            alert('ok')
            $.each(data.retlist, function (index, val) {
                //this必须加引号，否则报错
                // $('#basic-datatables').append("<tr><td>" + val.title + "</td><td>" + val.content + "</td><td>" + val.keyword + "</td><td>" + val.abstract + "</td><td>" + val.publish_date + "</td><td>" + " " +
                //     "<button class="btn btn-link" style="float: left;"   data-toggle="tooltip"  data-original-title="查看" onclick=edit_customer(" + val.id + ")> <i class="fas fa-book-open" style="font-size: 18px;"></i></button>" + "" +
                // "<button onclick=delete_customer(" + val.id + ",this" + ")>删除</button>" + "</td></tr>")
                // $('#tbody').innerHTML="<tr><td>" + val.title + "</td><td>" + val.content + "</td><tr>"
                // $('#basic-datatables').append("<tr><td>" + val.title + "</td><td>" + val.content + "</td><td>" + val.keyword + "</td><td>" + val.abstract + "</td><td>" + val.publish_date + "</td><td>" + "<button onclick=edit_customer(" + val.id + ")>编辑</button>" + "<button onclick=delete_customer(" + val.id + ",this" + ")>删除</button>" + "</td></tr>")

            });

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
