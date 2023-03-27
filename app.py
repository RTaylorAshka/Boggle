from boggle import Boggle
import json
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohnooo'




class GameSession():

    def __init__(self):
        self.game = Boggle()
        

    def get_board(self, sess):
        if not (sess.get('board', False)):
            sess['board'] = self.game.make_board()
            return sess['board']
    
        else:
            return sess['board']
    
    def get_score(self, sess):
        if not (sess.get('score', False)):
            score = 0
            return score
    
        else:
            return int(sess['score'])
        
    
    def check_prev_answers(self, sess, ans=False):

        
        prev_ans = self.get_prev_ans(sess)
        if ans and self.game.check_valid_word(self.get_board(sess), ans) == 'ok':
            if ans in prev_ans:
               
                return False
            else:
                
                
                prev_ans.append(ans)
                sess['prev_ans'] = prev_ans

                return True
    
        return False

    def get_prev_ans(self, sess):

        if not (sess.get('prev_ans', False)):
            sess['prev_ans'] = []
            prev_ans = sess['prev_ans']
            return prev_ans
    
        else:
            prev_ans = sess['prev_ans']
            return prev_ans 




current_game = GameSession()   



@app.route('/')
def game_board():
    # print(session['prev_ans'])
    return(render_template('boggle.html', board = current_game.get_board(session), 
            score = current_game.get_score(session), prev_ans = current_game.get_prev_ans(session)))


@app.route('/guess', methods = ['POST'])
def handle_guess():
    guess = request.json['guess']
    check_res = current_game.game.check_valid_word(current_game.get_board(session), guess)
    if check_res != 'ok':
        return {"outcome":"error","reason":"word not valid"}
    
    elif current_game.check_prev_answers(session, guess) == False:
         return {"outcome":"error","reason":"word already guessed"}

    elif check_res == 'ok':
        session['score'] = current_game.get_score(session)  + 1
    
    return {"outcome":"success"}


@app.route('/refresh')
def refresh_game():
    

    give_json()

    session['games'] = session['games'] + 1
    session['score'] = None
    session['board'] = None
    session['prev_ans'] = None
    return redirect('/')

@app.route('/json')
def give_json():
        
        # import pdb
        # pdb.set_trace()


        score = current_game.get_score(session)
        if not (session.get('highscore', False)):
            highscore = score
        else:
            highscore = int(session['highscore'])
            if highscore < score:
                highscore = score
        
        if not (session.get('games', False)):
            games = 1
        else:
            games = int(session['games'])


        session['highscore'] = highscore
        session['games'] = games
        response = jsonify({'highscore' : highscore, 'games' : games})

        return response

    