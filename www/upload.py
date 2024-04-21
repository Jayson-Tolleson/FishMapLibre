
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# enable debugging
import cgitb
cgitb.enable()

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
 
app = Flask(__name__)
@app.route("/uploader", methods=["GET", "POST"])

def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        locnum = request.form.get('f')
#        f.save(secure_filename("temp" + str(locnum) + ".mp4"))
        f.save(os.path.join('/var/www/fishvid/', secure_filename('temp'+str(locnum)+'.mp4')))
        return "file uploaded successfully"


if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, ssl_context=('/var/security/lftr.biz.crt', '/var/security/lftr.biz.key'), port=8084)
