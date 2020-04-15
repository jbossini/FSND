import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category,database_path

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  
  '''
  DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  DONE 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories={category.id:category.type for category in Category.query.order_by(Category.id).all()};
    return jsonify({'categories':categories})

  def pagination(questions,page):
    start = (int(page)-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return questions[start:end]
  '''
  DONE 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page',1,type=int)
    questions = [question.format() for question in Question.query.order_by(Question.id).all()]
    paginated_questions=pagination(questions,page)
    categories={category.id:category.type for category in Category.query.order_by(Category.id).all()}
    if (len(paginated_questions)==0):
      abort(404)
    else:
      return jsonify({'success':True, 'questions':paginated_questions,'total_questions':len(questions),'current_category':'ALL','categories':categories})
      
  '''
  DONE 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id_question>', methods=['DELETE'])
  def delete_question(id_question):
  
    question = Question.query.filter(Question.id==id_question).one_or_none()
    if question==None:
      abort(422)
    else:
      question.delete()
      return jsonify({'success':True,'deleted':id_question})

  '''
  DONE 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def create_question():
    body=request.get_json()
    search_term=body.get('searchTerm')
    if search_term!=None:
      questions=[
        question.format() for question in
        Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
      ]
      page=request.args.get('page',1,type=int)
      paginated_questions=pagination(questions,page)
      return jsonify({
        'success':True,
        'questions': paginated_questions,
        'total_questions' : len(questions)
      })
    else:
      question_text=body.get('question')
      answer=body.get('answer')
      difficulty=body.get('difficulty')
      category=Category.query.filter(Category.id==body.get('category')).one_or_none()
      if category==None:
        abort(422)
      question=Question(question = question_text, answer = answer, category = category.id, difficulty = difficulty)
      question.insert()
      return jsonify({
        'success': True,
        'id_question' :question.id
        })
  '''
  DONE 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  DONE 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id_category>/questions')
  def get_questions_by_category(id_category):
    
    category=Category.query.filter(Category.id==id_category).one_or_none()
    if category==None:
      abort(404)
    questions= [
      question.format() for question in 
      Question.query.order_by(Question.id).filter(Question.category==id_category).all()
    ]
    page=request.args.get('page',1,type=int)
    paginated_questions=pagination(questions,page)
    categories={category.id:category.type for category in Category.query.order_by(Category.id).all()}
    return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': category.type
        })


  '''
  DONE 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')
        if category['id'] == 0:
            question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        else:
            question = Question.query.filter(Question.id.notin_(previous_questions), Question.category == category['id']).order_by(func.random()).first()

        if question == None:
          abort(404)
          
        return jsonify({
            'success': True,
            'question': question.format(),
        })     

  '''
  DONE 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
      }), 404
  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
      }), 422

  return app

    