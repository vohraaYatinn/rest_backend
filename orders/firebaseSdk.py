import firebase_admin
from firebase_admin import credentials, messaging
import firebase_admin
from firebase_admin import credentials

service_account_info = {
  "type": "service_account",
  "project_id": "restportguese",
  "private_key_id": "49ff47223a7c4ab900b23e2724d9477ed2b9fd1c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5LGru/FAPPwuw\nyYZwCZMO61twsul17rNVYqv4NB25SijhJGdJ7MjcnLVCUkzJzHiiJutIabQFHf3+\nxZO1P+oVgRdyAEQspwbGNpOti86itDGs/9zsW3DUEzae/+U0H7YtkZxyaLmn10Ub\nTmkZLzx3j+ATzGz5FfzqHyLaP0ufXwzzYWdkwXcKEo3g6LcXW3TMYSXkljbhnblI\nAyoZ4SZibCuQeKbhDCe38WKkkMt5O0Jg6r5AnGteTySR6lD+0C4+r+tnwGwZg21u\nHgvIiVfHqJtILIZCERVbdqJzyiaEAsL5yEoy0R8pPVUjgJQO5ew1PTqjFm62a6/S\nJO+yjJopAgMBAAECggEADvNnOolXKnVNQOvIhb0UKU53Q9EXjfIk+xt8JeOz/wJI\nl4MBru47ZSqRl6ZUSlp5ZqLh+NGwsKq/AlDFWrXrdRXcRNQA180a5tVAaluhJlxf\nrWeRg2jk93k0qLT3C9S/+AvAwrEHb7svD85ufb4lXERFfpERFFxs3vdUGvnPezFv\n/fWwAaIk9eX3NzKO3oPUkFksLkcsGmj4es3dkntm4zsBlI9sHzQP81TjIZ3cfZzI\nO+fTNbwru1YzZpwyJStLI8x1Jk4P2FAfQeWAwN2W7G+JtC33bWf7vdOE3E1K3QYe\nYdY2gJHhFYhKmIJh1T1MV9rNiO2ltpyIuCxNRcu6/QKBgQD0G+Rd5XDTL6q2w/Hu\n9alG9B30TXTyn9EWUAh7eWAOmgLjCMno92TYm18pwvsLa7+tQGBBNlMzveOC6dXU\nGy19Dv3/PDbQv7ATy+JJMi2DA85fFlJr+O0fdrakIh0FdwO3cqD05XmbCG9lKP6B\n6plzzsway7y+G/eTc4/cRfPitQKBgQDCMZV6lCOxvYCDQh1l53Pive+sALgHe8Jk\ntMU7Y3pWi7goAuDym9x+42ChVXz9jqxJ6CvNf2VpmFHsCMFUfHOVQy3xmaL9u+8q\nVUSeWEUw+PfAnv9i9ogQbmdBSj0NZKE/lESlt2/5E1UhOihK93CaMcXfKnJaV0gh\nF7diVfE+JQKBgDXmnsNY8VPAd7qJg7dXCTzAlIioPcWBIoMBww24nEw9F5wYCbVm\nQx9NF3M6OYKpFRblWxurKi4HpN/4UB3Yrm+pys379sKbQP7uCxZMfR4rzfrTC/oJ\nahqDdQrC+ZOGVwy/w+ivbu2brDUzGxeGvMGEjS7xg8ialk05vC9QRuztAoGBAISO\n1DqYZMUvVkpDF044cCKXBMOkufphwJB91SR1A02QkmS9klAJlLoI/C0k7e0nNvQ8\nR6o/DDrIfyNf1piVW1DIStRgy6HoZ5m+Gtj76D9Fs9kIr8wd/UM6GcG3q3U4+9kq\nnLGCRiz/xVypFlgWEAcxcqCjmOuSKOpuBgBaKhMBAoGBAKBFxHWwwVAjE5GxB61Y\nrYy7Ph5FWwE4stNxTuB4fal7c+CDKWTQqq55eL1IqJtkUWClb+jgMtiQatAgDjmZ\nFpuKNqf81FoMD/yyUI0brG/4vH2+emLiR8V6SWeXcy+MXnxfF1/eZG50/F8nByjU\nl1cnMIxqwB1/7MFSL+CcM2ER\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-i8zn4@restportguese.iam.gserviceaccount.com",
  "client_id": "112883991693727875845",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-i8zn4%40restportguese.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

def send_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    try:
        response = messaging.send(message)
        print(f'Successfully sent notification: {response}')
    except Exception as e:
        print(f'Error sending notification: {e}')
