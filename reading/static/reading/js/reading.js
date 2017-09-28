$(function(){
    //初始化input状态样式图标
    var icon = {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    };
    //初始化验证规则
    $("form").bootstrapValidator({
        feedbackIcons: icon,   //加载图标
        /* 生效规则
         * enabled:字段值发生变化就触发验证
         * disabled/submitted:点击提交时触发验证
         */
        live: 'disabled',
        //表单域配置
        fields: {
            username: {//username为input标签name值
                validators: {
                    notEmpty: {message: '请输入用户名'},    //非空提示
                    stringLength: {    //长度限制
                          min: 4,
                          max: 20,
                          message: '用户名长度必须在4到20之间'
                    },
                    regexp: {//匹配规则
                          regexp: /^[a-zA-Z0-9_\\u4e00-\\u9fa5]+$/,  //正则表达式
                          message:'用户名仅支持汉字、字母、数字、下划线的组合'
                    }
                }
            },
            password1: {
                validators: {
                   notEmpty: {message: '请输入密码'},
                   stringLength: {    //长度限制
                          min: 6,
                          max: 60,
                          message: '用户名长度必须在6到60之间'
                    },
                   different: {  //比较
                        field: 'username', //需要进行比较的input name值
                        message: '密码不能与用户名相同'
                   }
                }
            },
            password: {
                validators: {
                   notEmpty: {message: '请输入密码'},
                   stringLength: {    //长度限制
                          min: 6,
                          max: 60,
                          message: '用户名长度必须在6到60之间'
                    },
                   different: {  //比较
                        field: 'username', //需要进行比较的input name值
                        message: '密码不能与用户名相同'
                   }
                }
            },
            password2: {
                validators: {
                    notEmpty: {message: '请再次输入密码'},
                    identical: {  //比较是否相同
                           field: 'password1',  //需要进行比较的input name值
                           message: '两次密码不一致'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {message: '请输入邮箱'},
                    emailAddress: {message: '请输入正确的邮件地址'}
                }
            },
            name: {
                validators: {
                    notEmpty: {message: '请输入书名'},
                    stringLength: {    //长度限制
                          min: 1,
                          max: 150,
                          message: '书名长度必须在1到150之间'
                    }
                }
            },
            bookname: {
                validators: {
                    notEmpty: {message: '请输入书名'},
                    stringLength: {    //长度限制
                          min: 1,
                          max: 150,
                          message: '书名长度必须在1到150之间'
                    }
                }
            },
            author: {
                validators: {
                    notEmpty: {message: '请输入作者'},
                    stringLength: {    //长度限制
                          min: 1,
                          max: 150,
                          message: '作者长度必须在1到150之间'
                    }
                }
            },
            imgurl: {
                validators: {
                    stringLength: {    //长度限制
                          min: 10,
                          max: 2048,
                          message: '图片链接长度必须在10到2048之间'
                    }
                }
            },
            content: {
                validators: {
                    notEmpty: {message: '请输入内容'}
                }
            }
        }
    })
});
