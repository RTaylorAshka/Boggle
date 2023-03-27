const guessForm = document.querySelector("#guess");
const htmlTimer = document.querySelector("h1.timer");
const refreshButton = document.querySelector("button.ref");
const highscore = document.querySelector("#h-score");
const score = document.querySelector("#score");
const erroDiv = document.querySelector("#error-div");
let timeLimit = 60;
let isDisabled = false;

function timer() {
  setTimeout(() => {
    timeLimit--;
    htmlTimer.innerText = `Time: ${timeLimit}`;
    if (timeLimit == 0) {
      disableInput();
      //send the data to the backend to save the score and potentially the backend will update the highscore
      // if the score is higher than the highscore
    }
  }, 1000);
}

function disableInput() {
  guessForm.disabled = true;
  guessForm.innerHTML = "<h1>Time's Up!</h1>";
}

async function update_json(e) {
  e.preventDefault();
  const guess = document.querySelector("#text-guess").value;
  if (!guess) {
    return undefined;
  }
  const guessResult = await axios.post("/guess", { guess });
  handleResult(guessResult.data);
}

function displayErrorDiv(value) {
  erroDiv.innerText = value;
  setTimeout(() => {
    erroDiv.innerText = "";
  }, 3000);
}

function handleResult(result) {
  if (result.outcome === "error") {
    displayErrorDiv(result.reason);
  } else {
    const currentScore = +score.innerText + 1;
    score.innerText = currentScore;
  }
}

function getHighScore() {
  //request to backend
}

refreshButton.addEventListener("click", () => {
  sessionStorage.clear();
});

guessForm.addEventListener("submit", update_json);

timer();
getHighScore();
