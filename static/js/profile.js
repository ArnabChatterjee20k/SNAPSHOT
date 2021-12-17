console.log("profile")
let btn_log_in = document.getElementById("btn_send_req");
const btn_value = btn_log_in.value;

function alert_msg(msg, category) {
    // utility function for displaying message
    let alert = document.querySelector(".alert")
    alert.style.display = "block"
    alert.innerText = msg
    alert.classList.add(category)
}

function register() {
    btn_log_in.onclick = function () {
        const warning = "warning"
        const success = "success"

        let loader = document.querySelector(".loader")

        let name = document.getElementById("Name").value.trim()
        let password = document.getElementById("Password").value.trim()
        if (name != "" & password != "") {
            let obj = {
                name: name,
                password: password
            }

            let xhr = new XMLHttpRequest();
            xhr.onloadstart = function () {
                btn_log_in.value = "Loading..."
                loader.classList.add("click__load__invisible")
            }

            xhr.onload = function () {
                btn_log_in.value = btn_value;
                loader.classList.remove("click__load__invisible")
                if (xhr.status == 200) {
                    let message = JSON.parse(xhr.responseText)
                    let response = message["response"]
                    let category = message["category"]
                    alert_msg(response, category)
                }
                else {
                    alert_msg("Try again", warning)
                }
            }

            xhr.open("POST", "/register", true)
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(obj))
        } else {
            alert_msg("Plz complete the details", warning)
        }

    }
}


function login(){

}

login()