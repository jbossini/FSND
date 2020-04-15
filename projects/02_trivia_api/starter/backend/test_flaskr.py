import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user=os.environ.get("DB_USER")
        self.database_password = os.environ.get("DB_PASSWORD")
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user,self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question ={
            'question' : 'What is the name of Son Goku\'s second son?',
            'answer' : 'Son Gotten',
            'category' : 5,
            'difficulty' : 3
        }
        self.bad_question = {
            'question' : 'What is the best vampire slayer of all time?',
            'answer' : 'Buffy, of course',
            'category' : 1000,
            'difficulty' : 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables    
            self.db.create_all()
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    
    #Test that returns success if it found questions for page 1    
    def test_get_questions_paginated_success(self):
        res=self.client().get('/questions?page=1')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
    
    #Test that returns error code 404 if we can't find the page of the questions searched 
    def test_get_questions_paginated_error_404(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual((data['message']),'Resource not found')
    
    #This test will be succeed if the new question is created and we receive the new id
    def test_create_question_OK(self):
        res = self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success',True])
        self.assertTrue(data['id_question',id])
    
    #This test will be succeed if the new question is created and we receive the new id
    def test_create_question_OK(self):
        res = self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['id_question'],id)

     #This test will be succeed if the new question is created and we receive the new id
    def test_create_question_bad_category(self):
        res = self.client().post('/questions',json=self.bad_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],'unprocessable')
    
    #Success if we can delete question with id = last
    def test_delete_question_ok(self):
        res=self.client().delete('/questions/5')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],5)
    
    #The test will be succeed if the code raises an error 422 while trying to delete a non existent question
    def test_delete_question_error_404(self):
        res=self.client().delete('/questions/1000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable') 

    def test_search_question_results_OK(self):
        res=self.client().post('/questions', json={'searchTerm': 'title'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    def test_search_question_results_not_found(self):
        res=self.client().post('/questions', json={'searchTerm': 'patata'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['questions']),0)
     
    def test_search_question_by_category_OK(self):
        res=self.client().get('/categories/1/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    def test_search_question_by_wrong_category(self):
        res=self.client().get('/categories/10/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual((data['message']),'Resource not found')
    
    def test_quizzes_get_question(self):
        res=self.client().post('/quizzes', json={
            "previous_questions": [9],
            "quiz_category": {"type":"Entertainment", "id": "5" }
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
    
    def test_quizzes_get_question_category_not_found_404(self):
        res=self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"type":"None", "id": "100" }
        })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual((data['message']),'Resource not found')
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()