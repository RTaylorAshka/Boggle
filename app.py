from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohnooo'


game = Boggle()

def get_board(sess):
    if not (sess.get('board', False)):
        sess['board'] = game.make_board()
        return sess['board']
    
    else:
        return sess['board']
    
def get_score(sess):
    if not (sess.get('score', False)):
        score = 0
        return score
    
    else:
        return int(sess['score'])
    
def check_prev_answers(sess,ans=False):

    prev_ans = get_prev_ans(sess)
    if ans and game.check_valid_word(get_board(sess), ans) == 'ok':
        if ans in prev_ans:
            print(ans)
            print(prev_ans)
            print('here!')
            return False
        else:
            
            prev_ans.append(ans)
            sess['prev_ans'] = prev_ans

            return True
    
    return False

def get_prev_ans(sess):

    if not (sess.get('prev_ans', False)):
        sess['prev_ans'] = []
        prev_ans = sess['prev_ans']
        return prev_ans
    
    else:
        prev_ans = sess['prev_ans']
        return prev_ans 
    



@app.route('/')
def game_board():
    # print(session['prev_ans'])
    return(render_template('boggle.html', board = get_board(session), score = get_score(session), prev_ans = get_prev_ans(session)))


@app.route('/guess', methods = ['POST'])
def handle_guess():

    guess = request.form.get('guess', False)
    check_res = game.check_valid_word(get_board(session), guess)
    if check_res != 'ok':
        flash(f'{check_res}')

        return redirect('/')
    
    elif check_prev_answers(session, guess) == False:
        flash(f'{guess} has already been guessed!')
        return redirect('/') 

    elif check_res == 'ok':
        session['score'] = get_score(session)  + 1
        

        return redirect('/') 
    
    return redirect('/') 


@app.route('/refresh')
def refresh_game():
    session.clear()
    return redirect('/')
    