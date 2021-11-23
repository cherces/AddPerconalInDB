import requests
import json
import base64
import datetime


API_token = ''
Perco_API_IP = ''


class User:
    def __init__(self):
        self.fio = ""
        self.division_name = ""
        self.position_name = ""
        self.access_template = ""
        self.isInTheDB = False
        self.user_id = -1
        self.division_id = -1
        self.position_id = -1
        self.access_template_id = -1
        self.image = ""


def refresh_token():
    authData = {
        "login": "",
        "password": "",
        "uid": ""
    }
    response = requests.post(Perco_API_IP + "/api/system/auth?", data=authData)

    if response.status_code == 200:
        global API_token
        API_token = json.loads(response.text)["token"]
    else:
        with open("log.txt", "w") as log_file:
            log_file.write(str(datetime.datetime.now()) + response.text)


def checkUserInDB(_user):
    response = requests.get(Perco_API_IP + "/api/users/staff/list?&token=" + API_token)

    if response.status_code == 500:
        with open("log.txt", "w") as log_file:
            log_file.write(str(datetime.datetime.now()) + response.text)
    else:
        json_data = json.loads(response.text)

        f = False

        for item in json_data:
            if item["name"] in _user.fio and item["division_name"].lower() in _user.division_name.lower():
                _user.user_id = item["id"]
                f = True
                break
        if f:
            return True
        else:
            return False


def addNewUser(_user):
    userData = {
        "last_name": "",
        "first_name": "",
        "middle_name": "",
        "hiring_date": "",
        "division": 0,
        "position": 0,
        "access_template": 0,
        "begin_datetime": "",
        "end_datetime": "",
        "photo": ""
    }

    fio = _user.fio.split()

    userData["last_name"] = fio[0]
    userData["first_name"] = fio[1]
    userData["middle_name"] = fio[2]

    userData["hiring_date"] = str(datetime.date.today())
    userData["division"] = getDivisionId(_user.division_name)
    userData["position"] = getPositionId(_user.position_name)

    userData["access_template"] = getAccessTemplateId(_user.access_template)
    userData["begin_datetime"] = str(datetime.datetime.now()).split(".")[0]

    y = datetime.date.today().year + 1
    s = str(datetime.datetime.now()).split("-")
    s[0] = y
    ns = (str(s[0]) + "-" + str(s[1]) + "-" + str(s[2])).split(".")[0]

    userData["end_datetime"] = ns

    userData["photo"] = _user.image
    #print(_user.image)
    print(userData)

    response = requests.put(Perco_API_IP + "/api/users/staff?&token=" + API_token, json=userData)

    if response.status_code == 500:
        with open("log.txt", "w") as log_file:
            log_file.write(str(datetime.datetime.now()) + response.text)
        return False
    else:
        return True


def updateUser(_user):
    userData = {
        "photo": ""
    }

    #_user.image = getBase64Img()
    userData["photo"] = _user.image
    #print(_user.image)

    response = requests.post(Perco_API_IP + "/api/users/staff/" + str(_user.user_id) + "?&token=" + API_token, json=userData)

    if response.status_code == 500:
        with open("log.txt", "w") as log_file:
            log_file.write(str(datetime.datetime.now()) + response.text)
        return False
    else:
        return True


def getDivisionId(division_name):
    response = requests.get(Perco_API_IP + "/api/divisions/list?&token=" + API_token)

    json_data = json.loads(response.text)

    for item in json_data:
        if item["name"].lower() in division_name.lower():
            return item["id"]


def getPositionId(position_name):
    response = requests.get(Perco_API_IP + "/api/positions/list?&token=" + API_token)

    json_data = json.loads(response.text)

    for item in json_data:
        if item["name"].lower() in position_name.lower():
            return item["id"]


def getAccessTemplateId(access_template):
    response = requests.get(Perco_API_IP + "/api/accessTemplates/list?&token=" + API_token)

    json_data = json.loads(response.text)

    for item in json_data:
        if item["name"].lower() in access_template.lower():
            return item["id"]


def getDivisionList():
    response = requests.get(Perco_API_IP + "/api/divisions/list?&token=" + API_token)

    json_data = json.loads(response.text)

    d_list = []

    for item in json_data:
        d_list.append(item["name"])

    return d_list


def getPositionList():
    response = requests.get(Perco_API_IP + "/api/positions/list?&token=" + API_token)

    json_fata = json.loads(response.text)

    p_list = []

    for item in json_fata:
        p_list.append(item["name"])

    return p_list


def getAccessTemplateList():
    response = requests.get(Perco_API_IP + "/api/accessTemplates/list?&token=" + API_token)

    json_data = json.loads(response.text)

    at_list = []

    for item in json_data:
        at_list.append(item["name"])

    return at_list


def getBase64Img():
    with open("пу.jpg", "rb") as img_file:
        imgstring = b'data:image/jpeg;base64,' + base64.b64encode(img_file.read())
    return str(imgstring)


def main(_user):
    if checkUserInDB(_user):
        if updateUser(_user):
            return True
        else:
            return False
    else:
        if addNewUser(_user):
            return True
        else:
            return False