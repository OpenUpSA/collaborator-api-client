import requests

code_table = {
    "type": "F1",
    "user_name": "F2",
    "user_surname": "F3",
    "user_mobile_number": "F4",
    "user_email_address": "F5",
    "municipal_account_number": "F6",
    "street_name": "F7",
    "street_number": "F8",
    "suburb": "F9",
    "description": "F10",
    "coordinates": "F11",
    "request_date": "F12",
    "mobile_reference": "F13",
    "on_premis_reference": "F14",
    "status": "F15",
    "demarcation_code": "F20",
}


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()

    def authenticate(self):
        # url = "https://api.collaboratoronline.com/webAPIConsumer/api/MobileToken/GetTokenForUser"
        url = "https://consumercollab.collaboratoronline.com/webAPI/api/MobileToken/GetTokenForUser"
        request_data = {
            "username": self.username,
            "password": self.password,
        }
        request_headers = {
            "accept": "application/json",
            "authorization": "Bearer ",
            "deviceId":  "COMUNITY",
            "appVersion": "1.1.6",
        }
        result = requests.post(url, headers=request_headers, json=request_data)
        result.raise_for_status() # Watch out, they do return 200 for "Auth Failed"
        if result.text == "\"Auth Failed\"":
            raise Exception("Auth Failed :(")
        self.token = result.json()

    def new_task_feedback(self):
        url = "https://consumercollab.collaboratoronline.com/webAPIConsumer/api/Task/SaveNewTaskFeedback"
        request_data = {
            "TemplateId": 9,
            "BPID": 3,
            "PercentComplete": 0,
            "Comments": "Feedback done from OpenUp",
            "FormFields": [
                { "FieldID": "F1", "FieldValue": "Roads"},
                { "FieldID": "F2", "FieldValue": "JD"},
                { "FieldID": "F3", "FieldValue": "Bothma"},
                { "FieldID": "F4", "FieldValue": "0792816737"},
                { "FieldID": "F5", "FieldValue": "jd@openup.org.za"},
                { "FieldID": "F6", "FieldValue": "1234567"},
                { "FieldID": "F7", "FieldValue": "Here street"},
                { "FieldID": "F8", "FieldValue": "123"},
                { "FieldID": "F9", "FieldValue": "there suburb"},
                { "FieldID": "F10", "FieldValue": "This is a test. If you see this, please email me."},
                { "FieldID": "F12", "FieldValue": "2020-11-03"},
            ],
        }
        request_headers = {
            "accept": "application/json",
            "authorization": f"Bearer { self.token }",
            "deviceId":  "COMUNITY",
            "appVersion": "1.1.6",
        }
        request = requests.Request("POST", url, headers=request_headers, json=request_data)
        prepared_request = request.prepare()
        pretty_print_POST(prepared_request)
        result = self.session.send(prepared_request)

        # returns 401 when auth header not provided.
        # Returns 500 for some error with text {"Message":"An error has occurred."}
        print(result.text)
        result.raise_for_status()

        print(result.json())

    def get_task(self, obj_id: int, template_id: int = 9,  fields: list = None):
        url = "https://consumercollab.collaboratoronline.com/webapi/api/Objects/GetObject"
        if fields is None:
            fields = []
        if not self.token:
            raise Exception("Auth Token not set. Did you login with authenticate()?")

        request_data = {
            "template_id": template_id,  # 9
            "obj_id": obj_id,  # 1?
            "Fields": fields,
        }
        request_headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}",
            "deviceId": "COMUNITY",
            "appVersion": "1.1.6",
        }

        request = requests.Request("POST", url, headers=request_headers, json=request_data)
        prepared_request = request.prepare()
        pretty_print_POST(prepared_request)
        result = self.session.send(prepared_request)

        # returns 401 when auth header not provided.
        # Returns 500 for some error with text {"Message":"An error has occurred."}
        print(result.text)
        result.raise_for_status()
        print(result.json())

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    https://stackoverflow.com/a/23816211
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
