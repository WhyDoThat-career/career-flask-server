from admin import app,db
from admin import github_client,github_oauth
from flask import request, redirect, url_for, session
from flask_login import current_user
from admin.control import user_mgmt
import requests, json

@app.route("/github_login")
def github_login() :
    if not current_user.is_authenticated :
        request_uri = github_client.prepare_request_uri(
            github_oauth['auth_uri'],
            redirect_uri=request.base_url + "/callback",
            scope="user:email read:org read:user",
        )
        return redirect(request_uri)
    else :
        return redirect(url_for('index'))

@app.route("/github_login/callback")
def github_callback():
    code = request.args.get("code")
    token_endpoint = github_oauth["token_uri"]

    token_url, headers, body = github_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    headers['Accept'] = 'application/json'
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(github_oauth['client_id'], github_oauth['client_secret']),
    )

    # Parse the tokens!
    github_client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = github_oauth["user_info_uri"]
    useremail_endpoint = github_oauth['user_email_uri']

    uri, headers, body = github_client.add_token(userinfo_endpoint)
    email_uri, email_headers, email_body = github_client.add_token(useremail_endpoint)
    email_headers['Accept'] = 'application/json'

    userinfo_response = requests.get(uri, headers=headers, data=body)
    useremail_response = requests.get(email_uri, headers=email_headers, data=email_body)
    useremail_data = json.loads(useremail_response.content)[0]

    social_data = dict()

    if useremail_data["verified"]:
        social_data['unique_id'] = userinfo_response.json()["id"]
        social_data['user_email'] = useremail_data["email"]
        social_data['user_name'] = userinfo_response.json()["login"]
    else:
        return "User email not available or not verified by Github.", 400

    user_mgmt.social_login(social_data,platform='github')
    return redirect(url_for('index'))