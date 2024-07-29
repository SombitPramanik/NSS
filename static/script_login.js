
const wrapper = document.querySelector('.wrapper')
const menu_login_button = document.querySelector('.login')

const login_form = document.querySelector('.form-box.lgin');
const otp_form = document.querySelector('.form-box.otp');

const login_ico_close = document.querySelector('.close_ico');
const login_button = document.querySelector('.btn.lgin');
const otp_submit_button = document.querySelector('.btn.otp');
const back_button = document.querySelector('.btn.bck');


wrapper.style.display = 'none';   //default values

menu_login_button.addEventListener('click',function (){ 
    login_form.style.transition = 'transform .18s ease';
    login_form.style.transform = 'translateX(0)'     //login button on the navbar
    wrapper.style.display = 'block';
});


function show_otp_form(){
    
    wrapper.style.height = '350px';
    login_form.style.display = 'none';
    otp_form.style.display = 'block';
    otp_form.style.transition = 'transform .18s ease';
    otp_form.style.transform = 'translateX(0)'
}

function show_login_form() {
    wrapper.style.height = '400px';
    otp_form.style.display = 'none';
    login_form.style.display = 'block';
    login_form.style.transition = 'transform .18s ease';
    login_form.style.transform = 'translateX(0)'
}


login_button.addEventListener('click', function (event){

    event.preventDefault();

    const user_email_input = login_form.querySelector('input[type = "email"]');
    const user_email = user_email_input.value.trim();

    const user_password_input = login_form.querySelector('input[type = "password"]');
    const user_password = user_password_input.value.trim();

    //do not uncomment it !!For testting purpose only==========================================<<<<<
    // alert('email = '+ user_email + 'password = ' + user_password);    
    //=========================================================================================<<<<<

    //user verification code here===============================================<<<<<
    if (user_email === 'am@gmail.com' && user_password === '123') {          //dummy testing values , change accordingly
        // alert('Please fill in all the fields.');
        show_otp_form();
    }
    else{
        alert('invalid');
    }

    
});


otp_submit_button.addEventListener('click', function (event){

    event.preventDefault();

    const user_otp_input = otp_form.querySelector('input[type = "otp"]');
    const user_otp = user_otp_input.value.trim();

    if (otp === '') {
        alert('Please enter the correct OTP.');
        return;
    }

    alert('OTP submitted successfully');
});


back_button.addEventListener('click', function (event){     //back button in the otp form
    event.preventDefault();
    show_login_form();
});


login_ico_close.addEventListener('click',function (){       // close icon of the wrapper
    wrapper.style.display = 'none';
});