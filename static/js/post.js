// for menu
const line_menu = document.querySelector("#line-menu")
const x_menu = document.querySelector("#x-menu")
const nav = document.querySelector("nav")
const upload = document.getElementById("upload")
const preview = document.getElementById("image_preview")
const preview_text = document.getElementById("preview_text")
const img_btn = document.getElementById("upload-btn")

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


img_btn.addEventListener("click",function(){
    let file = document.getElementById("file")
    file.click()
        file.addEventListener("change",function(){
            if(file){
                // if file element exists then get the value of actual file from the array of files. Then if actual file is not none (means the array is not none and a file is present at 0 index of file) then execute this. At when we are setting the image in the frame before that there is no files array in the file element. So if any file is present in the array then do the action
                let actual_file = file.files[0]
                if(actual_file){
                    const full_filename = actual_file.name
                    const spliced_filename = full_filename.split(".")
                    let i;
                    let file_extension;
                    for(i in spliced_filename){
                        file_extension = spliced_filename[i];
                    }
                    const actual_filename = full_filename.slice(0,5) + "..." + file_extension;
                    preview_text.innerText = actual_filename
                    preview.style.display = "block"
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
            }
            
        })
        
    
})