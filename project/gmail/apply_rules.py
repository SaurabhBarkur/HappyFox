from .models import Email
from django.db.models import Q
import json
from .serializers import EmailSerializer
import datetime

rules_file = "rules.json"
operation_mapping = {
    "contains": "icontains",
    "does_not_contains": "icontains",
    "equals": "exact",
    "not_equals": "exact",
    "less_than": "lt",
    "greater_than": "gt"
}


def filter_date(value):
    # Parse the date value from the JSON
    value = int(value)  #todo add month, only date works now
    today = datetime.datetime.now().date()
    value = today - datetime.timedelta(days=value)
    return value


def apply_rules():
    emails = Email.objects.all()
    with open(rules_file, 'r') as file:
        rules = json.load(file)

    for rule in rules:
        res = Q()
        binding = rule.get("condition")
        for obj in rule.get("properties"):
            field = obj.get("field")
            operation = obj.get("operation")
            value = obj.get("value")
            lookup = operation_mapping.get(operation)
            if field == "date":
                value = filter_date(value)
            if "not" in operation:
                condition = ~Q(**{f"{field}__{lookup}": value})
            else:
                condition = Q(**{f"{field}__{lookup}": value})
            if binding.lower() == "all":
                if field in Email.get_model_fields():
                    res &= condition
            else:
                res |= condition

        output_file = f"output/{rule.get('description')}.json"
        with open(output_file, 'w') as file:
            ser = EmailSerializer(emails.filter(res), many=True)
            json.dump(ser.data, file)





