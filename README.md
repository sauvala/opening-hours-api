# Readme

# Part 1
### Running the application
#### Using Docker
Run in the root folder:
1. `docker build --tag hours-api .`
2. `docker run -p 8080:8080 hours-api`
3. Make a http call to the server with your favorite tool, here I use httpie:
```
echo '{
  "monday": [],
  "tuesday": [
    {
      "type": "open",
      "value": 36000
    },
    {
      "type": "close",
      "value": 64800
    }
  ],
  "wednesday": [],
  "thursday": [
    {
      "type": "open",
      "value": 36000
    },
    {
      "type": "close",
      "value": 64800
    }
  ],
  "friday": [
    {
      "type": "open",
      "value": 36000
    }
  ],
  "saturday": [
    {
      "type": "close",
      "value": 3600
    },
    {
      "type": "open",
      "value": 36000
    }
  ],
  "sunday": [
    {
      "type": "close",
      "value": 3600
    },
    {
      "type": "open",
      "value": 43200
    },
    {
      "type": "close",
      "value": 75600
    }
  ]
}' | http POST 127.0.0.1:8080/api/format

HTTP/1.0 200 OK
Content-Length: 166
Content-Type: application/json
Date: Sun, 31 May 2020 23:33:31 GMT
Server: Werkzeug/1.0.1 Python/3.8.3

{
    "Friday": "10 AM - 1 AM",
    "Monday": "Closed",
    "Saturday": "10 AM - 1 AM",
    "Sunday": "12 PM - 9 PM",
    "Thursday": "10 AM - 6 PM",
    "Tuesday": "10 AM - 6 PM",
    "Wednesday": "Closed"
}
```
(The weekdays seems not to be in order, could need sorting before sending to client)


#### Running without Docker
1. Install pipenv (https://pipenv-fork.readthedocs.io/en/latest/)
2. Use Python 3.8.3 (pyenv recommended)
3. `pipenv shell`
4. `pipenv install`
5. `export FLASK_APP=app_api.py`
6. `cd openinghours/app/`
7. `flask run`
8. Application should be running in `http://127.0.0.1:5000/`


### Notes about the application
- This is just a simple web API that is not prepared for production, e.g. uses development Flask server.
- The formatting code relies heavily on the sorting of times. For example, the opening and closing times for a given day are expected to be in order in the time tables. If they come in a random order, the current implementation doesn't work and would need another approach. 


## Part 2

The data format wasn't optimal for the task for a few reasons:
- The closing times could be marked on the next day and when processing the times the application needs to peek to the next day to get the closing time.
- Weekdays as keys are not easily sortable, the data could be wrapped inside 0..6 number keys and the data could include a clear text value for the date:
- Opening and closing times could be wrapped inside of one JSON-blob, so the link between opening and closing time would be explicit. This would also remove the need to "peek" closing times from the next day if the closing time is marked on the next day.
- Opening times could be marked as opening time + how long the restaurant is open.
- If the data doesn't need to be computer readable, unix timestamps could be replaces with human readable format in the first place :)
