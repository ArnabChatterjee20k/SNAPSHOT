// for menu
const line_menu = document.querySelector("#line-menu")
const x_menu = document.querySelector("#x-menu")
const nav = document.querySelector("nav")
function class_toggle(firstClass,secondClass){
    if (firstClass.classList.contains("inactive")){
        secondClass.classList.add("inactive")
        firstClass.classList.remove("inactive")
    }
    else{
        firstClass.classList.add("inactive")
        secondClass.classList.remove("inactive")
    }
}

line_menu.addEventListener("click",function(){
    class_toggle(line_menu,x_menu)
    nav.style.display="block"
    nav.style.transform = "scale(1)"
})
x_menu.addEventListener("click",function(){
    class_toggle(line_menu,x_menu)
    nav.style.transform = "scale(0)"
})


// for like option
let like = document.querySelectorAll("box-icon[name='like']")
like.forEach(function(elem){
    elem.addEventListener("click",function(){
        let state = elem.getAttribute("color");
        // console.log(state)
        // console.log(elem.id)
        if(state=="red"){
            elem.setAttribute("color","black")
        }
        else{
            elem.setAttribute("color","red")
        }
    })
})
