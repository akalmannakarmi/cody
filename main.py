from flask import Flask , render_template, request,redirect,session
from os import path
from termcolor import cprint
import json
from time import time,sleep

app = Flask(__name__)
app.secret_key ="secret"

@app.route('/qna',methods=['POST'])
def qna():
    startTime = time()
    # Set all data recived to session
    rData = json.loads(request.data) 
    
    #Print data Recived
    cprint(f"Users {rData}",'blue')
        
    with open('qna/ver1/c2/v10/1.json','r') as file:
        result = json.load(file) 
    cprint(f"Users Data Sent:{time()-startTime}",'cyan')
    return result


@app.route('/')
@app.route('/<path:p>')
def default(p=""):
    cprint(f"Data Recived:{p}",'blue')
    for key, value in request.form.items():
        cprint((key,value),'blue')
    if p == "":
        return render_template("index.html",session=session)
    p = p.lower()+".html"
    if path.exists(f"templates/{p}") and not p.startswith('0'):
        return render_template(p)
    return render_template("error.html",error=f"{p} does not exist")

if __name__ == "__main__":
    app.run(debug=False)