import pyhiveapi
import getpass
import json

from pyhiveapi.helper.hive_exceptions import NoApiToken

username = input("Username: ")
password = getpass.getpass('Password:')

auth = pyhiveapi.Auth(username, password)
session = auth.login()
if session.get("ChallengeName") == pyhiveapi.SMS_REQUIRED:
    # Complete SMS 2FA.
    code = input("Enter your 2FA code: ")
    session = auth.sms_2fa(code, session)

if "AuthenticationResult" in session:
    print(json.dumps(session["AuthenticationResult"], indent=2))
else:
    raise NoApiToken
