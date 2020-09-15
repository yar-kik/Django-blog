function showPassword() {
  var element = document.getElementById("id_password");
  if (element.type === "password") {
    element.type = "text";
  } else {
    element.type = "password";
  }
}