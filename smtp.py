'''
Send-In-Blue: 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
'''

# import requests
import tokenZ as tz

# api = tz.smtp_key

url = "https://api.brevo.com/v3/smtp/email"
# api = "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"

# Customize the HTML content with an embedded button link
html_content = """
<html>
  <body>
    <h1>Hello!</h1>
    <p>This is a greetings message.</p>
    <a href="{}" style="background-color: #008CBA; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Click Me</a>
  </body>
</html>
"""

payload_schema = {
    "sender": {
        "name": "Web2app-Support",
        "email": "no-reply@myshop.com"
    },
    "to": [
        {
            "email": "rsnehasish1251@gmail.com",
            "name": "Recipient's Name"
        }
    ],
    "subject": "Greetings!",
    "htmlContent": html_content
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": 'api'
}

def verify_Token(token):...

def content(link) -> str:
    # html_=html_content
    # dynamic_link = link
    html_ = html_content.format(link)
    # print(html_)
    return html_

def send_mail(link,name,email):
    # prepare link:
    ## get with JWT ....

    payload = payload_schema.copy()
    payload["htmlContent"] = content(link)
    # name-email:
    payload_ = lambda email,name: payload["to"][0].update({"email":email,'name':name})
    payload_(name=name,email=email)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Greetings message sent successfully.")
    else:
        print("Failed to send greetings message. Status code:", response.status_code)
        print(response.text)


# payload_('r@125','roy')
# print(payload)
# html-content:

# send_mail(name='LambdaX',email="rsnehasish1251@gmail.com",link='https://github.com/sendinblue/APIv3-python-library')
