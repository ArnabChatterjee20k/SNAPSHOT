let btn_log_in = document.getElementById("btn_log_in");
const  btn_log_in__value= btn_log_in.value;

let btn_reg = document.getElementById("btn_reg");
const btn_reg__value = btn_reg.value;

function alert_msg(msg, category) {
    // utility function for displaying message
    let alert = document.querySelector(".alert")
    alert.style.display = "block"
    alert.innerText = msg
    alert.id = category
}

function btn_action(endpoint,selected_btn,btn_value) {
    selected_btn.onclick = function () {
        const warning = "warning"
        const success = "success"

        let loader = document.querySelector(".loader")

        let name = document.getElementById("Name").value.trim()
        let password = document.getElementById("Password").value.trim()
        if (name != "" && password != "") {
            let obj = {
                name: name,
                password: password
            }

            let xhr = new XMLHttpRequest();
            xhr.onloadstart = function () {
                selected_btn.value = "Loading..."
                loader.classList.add("click__load__invisible")
            }

            xhr.onload = function () {
                selected_btn.value = btn_value;
                loader.classList.remove("click__load__invisible")
                if (xhr.status == 200) {
                    let message = JSON.parse(xhr.responseText)
                    
                    let response = message["response"]
                    let category = message["category"]
                    let redirect_url = message["redirect_url"]
                    alert_msg(response, category)
                    
                    if(redirect_url){
                        window.location = redirect_url
                    } else{
                        console.log(redirect_url)
                    }
                }
                else {
                    alert_msg("Try again", warning)
                }
            }

            xhr.open("POST", `/${endpoint}`, true)
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(obj))
        } else {
            alert_msg("Plz complete the details.", warning)
        }

    }
}


function change_field() {
    //links--activators
    const log__link__activate = document.getElementById("reg__link")
    const reg__link__activate = document.getElementById("log__link")
    // containers--form
    const reg__cont = document.getElementById("reg__cont")
    const log__cont = document.getElementById("log__cont")

    function toggle_class(cont1,cont2,classname){
        cont1.classList.toggle(classname)
        cont2.classList.toggle(classname)
    }

    const classname = "inactive"

    log__link__activate.onclick = function(){
        toggle_class(log__cont,reg__cont,classname)
    }
    reg__link__activate.onclick = function() {
        toggle_class(log__cont,reg__cont,classname)
    }

}



btn_action("log",btn_log_in,btn_log_in__value)

btn_action("register",btn_reg,btn_reg__value)
change_field()