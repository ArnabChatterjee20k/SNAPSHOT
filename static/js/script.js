// for menu
const line_menu = document.querySelector("#line-menu")
const x_menu = document.querySelector("#x-menu")
const nav = document.querySelector("nav")
function class_toggle(firstClass, secondClass) {
    if (firstClass.classList.contains("inactive")) {
        secondClass.classList.add("inactive")
        firstClass.classList.remove("inactive")
    }
    else {
        firstClass.classList.add("inactive")
        secondClass.classList.remove("inactive")
    }
}

line_menu.addEventListener("click", function () {
    class_toggle(line_menu, x_menu)
    nav.style.display = "block"
    nav.style.transform = "scale(1)"
})
x_menu.addEventListener("click", function () {
    class_toggle(line_menu, x_menu)
    nav.style.transform = "scale(0)"
})

function like_post(post_id,elem){
    const url = `/likes/${post_id}`
    xhr = new XMLHttpRequest;
    xhr.onload = function(){
        if(this.statusText==="OK"){
            const response  = this.responseText;
            const status = JSON.parse(response).status
            Toastify({
                text: `${status} ${elem.parentNode.parentNode.querySelector(".image-title").innerText}`,
                duration: 3000,
                close: true,
                gravity: "bottom", // `top` or `bottom`
                position: "right", // `left`, `center` or `right`
                stopOnFocus: true, // Prevents dismissing of toast on hover
                style: {
                    "font-family": 'Roboto Mono',
                    color:"white",
                    background: "red",
                }
            }).showToast();
        }
    }
    xhr.open("GET",url,true);
    xhr.send()
}

// for like option
let like = document.querySelectorAll("box-icon[name='like']")
like.forEach(function (elem) {
    elem.addEventListener("click", function () {
        const state_attribute_name = "category";
        let state = elem.getAttribute(state_attribute_name); // category = 0 means disliked
        const parent_node = elem.parentNode
        const like_counter = parent_node.querySelector("#like-counter")
        const like_counter_value = parent_node.querySelector("#like-counter").textContent
        if(elem.ariaDisabled === 'false'){
            like_post(elem.id,elem)
            if (state == "0") {
                elem.setAttribute(state_attribute_name,"1")
                elem.setAttribute("color", "red")
                like_counter.textContent = Number(like_counter_value) + 1
            }
            else {
                elem.setAttribute(state_attribute_name,0)
                elem.setAttribute("color", "black")
                like_counter.textContent = Number(like_counter_value) - 1
            }
        } else{
            alert("Please login! to like the post")
        }
    })
})


// lighthouse image gallery
let images = document.querySelectorAll(".image-click");
const lighthouse = document.querySelector(".lighthouse")
const lighthouse_close_btn = document.querySelector(".lighthouse-close")
images.forEach(function (element) {
    if (!lighthouse.classList.contains("lighthouse-open")) {
        element.onclick = function () {


            lighthouse.classList.add("lighthouse-open")
            const img = document.createElement("img")
            img.src = this.src
            img.setAttribute("class", "lighthouse-img")
            lighthouse.append(img)
            lighthouse_close_btn.onclick = function () {
                lighthouse.removeChild(img)
                lighthouse.classList.remove("lighthouse-open")
            }

        }
    }
})

