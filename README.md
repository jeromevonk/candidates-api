# Candidates API
This is an example of a RESTful API for inserting candidates in a database.

It's developed in **Python**, version 3.6.4, taking advantage of the [Flask](http://flask.pocoo.org/) microframework.

It's hosted on heroku, you can find it here.



| method | uri                                   | Meaning                    |
| ------ | :------------------------------------ | :------------------------- |
| GET    | /candidates/api/v1.0/candidates       | Get list of candidates     |
| GET    | /candidates/api/v1.0/candidates/id    | Get single candidate       |
| POST   | /candidates/api/v1.0/candidates       | Insert candidate           |
| POST   | /candidates/api/v1.0/candidates/batch | Insert batch of candidates |
| PUT    | /candidates/api/v1.0/candidates/id    | Update a candidate         |
| DELETE | /candidates/api/v1.0/candidates/id    | Delete a candidate         |



