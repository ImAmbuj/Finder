document.getElementById("dismiss-popup-btn").addEventListener("click",function(){
    document.getElementsByClassName("popup")[0].classList.remove("active");
});

document.getElementById("edit-profile").addEventListener("click",function(){
    document.getElementsByClassName("popup")[0].classList.add("active");
});


document.getElementById("save-btn").addEventListener("click",function(){
    document.getElementsByClassName("popup")[0].classList.remove("active");
});



