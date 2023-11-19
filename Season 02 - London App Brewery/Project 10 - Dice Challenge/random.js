function getRandom(odds) {
  var number = Math.floor(Math.random() * odds) + 1;
  return number;
}

function showDice() {
  var players = document.querySelectorAll("img.dice");
  var playerCount = players.length;
  var scores = [];
  for (var i = 0; i < 2; i++) {
    document.querySelectorAll("h2.player")[i].innerHTML = "Player " + (i + 1);
  }
  for (var i = 0; i < playerCount; i++) {
    scores[i] = getRandom(6);
    players[i].setAttribute("src", "./images/dice" + String(scores[i]) + ".png");
  }
  if (scores[0] > scores[1]) {
    var result = "Player 1 win!"
    document.querySelector("h1").innerHTML = result;
    console.log(result);
  }
  else if (scores[0] < scores[1]) {
    var result = "Player 2 win!"
    document.querySelector("h1").innerHTML = result;
    console.log(result);
  }
  else {
    var result = "Draw!"
    document.querySelector("h1").innerHTML = result;
    console.log(result);
  }
}
