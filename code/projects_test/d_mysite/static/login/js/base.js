var btn_register = document.getElementById('register');
var btn_login = document.getElementById('login');
var btn_logout = document.getElementById('logout');

if(btn_register){
    btn_register.onclick = register_func;
}else if(btn_login){
    btn_login.onclick = login_func;
}else if(btn_logout){
    btn_logout.onclick = logout_func;
};

function get_token(){
    var datas = document.cookie.split(';');
    for(var key in datas){
        var item = datas[key].split('=');
        if(item[0]=='csrftoken'){
            console.log(item);
            return item[1];
        }
    }
};

function login_func() {
    console.log('login_func');
    var name = document.getElementsByName('name')[0].value;
    var password = document.getElementsByName('password')[0].value;
    var data = new FormData();
    data.append('name', name);
    data.append('password', password);
    data.append('csrfmiddlewaretoken', get_token());
    xhr = new XMLHttpRequest();
    xhr.open('post',url='/login/', async=true);
    // xhr.setRequestHeader("X-CSRFToken", get_token());
    xhr.onload  = function(e){
        var response = JSON.parse(e.target.response);
        console.log(response.msg);
        location.href = '/index/';
    };
    xhr.onerror = function(e){
        var response = JSON.parse(e.target.response);
        console.log(response.msg);
    };
    xhr.send(data);
};

function logout_func() {
    console.log('logout_func');
    xhr = new XMLHttpRequest();
    xhr.open('get',url='/logout/', async=true);
    xhr.onload  = function(e){
        var response = JSON.parse(e.target.response);
        console.log(response);
        location.href = '/login/';
    };
    xhr.onerror = function(e){
        var response = JSON.parse(e.target.response);
        console.log(response.msg);
    };
    xhr.send();
};
function register_func() {
    console.log('register_func');
};


