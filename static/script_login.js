const wrapper = document.querySelector('.wrapper')
// const LoginLink = document.querySelector('.login-link')
const OTPLink = document.querySelector('.otp-link')
const login_button = document.querySelector('.btn.lgin')
const back_button = document.querySelector('.btn.bck')
const menu_login_button = document.querySelector('.login')
const login_ico_close = document.querySelector('.close_ico')

menu_login_button.addEventListener('click',()=>{
    wrapper.classList.add('active_popup');
});

login_ico_close.addEventListener('click',()=>{
    wrapper.classList.remove('active_popup');
    console.log('working');
});

login_button.addEventListener('click',()=>{
    wrapper.classList.add('active');
    console.log('login link');
});

back_button.addEventListener('click',() => {
    wrapper.classList.remove('active');
});