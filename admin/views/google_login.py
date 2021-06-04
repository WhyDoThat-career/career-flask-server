from admin import app,db
from admin import google_client,google_discovery_uri,google_oauth
from flask import request, redirect, url_for, session
from flask_login import current_user
from flask_restx import Resource
from admin.control import user_mgmt
import requests, json
from admin.views.loginAPI import LoginFunc

def get_google_provider_cfg():
    return requests.get(google_discovery_uri).json()

@LoginFunc.route("/google")
class GoogleLogin(Resource) :
    def get(self):
        '''구글 로그인 API'''
        if not current_user.is_authenticated :
            # Find out what URL to hit for Google login
            google_provider_cfg = get_google_provider_cfg()
            authorization_endpoint = google_provider_cfg["authorization_endpoint"]

            # Use library to construct the request for Google login and provide
            # scopes that let you retrieve user's profile from Google
            request_uri = google_client.prepare_request_uri(
                authorization_endpoint,
                redirect_uri=request.base_url.replace('http','https') + "/callback",
                scope=["openid", "email", "profile"],
            )
            return redirect(request_uri)
        else :
            return redirect(url_for('index'))

@LoginFunc.route("/google/callback")
@LoginFunc.hide
class GoogleLoginCallback(Resource) :
    def get(self):
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = google_client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url.replace('http','https'),
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(google_oauth['client_id'], google_oauth['client_secret']),
        )

        # Parse the tokens!
        google_client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = google_client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        social_data = dict()

        if userinfo_response.json().get("email_verified"):
            social_data['unique_id'] = userinfo_response.json()["sub"]
            social_data['user_email'] = userinfo_response.json()["email"]
            social_data['user_name'] = userinfo_response.json()["name"]
            social_data['thumbnail'] = userinfo_response.json()['picture']
        else:
            return "User email not available or not verified by Google.", 400

        user_mgmt.social_login(social_data,platform='google')
        return redirect(url_for('index'))