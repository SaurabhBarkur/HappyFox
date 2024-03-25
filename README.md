
# Happy Fox

This is a standalone Python script that integrates
with Gmail API and performs some rule based
operations on emails.


## Installation

Once the project is cloned , follow the below steps
```
cd HappyFox
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

Note:
Make sure you have python version >= 3.7

## Run Locally

Prepare your rules.json according to below format.
```
[
  {
    "description": "Rule1",
    "condition": "any",
    "properties": [
      {
        "field": "email_from",
        "operation": "contains",
        "value": "Avinash"
      },
      {
        "field": "date",
        "operation": "less_than",
        "value": "1"
      }
    ],
    "actions": [
      {
        "type": "Move",
        "destination": "Inbox"
      },
      {
        "mark_read": "True"
      }
    ]
  }
]
```
```
Note: 
1)Only days work for date field so value should be int. Avoid appending days or months
2) Actions are still wip
```

Command:
```
cd project
python manage.py makemigrations
python manage.py migrate
python3 email_processor.py
```

Working:

```

This will open up your browser to select your gmail id and authorize. Once you have authorized your emails will be stored in the database(last 100 emails) and token.json is created then based on the rules in rules.json <description>.json will be created which will have the ouput of the applied rules. As mentioned above action and date field with months is still wip.

```
