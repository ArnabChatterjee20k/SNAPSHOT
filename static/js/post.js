// for menu
const line_menu = document.querySelector("#line-menu")
const x_menu = document.querySelector("#x-menu")
const nav = document.querySelector("nav")
const upload = document.getElementById("upload")
const preview = document.getElementById("image_preview")
const preview_text = document.getElementById("preview_text")

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
    nav.style.display="flex"
})
x_menu.addEventListener("click",function(){
    class_toggle(line_menu,x_menu)
    nav.style.display = "none"
})


upload.addEventListener("click",function(){
    let file = document.getElementById("file")
    if(file){
        preview_text.style.display = "none"
        preview.style.display = "block"
        preview.classList.add("preview_onload")
        let new_img = URL.createObjectURL(file.files[0])
        preview.src = new_img

        const xhr = new XMLHttpRequest;
        const form =  new FormData()
        form.append("name","arnab")
        form.append("file",file.files[0])

        xhr.onload = function(){console.log(this.responseText)}
        xhr.open("POST","/submit",true)
        xhr.send(form)
    }
})