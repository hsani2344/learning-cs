function increaseValue () {
  var target = document.querySelector("div.display");
  var x = Number(target.getAttribute("value")) + 1;
  if (x <= 3) {
    target.setAttribute("value", String(x));
    target.innerHTML = x;
    console.log(x);
  }
}
