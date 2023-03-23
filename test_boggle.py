from unittest import TestCase
from app import game_board, handle_guess, refresh_game, GameSession
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_game_board(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<form action="/guess" method="post" class="guess">', html)
    
    def test_handle_guess(self):
        with app.test_client() as client:
            res = client.post('/guess', data = {'guess' : 'a'})

            self.assertEqual(res.status_code, 302)

    def test_refresh_game(self):
        with app.test_client() as client:
            res = client.get('/refresh')
            self.assertEqual(res.status_code, 302)

    def test_get_board(self):
        game = GameSession()
        board = game.get_board({})
        self.assertEqual(len(board),5)
        self.assertEqual(len(board[0]),5)

    def test_get_score(self):
        with app.test_client() as client:
            client.get('/')
            game = GameSession()
            score = game.get_score(session)
            self.assertEqual(score, 0)
    
    def test_prev_answers(self):
        with app.test_client() as client:
            client.get('/')
            
            game = GameSession()
           
            prev_ans = game.get_prev_ans({})
            
            print(prev_ans)
            
            self.assertEqual(prev_ans, [])
            
            

            

    

    
    

