/**
 * Created by buhe on 2017/1/22.
 */



    // 数据初始化

    function load_data(search_items) {
        $('#manager').datagrid({
            url: '/cmdb/get_data/',
            queryParams: {
                search_items: search_items,
            },
            traditional: true,
            loadMsg: '数据加载中...',
            fit: true,
            fitColumns: true,
            striped: true,
            rownumbers: true,
            border: false,
            pagination: true,
            pageSize: 20,
            pageList: [10, 20, 30, 40, 50],
            pageNumber: 1,
            sortName: 'id',
            sortOrder: 'desc',
            remoteSort: false,
            toolbar: '#manage_toolbar',
            frozenColumns: [[
                {
                    field: 'id',
                    title: '序号',
                    width: 10,
                    checkbox: true,
                },
                {
                    field: 'idc',
                    title: 'IDC',
                    width: 120,
                    sortable: true,
                    align: 'center',
                    editor: {
                        type: 'combobox',
                        options: {
                            method: 'get',
                            url: '/cmdb/get_idc_all/',
                            valueField: 'name',
                            textField: 'name',
                            editable: false,
                            required: true,
                        },
                    },
                },
                {
                    field: 'ip',
                    title: 'IP地址',
                    width: 100,
                    //sortable: true,
                    align: 'center',
                },
            ]],
            columns: [[
                {
                    field: 'sn',
                    title: 'SN',
                    width: 60,
                    //sortable: true,
                    align: 'center',
                },
                {
                    field: 'asset_type',
                    title: '资产类型',
                    width: 60,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'combobox',
                        options: {
                            method: 'get',
                            url: '/cmdb/get_asset_type_all/',
                            valueField: 'asset_value',
                            textField: 'asset_name',
                            editable: false,
                            required: true,
                        },
                    },
                },
                {
                    field: 'manufactory',
                    title: '生产厂商',
                    width: 40,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'combobox',
                        options: {
                            method: 'get',
                            url: '/cmdb/get_manufactory_all/',
                            valueField: 'manufactory',
                            textField: 'manufactory',
                            editable: false,
                            required: true,
                        },
                    },
                },
                {
                    field: 'model',
                    title: '设备型号',
                    width: 60,
                    //sortable: true,
                    align: 'center',
                },
                {
                    field: 'os_type',
                    title: '操作系统',
                    width: 60,
                    //sortable: true,
                    align: 'center',
                },
                {
                    field: 'os_version',
                    title: '系统版本',
                    width: 80,
                    //sortable: true,
                    align: 'center',
                },
                {
                    field: 'configuration',
                    title: '配置(CPU/内存/硬盘)',
                    width: 80,
                    //sortable: true,
                    align: 'center',
                },
                {
                    field: 'admin',
                    title: '运维人',
                    width: 40,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                {
                    field: 'user',
                    title: '使用人',
                    width: 40,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                {
                    field: 'use_dept',
                    title: '使用部门',
                    width: 60,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                /*{
                    field: 'use_dept',
                    title: '存活状态',
                    width: 200,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                {
                    field: 'use_dept',
                    title: '空闲状态',
                    width: 120,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                {
                    field: 'use_dept',
                    title: '系统口令',
                    width: 120,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },
                {
                    field: 'use_dept',
                    title: 'ILO口令',
                    width: 120,
                    //sortable: true,
                    align: 'center',
                    editor: {
                        type: 'validatebox',
                        options: {
                            required: true,
                        },
                    },

                },*/
                {
                    field: 'option_data',
                    title: '操作',
                    width: 40,
                    //sortable: true,
                    align: 'center',
                    formatter: function (value, row, index) {
                        return '<a href="#" class="easyui-linkbutton l-btn l-btn-small l-btn-selected" style="height:20px;line-height:20px" onclick="server_detail_fn(' + row.id + ')">查看详情</a>';
                    }

                },
            ]],
        });

        // 初始化分页
        $('#manager').datagrid('getPager').pagination({
            beforePageText: '第',
            afterPageText: '页 共{pages}页',
            displayMsg: '当前显示{from}-{to}条记录 共{total}条数据',
        });

    };

    var editIndex = undefined
    manager_edit_tools = {
        check_selection: function(select_rows) {
            if (select_rows.length > 1) {
                $.messager.alert('提示', '只能勾选一项进行修改！', 'warning');
                return false;
            }
            else if (select_rows.length == 0){
                $.messager.alert('提示', '请勾选一条数据进行修改！', 'warning');
                return false;
            }
            else {
                return true;
            }
        },
        endedit: function endEditing(editIndex) {
            //校验指定的行，如果有效返回true
            if ($('#manager').datagrid('validateRow', editIndex)) {
                $('#manager').datagrid('endEdit', editIndex);
                return true;
            } else {
                return false;
            }
        },
        edit: function () {
            var rows = $('#manager').datagrid('getSelections');
            if (manager_edit_tools.check_selection(rows)) {
                $("#manager_edit_btn").hide();
                $("#manager_edit_toolbar").show();
                var row_index = $('#manager').datagrid('getRowIndex', rows[0]);
                editIndex = row_index
                $('#manager').datagrid('beginEdit', row_index);
            }
        },
        save: function() {
            if (manager_edit_tools.endedit(editIndex)) {
                //获取更新更改的行的集合
                var row = $("#manager").datagrid('getChanges');
                console.log(row)

                if (row.length) {
                    $.ajax(
                        {
                            type: 'POST',
                            url: "/cmdb/manager_data_edit/",
                            data: { edit_data: JSON.stringify(row), },
                            success: function (data) {
                                if (data == 1) {
                                    $.messager.show({
                                        title: '提示',
                                        msg: '数据修改成功',
                                    });
                                }
                                else {
                                    $.messager.alert('提示信息', '保存失败，请联系管理员！', 'warning');
                                    $("#manager").datagrid('reload');
                                }
                            }
                        });
                }
                else  //如果没有修改数据，则提醒用户
                {
                    $.messager.alert('提示信息', '您还没有修改信息！', 'warning');
                }
                $('#manager').datagrid('clearSelections');
                $("#manager_edit_toolbar").hide();
                $("#manager_edit_btn").show();
                editIndex = undefined
            }
        },
        reject: function() {
            $('#manager').datagrid('rejectChanges');
            $("#manager_edit_toolbar").hide();
            $("#manager_edit_btn").show();
        }
    }

    // 默认数据加载
    function load_default_data() {
        load_data(JSON.stringify([{'tag': 'default', 'operator': '', 'value': ''}]));
    }

    load_default_data()

    // 数据查询
    function search_func() {
        var search_object = $('#search_object').combobox("getValue")
        var search_operator = $('#search_operator').combobox("getValue")
        var search_value = $('#search_value').val()
        var search_list = []
        var search_obj = {}

        search_obj['tag'] = search_object
        search_obj['operator'] = search_operator
        search_obj['value'] = search_value
        search_list.push(search_obj)

        load_data(JSON.stringify(search_list));
    }

    $('#manager_add').dialog({
        width: 350,
        title: '新增管理',
        modal: true,
        closed: true,
        buttons: [{
            text: '提交',
            iconCls: 'icon-add',
            handler: function () {
                if ($('#manager_add').form('validate')) {
                    $.ajax({
                        url: '/cmdb/add/',
                        type: 'post',
                        data: {
                            username: $('input[name="username"]').val(),
                            password: $('input[name="password"]').val(),
                            email: $('input[name="email"]').val(),
                        },
                        beforeSend: function () {
                            $.messager.progress({
                                text: '正在提交中...'
                            });
                        },
                        success: function (data, response, status) {
                            $.messager.progress('close');
                            if (data > 0) {
                                $.messager.show({
                                    title: '提示',
                                    msg: '新增用户成功',
                                });
                                $('#manager_add').dialog('close').form('reset');
                                $('#manager').datagrid('reload');
                            } else {
                                $.messager.alert('新增失败', '系统异常，请重试！', 'warning');
                            }
                        }
                    });
                }
            },
        },{
            text: '取消',
            iconCls: 'icon-redo',
            handler: function () {
                $('#manager_add').dialog('close').form('reset')
            },
        }],

    });


    $('#manager_edit').dialog({
        width: 350,
        title: '修改管理',
        modal: true,
        closed: true,
        buttons: [{
            text: '提交',
            iconCls: 'icon-add',
            handler: function () {
                if ($('#manager_edit').form('validate')) {
                    $.ajax({
                        url: '/cmdb/edit/',
                        type: 'post',
                        data: {
                            id_edit: $('input[name="id_edit"]').val(),
                            password_edit: $('input[name="password_edit"]').val(),
                            email_edit: $('input[name="email_edit"]').val(),
                        },
                        beforeSend: function () {
                            $.messager.progress({
                                text: '正在提交中...'
                            });
                        },
                        success: function (data, response, status) {
                            $.messager.progress('close');
                            if (data > 0) {
                                $.messager.show({
                                    title: '提示',
                                    msg: '数据修改成功',
                                });
                                $('#manager_edit').dialog('close').form('reset');
                                $('#manager').datagrid('reload');
                            } else {
                                $.messager.alert('修改失败', '系统异常，请重试！', 'warning');
                            }
                        }
                    });
                }
            },
        },{
            text: '取消',
            iconCls: 'icon-redo',
            handler: function () {
                $('#manager_edit').dialog('close').form('reset')
            },
        }],

    });

    // 表单验证

    $('input[name="username"]').validatebox({
        required: true,
        validType: 'length[2,20]',
        missingMessage: '请输入用户名称',
        invalidMessage: '用户名称为2-20位字符',
    });

    $('input[name="password"]').validatebox({
        required: true,
        validType: 'length[2,20]',
        missingMessage: '请输入用户密码',
        invalidMessage: '密码长度为2-20位字符',
    });

    $('input[name="email"]').validatebox({
        required: true,
        validType: 'email',
        missingMessage: '请输入用户邮箱',
        invalidMessage: '邮箱格式不正确',
    });

    manager_tool = {
        /*add: function () {
            $('#manager_add').dialog('open');
            $('input[name="username"]').focus();
        },*/
        add: function () {
            $('#manager').datagrid('insertRow', {
                index : 0,
                row : {

                },
            });
            $('#manager').datagrid('beginEdit', 0);
        },
        edit: function () {
            var rows = $('#manager').datagrid('getSelections')
            if (rows.length > 1){
                $.messager.alert('操作失败', '只能勾选一项进行修改', 'warning');
            } else if (rows.length == 0) {
                $.messager.alert('操作失败', '请勾选一个需要编辑的项', 'warning');
            } else if (rows.length == 1) {
                $.ajax({
                    url: '/cmdb/get_data_by_id/',
                    type: 'post',
                    data: {
                        id: rows[0].id,
                    },
                    beforeSend: function () {
                        $.messager.progress({
                            text: '正在获取中...'
                        });
                    },
                    success: function (data, response, status) {
                        $.messager.progress('close');
                        if (data.length > 0) {
                            var obj = $.parseJSON(data)
                            $('#manager_edit').form('load',{
                                //id : obj[0].id,
                                id_edit : obj[0].id,
                                username_edit : obj[0].username,
                                password_edit : obj[0].password,
                                email_edit : obj[0].email,
                            }).dialog('open')
                            /*$.messager.show({
                             title: '提示',
                             msg: '新增用户成功',
                             });
                             $('#manager_add').dialog('close').form('reset');
                             $('#manager').datagrid('reload');*/
                        } else {
                            $.messager.alert('获取失败', '系统异常，请重试！', 'warning');
                        }
                    }
                });
            }
        },
        remove: function () {
            var rows = $('#manager').datagrid('getSelections')
            if (rows.length == 0) {
                $.messager.alert('操作失败', '请至少勾选一个需要删除的项', 'warning');
            } else {
                $.messager.confirm('确定操作', '请问您确定要删除所选的项目吗？', function (flag) {
                    if (flag) {
                        var ids = [];
                        for (var i = 0; i<rows.length; i++) {
                            ids.push(rows[i].id);
                        }
                        $.ajax({
                            url: '/cmdb/delete/',
                            type: 'post',
                            traditional: true,
                            data: {
                                'id_delete': ids,
                            },
                            beforeSend: function () {
                                $.messager.progress({
                                    text: '正在删除中...'
                                });
                            },
                            success: function (data, response, status) {
                                $.messager.progress('close');
                                if (data.length > 0) {
                                    $.messager.show({
                                        title: '提示',
                                        msg: ids.length + '条数据删除成功',
                                    });
                                    $('#manager').datagrid('reload');
                                } else {
                                    $.messager.alert('删除失败', '系统异常，请重试！', 'warning');
                                }
                            }
                        });
                    }
                });
            }
        },
        data_management: function() {
            $("#data_management").show()
        },
        option_admin: function() {
            $("#modal_option_admin").window('open');
        },
    };

    data_management_tools = {
        open: function() {
            $("#data_management").show()
            $("#data_management_btn").attr('onclick', 'data_management_tools.close()')
        },
        close: function() {
            $("#data_management").hide()
            $("#data_management_btn").attr('onclick', 'data_management_tools.open()')
        }
    };



// 用于控制Excel表格上传组件
function excel_upload_tools() {

    $('#fb').filebox({
        buttonText: '选择文件',
        buttonAlign: 'right',
        width: 290,
        height: 30,
    })

    $('#excel_upload').dialog({
        width : 330,
        title : 'Excel 数据导入',
        modal : true,
        //closed : true,
        buttons : [
            {
                text : '提交',
                iconCls : 'icon-add',
                handler : function () {
                    if ($('#excel_upload').form('validate')) {
                        var upload_form_data = new FormData($( "#excel_upload" )[0]);
                        $.ajax({
                            url : '/cmdb/upload/',
                            type : 'POST',
                            data : upload_form_data,
                            processData: false,
                            contentType: false,
                            beforeSend : function () {
                                $.messager.progress({
                                    text : '正在导入Excel数据...',
                                });
                            },
                            success : function(data, response, status){
                                $.messager.progress('close');
                                if (data > 0) {
                                    $.messager.show({
                                        title : '提示',
                                        msg : 'Excel数据更新成功！',
                                    });
                                    $('#excel_upload').dialog('close').form('reset');
                                    $('#manager').datagrid('reload');
                                } else {
                                    $.messager.alert('警告操作', '未知错误，请联系系统管理员！', 'warning');
                                }
                            }
                        });
                    }
                },
            },
            {
                text : '取消',
                iconCls : 'icon-redo',
                handler : function () {
                    $('#excel_upload').dialog('close').form('reset');
                },
            }
        ],
    });
}

function server_detail_fn(row_id) {
    $('#modal_server_detail').window({
        title: '资源详情',
        modal: true,
        closed: false,
    });

    $.ajax({
        url : '/cmdb/get_server_detail/',
        type : 'POST',
        data : {'object_id': row_id},
        beforeSend : function () {
            $.messager.progress({
                text : '正在查询数据，请稍后...',
            });
        },
        success : function(data, response, status){
            $.messager.progress('close');
            if (data) {
                $("#server_detail_html").html(data)
            } else {
                $.messager.alert('警告操作', '未知错误，请联系系统管理员！', 'warning');
            }
        }
    });
}