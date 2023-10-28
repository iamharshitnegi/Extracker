const usernameField=document.querySelector('#usernameField');
const emailField = document.querySelector("#email-field");
const feedBackArea= document.querySelector('.invalid_feedback');
const emailfeedBackArea = document.querySelector(".emailfeedBackArea");
const usernameSuccessOutput= document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField=document.querySelector("#password-field");
const submitBtn = document.querySelector('.submit-btn');

const handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent=="SHOW"){
        showPasswordToggle.textContent="HIDE";
        passwordField.setAttribute("type","text");
    }
    else {
        showPasswordToggle.textContent= "SHOW";
        passwordField.setAttribute("type","password");
    }
};


showPasswordToggle.addEventListener('click', handleToggleInput);

emailField.addEventListener("keyup", (e)=>{

    const emailVal=e.target.value;

    emailField.classList.remove('is-invalid');
    emailfeedBackArea.style.display = "none";

    if(emailVal.length>0){
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        }).then(res=>res.json()).then(data=>{
            console.log("data",data);
            if(data.email_error){
                submitBtn.disabled=true;
                emailField.classList.add('is-invalid');
                emailfeedBackArea.style.display = "block";
                emailfeedBackArea.innerHTML=`<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});

usernameField.addEventListener("keyup", (e)=>{

    const usernameVal=e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display = "none";

    if(usernameVal.length>0){
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then(res=>res.json()).then(data=>{
            console.log("data",data);
            usernameSuccessOutput.style.display = "none";
            if(data.username_error){
                submitBtn.disabled=true;
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled");
            }
        });
    }
});

