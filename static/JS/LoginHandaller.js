const wrapper = document.querySelector(".wrapper");
const menu_login_button = document.querySelector(".login");

const login_form = document.querySelector(".form-box.lgin");
const otp_form = document.querySelector(".form-box.otp");

const login_ico_close = document.querySelector(".close_ico");
const login_button = document.querySelector(".btn.lgin");
const otp_submit_button = document.querySelector(".btn.otp");
const back_button = document.querySelector(".btn.bck");

wrapper.style.display = "none"; //default values

menu_login_button.addEventListener("click", function () {
  login_form.style.transition = "transform .18s ease";
  login_form.style.transform = "translateX(0)"; //login button on the navbar
  wrapper.style.display = "block";
});

function show_otp_form() {
  wrapper.style.height = "350px";
  login_form.style.display = "none";
  otp_form.style.display = "block";
  otp_form.style.transition = "transform .18s ease";
  otp_form.style.transform = "translateX(0)";
}

function show_login_form() {
  wrapper.style.height = "400px";
  otp_form.style.display = "none";
  login_form.style.display = "block";
  login_form.style.transition = "transform .18s ease";
  login_form.style.transform = "translateX(0)";
}
function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9]+@cemk\.ac\.in$/;
  return emailRegex.test(email);
}

function validatePassword(password) {
  const passwordRegex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{9,}$/;
  return passwordRegex.test(password);
}

login_button.addEventListener("click", function (event) {
  event.preventDefault();

  const user_email_input = login_form.querySelector('input[type = "email"]');
  const user_email = user_email_input.value.trim();

  const user_password_input = login_form.querySelector(
    'input[type = "password"]'
  );
  const user_password = user_password_input.value.trim();


  if (validateEmail(user_email) && validatePassword(user_password)) {
    fetch("/SendOTP", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ Email: user_email, Password: user_password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.Message === true) {
          show_otp_form();
        } else {
          alert(data.Message);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    alert("Unsupported Email or Password");
  }
});

otp_submit_button.addEventListener("click", function (event) {
  event.preventDefault();

  const user_otp_input = otp_form.querySelector('input[type = "otp"]');
  const user_otp = user_otp_input.value.trim();

  if (user_otp === "") {
    alert("OTP Should not be Null");
    return;
  }
  fetch("/VerifyOTP", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ OTP: user_otp }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.Message === true) {
        alert("OTP Verified Redirect to Dashboard in 2 Seconds");
        setTimeout(() => {
          window.location.href = "/Dashboard";
        }, 2000); // 2000 milliseconds = 2 seconds
      } else {
        alert("Invalid OTP");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

back_button.addEventListener("click", function (event) {
  //back button in the otp form
  event.preventDefault();
  show_login_form();
});

login_ico_close.addEventListener("click", function () {
  // close icon of the wrapper
  wrapper.style.display = "none";
});
