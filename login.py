import cgitb
from http import cookies
import cgi
import socket
import json
import sys
import os
import random
import hashlib
import boto3
for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name # clean up this module's name space a little (optional)
cgitb.enable()
form = cgi.FieldStorage()
dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIA3QPMHYLWUEZOGRW4", aws_secret_access_key="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", region_name="us-east-1")
table = dynamodb.Table('Users')

def success(item):
        if "redirect" not in form:
            print ("<html><body>\n")
            print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/\" />")
            print ("</body></html>")
        else:
            print ("<html><body>\n")
            print ("<meta http-equiv=\"refresh\" content=\"0; url = "+form["redirect"].value+"\" />")
            print ("</body></html>")


if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""

if "login" in os.environ["HTTP_COOKIE"]:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    uname = cookie["username"].value
    psswd = cookie["password"].value
    response = table.get_item(
            Key = {
                    'username':uname
                }
        )
    try:
        item = response["Item"]
        if item["password"] == psswd:
            print("Content-Type: text/html")
            print("")
            success(item)
        else:
            assert False
    except:
        cookie["login"]=""
        cookie["login"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["session"]=""
        cookie["session"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["password"]=""
        cookie["password"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["username"]=""
        cookie["username"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        print("Content-Type: text/html")
        print(cookie.output())
        print("")
        print ("<html><body>\n")
        print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
        print ("</body></html>")
elif "login" not in form:
    print("Content-Type: text/html")
    print("")
    print ("<html><body>\n")
    print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
    print ("</body></html>")
elif "uname" not in form or "psswd" not in form:
    print("Content-Type: text/html")
    print("")
    print(open("loginFailed.html", "r").read())
else:
    response = table.get_item(
            Key = {
                    'username':form["uname"].value
                }
        )
    try:
        item = response["Item"]
        if item["password"] == hashlib.sha3_256(str(form["psswd"].value).encode()).hexdigest():
            print("Content-Type: text/html")
            cookie = cookies.SimpleCookie()
            cookie["session"] = random.randint(0,1000000000)
            cookie["session"]["domain"] = os.environ["HTTP_HOST"]
            cookie["username"] = form["uname"].value
            cookie["username"]["domain"] = os.environ["HTTP_HOST"]
            cookie["password"] = hashlib.sha3_256(str(form["psswd"].value).encode()).hexdigest()
            cookie["password"]["domain"] = os.environ["HTTP_HOST"]
            cookie["login"] = "login"
            cookie["login"]["domain"] = os.environ["HTTP_HOST"]
            print(cookie.output())
            print("")
            success(item)
        else:
            assert False
    except:
        print("Content-Type: text/html")
        print("")
        print(open("loginFailed.html", "r").read())