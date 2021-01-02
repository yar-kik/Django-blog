function showPassword() {
  let element = document.getElementById("id_password");
  let checkbox = document.getElementById("icon-eye");
  if (element.type === "password") {
    element.type = "text";
    checkbox.className = "flaticon-hide";
  } else {
    element.type = "password";
    checkbox.className = "flaticon-view";
  }
}