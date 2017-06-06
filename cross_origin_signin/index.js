var gd_accountname = document.getElementById('gd_accountname');
var gd_username = document.getElementById('gd_username');
var gd_password = document.getElementById('gd_password');
var gd_login = document.getElementById('gd_login');
window.msg;

	gd_password.onkeydown = function(event) {
    if (event.keyCode == 13) {
      var data = {};
      data.account_name = gd_accountname.value;
      data.user_name = gd_username.value;
      data.password = gd_password.value;
      if (data.account_name && data.password) {
        gd_login.onclick();
      } else {
        window.msg = '账户名、用户名或密码不能为空!';
      }
    }
  };


  gd_login.onclick = function() {
    var data = {};
    data.account_name = gd_accountname.value;
    data.user_name = gd_username.value;
    data.password = gd_password.value;
    // 请将origin值改写为真实的域名或地址
    // 注意：请事先确保该地址已通知GeneDock进行认证，如有疑问请联系我们
    data.origin = 'http://192.168.0.170:1234';
    if (data.account_name && data.user_name && data.password) {
      $.ajax({
          url: 'https://www.genedock.com/external_signin/',
          xhrFields: {withCredentials: true},
          data: JSON.stringify(data),
          type: 'post',
          contentType: 'application/json;charset=utf-8',
          success: function() {
            location.href = 'https://www.genedock.com/external_signin_gateway/';
          },
          error: function(res) {
            //登录报错信息可在此处拿到
            window.msg = eval("(" + res.responseText + ")");
          }
        });

    } else {
      window.msg = '用户名或密码不能为空！';
    }
  };
