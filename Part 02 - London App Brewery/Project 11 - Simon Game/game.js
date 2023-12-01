var gamePattern = [];
var userClickedPattern = [];
var userColorChoice = null;
var levelCount = 0;
var gameStarted = false;
var gameOver = false;
var choiceCount = 0;
let buttonColors = ["red", "blue", "green", "yellow"];
let FADE_MS = 150;


function playSound(name) {
    var audio = new Audio("sounds/" + name + ".mp3");
    audio.play();
}


function animatePress(name) {
  playSound(name);
  $('#' + name).css("box-shadow", "1px 1px 2px black, 0 0 25px white, 0 0 5px white")
  setTimeout(function () {
    $('#' + name).css("box-shadow", "")
  }, 100);
}


function nextSequence() {
  levelCount++
  $("h1").text("Level " + levelCount);
  var randomNumber = Math.floor(Math.random() * 4);
  var randomChosenColor = buttonColors[randomNumber];
  gamePattern.push(randomChosenColor);
  $("#" + randomChosenColor).fadeOut(FADE_MS, playSound(randomChosenColor)).fadeIn(FADE_MS);
}


function btnClicked(name) {
    animatePress(name);
}


function verifyPattern () {
  if ((choiceCount + 1 === levelCount) && (userClickedPattern[choiceCount] === gamePattern[choiceCount])) {
    setTimeout(function () {
      choiceCount = 0;
      userClickedPattern = [];
      nextSequence();
    }, 500)
  }
  else if (userClickedPattern[choiceCount] !== gamePattern[choiceCount]) {
    $("h1").text("Game Over, Press Any Key to Restart");
    gameStarted = false;
    gameOver = true;
    $("body").addClass("game-over");
    setTimeout(function () {
      $("body").removeClass("game-over");
    }, 300)
  }
  choiceCount++
}


function main() {
  $(".btn").on("click", function () {
    userColorChoice = $(this).attr("id");
    btnClicked(userColorChoice);
    if (gameStarted === true) {
      userClickedPattern.push(userColorChoice);
      verifyPattern();
    }
  })
  $("body").on("keypress", function (event) {
    if (gameStarted === false && gameOver === false && event.key === 'a') {
      nextSequence();
      gameStarted = true;
    }
  })
  $("body").on("keypress", function (event) {
    if (gameOver === true) {
      gamePattern = [];
      userClickedPattern = [];
      userColorChoice = null;
      levelCount = 0;
      gameStarted = true;
      gameOver = false;
      choiceCount = 0;
      nextSequence();
    }
  })
}


main()
