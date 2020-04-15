# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export DB_USER="<your database username>"
export DB_PASSWORD="<your database password>"
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing 

To running the test correctly, first you should drop the database and recreate it. To do so, you just have to execute the following sentences in a bash terminal from the backend folder: 

```bash
dropdb trivia
createdb trivia
psql trivia<trivia.psql
python test_flaskr.py
```
## API Reference

### Getting started
- Base URL: At this moment this API only works in your local machine in the port 5000, so the base URL for our API is  http://127.0.0.1:5000 
- Authentication : This version of the API doesn't require authentication

### Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample URL : curl http://127.0.0.1:5000/categories
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
 
```json
{
 "1" : "Science",
 "2" : "Art",
 "3" : "Geography",
 "4" : "History",
 "5" : "Entertainment",
 "6" : "Sports"
} 
```

GET '/questions'
- Fetches the full set of questions in our database
- Required Arguments: None
- Sample URL : curl http://127.0.0.1:5000/questions
- Returns :
    - a dictionary of categories, 
    - current category
    - the complete set of questions in our database
    - the flag success (True if everything went right)
    - total_questions : The number of questions availables in our database
- Sample:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "ALL",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    } ],
  "success": true,
  "total_questions": 2
```

DELETE '/questions/<id_question>'
- Delete a question from the database
- Request Arguments: The id in the url of the question to delete
- Sample URL : curl -X DELETE http://127.0.0.1:5000/questions 
- Returns :
    - the flag success (True if everything went right)
    - id of the question deleted
- Sample :
```json
  {
      "success": true,
      "deleted": 5
  }
```

POST '/questions'
- Create a question in the database or search for a question in the database
- Required Arguments: A question with the following format:
```json
    {
        "question" : "What is the name of Son Goku's second son?",
        "answer" : "Son Gotten",
        "category" : 5,
        "difficulty" : 3

    }
```
- Sample URL : curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/questions -d '{"question": "question text", "answer": "answer", "difficulty": "1", "category": "1"}'
- Returns :
    - the flag success (True if everything went right)
    - id of the question created
- Sample : 
```json
  {
      "success": true,
      "id_question": 5
  }
```
GET '/categories/<id_category>/questions'
- Gets a set of questions by category
- Required Arguments : The id of the category used to filter by in the url of the request
- Sample URL:  curl http://127.0.0.1:5000/categories/3/questions
- Returns :
    - a dictionary of categories, 
    - current category
    - the questions from the category 
    - the flag success (True if everything went right)
    - total_questions : The number of questions availables in our database 
- Sample : 
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
POST '/quizzes'
- Return a question from the category selected 
- Sample: curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes -d '{"previous_questions": [],"quiz_category": {"type": "category type", "id": "3"}}'
- Required arguments : a json object with the following format : 
```json
{
    "previous_questions": [9],
    "quiz_category": {
        "type":"Entertainment",
         "id": "5" 
    }
}
```
- Returns 
    - the flag success (True if everything went right)
    - A random question from the database for the category selected
- Sample

```json
{
  "question": {
    "answer": "The Palace of Versailles",
    "category": 3,
    "difficulty": 3,
    "id": 14,
    "question": "In which royal palace would you find the Hall of Mirrors?"
  },
  "success": true
}
```
## Authors
José Manuel Díaz Bossini
## Acknowledgements
To Caryn for her teachings and to the udacity team for this great nanodegree

