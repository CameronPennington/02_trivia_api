import os
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy()
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Add-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by('id').all()
    formatted_categories = [category.format() for category in categories]
    
    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'status_code': 200
    })

  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    questions = Question.query.order_by('id').all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.order_by('id').all()
    formatted_categories = [category.format() for category in categories]

    category_items = [(category.type) for category in categories]
    #categories has to return as an object
    return jsonify({
      'success': True,
      'status_code': 200,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'categories': category_items
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      
      question = Question.query.filter(Question.id == question_id).one_or_none()
      question.delete()

      db.session.commit()
    except:
 
      db.session.rollback()
    finally:
      db.session.close()
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10
      questions = Question.query.order_by('id').all()
      formatted_questions = [question.format() for question in questions]
      categories = Category.query.order_by('id').all()
      category_items = [(category.type) for category in categories]
    return jsonify({
      'success': True,
      'status_code': 200,
      'deleted': question_id,
      'total_questions': len(formatted_questions),
      'questions': formatted_questions[start:end]
    })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_new_question():
    try:
      new_question = Question(
        question = request.get_json('question'),
        answer = request.get_json('answer'),
        category = request.get_json('category'),
        difficulty = reuqest.get_json('difficulty')
      )
      db.session.add(new_question)

      db.session.commit()
    except:
 
      db.session.rollback()
    finally:
      db.session.close()

    return jsonify({
      'success': True,
      'status_code': 200
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    