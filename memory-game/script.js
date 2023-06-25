// Backround change buttons below the game divs
const colorsSection = document.querySelector('#colors');

colorsSection.addEventListener('click', function(e) {
	document.body.style.backgroundColor = e.target.dataset.hex;
});

const gameContainer = document.getElementById("game");

let card1 = null;
let card2 = null;
let cardsFlipped = 0;
let noClick = false;
let score = 0; 


function startScreenOn() {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("overlay").innerText = "START";
}
function startScreenOff() {
  document.getElementById("overlay").style.display = "none";
}
overlay.addEventListener("click", startScreenOff);

const CARDS = [
  "red",
  "blue",
  "green",
  "orange",
  "purple",
  "red",
  "blue",
  "green",
  "orange",
  "purple",
  "yellow",
  "pink",
  "lime",
  "teal",
  "silver",
  "yellow",
  "pink",
  "lime",
  "teal",
  "silver"
];

// here is a helper function to shuffle an array
// it returns the same array with values shuffled
// it is based on an algorithm called Fisher Yates if you want ot research more
function shuffle(array) {
  let counter = array.length;

  // While there are elements in the array
  while (counter > 0) {
    // Pick a random index
    let index = Math.floor(Math.random() * counter);

    // Decrease counter by 1
    counter--;

    // And swap the last element with it
    let temp = array[counter];
    array[counter] = array[index];
    array[index] = temp;
  }

  return array;
}

let shuffledCards = shuffle(CARDS);

// this function loops over the array of colors
// it creates a new div and gives it a class with the value of the color
// it also adds an event listener for a click for each card
function createDivsForCards(cardsArray) {
  for (let card of cardsArray) {
    // create a new div
    const newDiv = document.createElement("div");

    // give it a class attribute for the value we are looping over
    newDiv.classList.add(card);

    // call a function handleCardClick when a div is clicked on
    newDiv.addEventListener("click", handleCardClick);

    // append the div to the element with an id of game
    gameContainer.append(newDiv);
  }
}

function screenScore() {
  document.getElementById("scorecard").innerText = "Score: " + score;
  const resetButton = document.createElement("button");
  resetButton.innerText = "RESET";
  scorecard.append(resetButton);
  resetButton.addEventListener('click',()=>{ location.reload()})
}

// TODO: Implement this function!
function handleCardClick(event) {
  // you can use event.target to see which element was clicked
  console.log("you just clicked", event.target);

  if (noClick) return;
  if (event.target.classList.contains("flipped")) return;

  let currentCard = event.target;
  currentCard.style.backgroundColor = currentCard.classList[0];

  if (!card1 || !card2) {
    currentCard.classList.add("flipped");
    card1 = card1 || currentCard;
    card2 = currentCard === card1 ? null : currentCard;
  }

  if (card1 && card2) {
    noClick = true;

  if (card1.className === card2.className) {
      score++;
      screenScore();
      cardsFlipped += 2;
      card1.removeEventListener("click", handleCardClick);
      card2.removeEventListener("click", handleCardClick);
      card1 = null;
      card2 = null;
      noClick = false;
    } else {
      setTimeout(function() {
        card1.style.backgroundColor = "";
        card2.style.backgroundColor = "";
        card1.classList.remove("flipped");
        card2.classList.remove("flipped");
        card1 = null;
        card2 = null;
        noClick = false;
        noClick = false;
      }, 1000);
    }
  }
  if (cardsFlipped === CARDS.length) alert("Game Over!");

}
screenScore();
startScreenOn();


// when the DOM loads
createDivsForCards(shuffledCards);






