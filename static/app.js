guessForm = document.querySelector('form.guess')
htmlTimer = document.querySelector('h1.timer')
refreshButton = document.querySelector('button.ref')
highscoreHTML = document.querySelector('p.hs')
gamesplayedHTML = document.querySelector('p.gp')


const timeLimit = 60;
let isDisabled = false

if (sessionStorage.getItem('timer') == null) {
    sessionStorage.setItem('timer', timeLimit)
}


function timer() {
    setTimeout(() => {

        let time = sessionStorage.getItem('timer')

        htmlTimer.innerText = `Time: ${time}`;

        // console.log(time)
        if (time > 0) {
            sessionStorage.setItem('timer', time - 1)
            timer()
        }

        else if (time == 0) {
            disableInput()
        }

    }, 1000)
}

function disableInput() {
    guessForm.disabled = true;
    guessForm.innerHTML = "<h1>Time's Up!</h1>"
}



refreshButton.addEventListener('click', () => {

    sessionStorage.clear()
})

async function update_json() {
    response = await axios.get('/json')
    sessionStorage.setItem('games', response.data.games)
    sessionStorage.setItem('highscore', response.data.highscore)
    update_html()
    return response
}

guessForm.addEventListener('submit', update_json())


function update_html() {

    gamesplayedHTML.innerText = `Games Played: ${sessionStorage.getItem('games')}`
    highscoreHTML.innerText = `Highscore: ${sessionStorage.getItem('highscore')}`

}


update_json()
timer()
