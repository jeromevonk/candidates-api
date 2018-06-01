# Candidates API
This is an example of a RESTful API for inserting candidates in a database.

It's developed in **Python**, version 3.6.4, taking advantage of the [Flask](http://flask.pocoo.org/) microframework.

It's hosted on heroku, you can [find it here](https://candidates-api.herokuapp.com/).

The API expects documents in JSON format.

These are the endpoint implemented:

| Method | Uri                                   | Meaning                    |
| ------ | :------------------------------------ | :------------------------- |
| GET    | /candidates/api/v1.0/candidates       | Get list of candidates     |
| GET    | /candidates/api/v1.0/candidates/id    | Get single candidate       |
| POST   | /candidates/api/v1.0/candidates       | Insert candidate           |
| POST   | /candidates/api/v1.0/candidates/batch | Insert batch of candidates |
| PUT    | /candidates/api/v1.0/candidates/id    | Update a candidate         |
| DELETE | /candidates/api/v1.0/candidates/id    | Delete a candidate         |

And these are the parameters for a candidate:

| Field      | Mandatory? | Format                      |
| ---------- | ---------- | --------------------------- |
| Name       | Yes        | String                      |
| Gender     | Yes        | "Male" or "Female"          |
| Email      | Yes        | String                      |
| Phone      | Yes        | Only numbers: 5511912345678 |
| Address    | Yes        | String                      |
| Latitude   | No         | Float                       |
| Longitude  | No         | Float                       |
| Tags       | No         | List of Strings             |
| Experience | No         | List of Strings             |
| Education  | No         | List of Strings             |
| Picture    | No         | Base64                      |
| Birthdate  | No         | DD/MM/YYYY                  |

