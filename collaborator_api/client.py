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
}

class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        url = "https://api.collaboratoronline.com/webAPIConsumer/api/MobileToken/GetTokenForUser"
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
        if result.text == "Auth Failed":
            raise Exception("Auth Failed")
        self.token = result.json()

    def new_task_feedback(self):
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
        };
        url = "https://api.collaboratoronline.com/webAPIConsumer/api/Task/SaveNewTaskFeedback"
        request_headers = {
            "accept": "application/json",
            "authorization": f"Bearer { self.token }",
            "deviceId":  "COMUNITY",
            "appVersion": "1.1.6",
        }
        result = requests.post(url, headers=request_headers, json=request_data)

        # returns 401 when auth header not provided.
        # Returns 500 for some error with text {"Message":"An error has occurred."}
        print(result.text)
        result.raise_for_status()

        print(result.json())


    def get_task(self):
        objData = {
            template_id: 10,
            obj_id: 1671,
            Fields: [
            ],
        };
