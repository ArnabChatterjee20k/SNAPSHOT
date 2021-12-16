console.log("profile")
let btn_log_in = document.getElementById("btn_send_req");
let loader = document.querySelector(".loader")
let alert = document.querySelector(".alert")

btn_log_in.onclick = function(){
    let obj = {
        name : 'arnab',
        roll : "8"
    }

    let xhr = new XMLHttpRequest();
    xhr.onload = function(){
        alert.innerText = xhr.responseText;
    }
    xhr.open("POST","/login",true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(obj))
    
    loader.classList.add("click__load__invisible")
    btn.value = "Loading..."

}



