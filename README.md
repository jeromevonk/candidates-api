# Candidates API
This is an example of a RESTful API for inserting candidates in a database.

It's developed in **Python**, version 3.6.4, taking advantage of the [Flask](http://flask.pocoo.org/) microframework.

Dependencies:

- Flask
- flask_sqlalchemy
- flask_marshmallow
- marshmallow-sqlalchemy

It's hosted on heroku [here](https://candidates-api.herokuapp.com/). But as heroku's  filesystem is [ephemeral](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem), the data gets reset everytime the dyno is restated (under under normal operations, every day)

The API expects documents in JSON format.

#### These are the endpoints implemented:

| Method | Uri                                   | Meaning                    | Needs Auth? |
| ------ | :------------------------------------ | :------------------------- | :------------------------: |
| GET    | /candidates/api/v1.0/candidates       | Get list of candidates     |No|
| GET    | /candidates/api/v1.0/candidates/id    | Get single candidate       |No|
| POST   | /candidates/api/v1.0/candidates       | Insert candidate           |No|
| POST   | /candidates/api/v1.0/candidates/batch | Insert batch of candidates |No|
| PUT    | /candidates/api/v1.0/candidates/id    | Update a candidate         |Yes|
| DELETE | /candidates/api/v1.0/candidates/id    | Delete a candidate         |Yes|

#### These are the credentials:

User: user
Password: 123

------

#### And these are the parameters for a candidate:

| Field      | Mandatory? | Format                                                       |
| ---------- | :--------: | ------------------------------------------------------------ |
| Name       |    Yes     | String                                                       |
| Gender     |    Yes     | 0, 1, 2 or 9 - see [ISO/IEC 5218](https://en.wikipedia.org/wiki/ISO/IEC_5218) |
| Email      |    Yes     | String                                                       |
| Phone      |    Yes     | Only numbers: 11912345678                                    |
| Address    |    Yes     | String                                                       |
| Experience |     No     | List of Dictionaries (see below)                                              |
| Education  |     No     | List of Dictionaries (see below)                                              |
| Tags       |     No     | List of Strings                                              |
| Birthdate  |     No     | DD/MM/YYYY                                                   |
| Latitude   |     No     | Float                                                        |
| Longitude  |     No     | Float                                                        |
| Picture    |     No     | Base64 encoded JPEG format                                   |

#### Education dictionary

| FIELD       | FORMAT     |
| :---------- | :--------- |
| Institution | String     |
| Degree      | String     |
| Date start  | DD/MM/YYYY |
| Date end    | DD/MM/YYYY |
| Description | String     |

#### Experience dictionary

| FIELD       | FORMAT     |
| :---------- | :--------- |
| Company     | String     |
| Job Title   | String     |
| Date start  | DD/MM/YYYY |
| Date end    | DD/MM/YYYY |
| Description | String     |

#### Instructions

In order to send a batch of candidates, the following must be met:

- Create a .zip file with .json files inside;
- Make a post request to /candidates/api/v1.0/candidates/batch with `enctype="multipart/form-data"` and `name="zipfile"`

A sample canditate.json file should look like this:
```xml
{
	"name": "Jerome Vergueiro Vonk",
	"picture": "",
	"birthdate": "18/02/1988",
	"gender": 1,
	"email": "vonk@gmail.com",
	"phone": "11912345678",
	"address": "Avenida Paulista, 1",
	"longitude": 0,
	"latitude": 0,
	"tags": ["mecathronics", "dutch/brazilian"],
	"experience": [{
		"company": "Diebold",
		"job_title": "Engineer",
		"date_start": "01/01/2007",
		"date_end": "31/12/2011",
		"description": "Mechatronics Engineering is a field between mechanics and elethronics"
	}, {
		"company": "EA",
		"job_title": "Tester",
		"date_start": "15/06/2017",
		"date_end": "28/09/2018",
		"description": "Localization tester for brazilian portuguese"
	}],
	"education": [{
		"institution": "USP",
		"degree": "Engineering",
		"date_start": "01/01/2007",
		"date_end": "31/12/2011",
		"description": "Mechatronics Engineering is a field between mechanics and elethronics"
	}]
}
```
Kindly have a look a the [test folder](https://github.com/jeromevonk/candidates-api/tree/master/test) for more test examples.
