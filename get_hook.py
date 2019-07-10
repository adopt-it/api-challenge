from flask import Flask, request,render_template, request, redirect, url_for, jsonify
from flask_ngrok import run_with_ngrok
from sys import argv
# http://pymotw.com/2/hmac/
import hmac
import hashlib
# http://techarena51.com/index.php/how-to-install-python-3-and-flask-on-linux/
import subprocess
import os
import json

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

@app.route('/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print(request.headers.get('X-GitHub-Event'))
   print(f"New Json response like: {data}")
   return "OK"

def verify_hmac_hash(data, signature):
    github_secret = bytes(os.environ['GITHUB_SECRET'], 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)


@app.route("/webhook", methods=['POST'])
def github_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            print(payload)
            return payload
            """if payload['commits'][0]['distinct'] == True:
                try:
                    cmd_output = subprocess.check_output(
                        ['git', 'pull', 'origin', 'master'],)
                    subject"Code deployed successfully"
                    email(, cmd_output)
                    return jsonify({'msg': str(cmd_output)})
                except subprocess.CalledProcessError as error:
                    email("Code deployment failed", error.output)
                    return jsonify({'msg': str(error.output)})
            else:
               return jsonify({'msg': 'nothing to commit'})"""
        if request.headers.get('X-GitHub-Event') == "create":
           payload = request.get_json()
           return jsonify({'msg': str(payload["ref"])})
    else:
        return jsonify({'msg': 'invalid hash'})


if __name__ == '__main__':
   app.run()
