import json
from os import path,makedirs

class CreateQNA:
    def __init__(self):
        self.ver = "ver1"
        self.category = "WAP WAP WAP"
        self.value = "10"
        self.question = "q1"
        self.answer = "a1"
    
    def write(self):
        data = {"qnas":[]}
        p = f"qna/{self.ver}/{self.category}/{self.value}.json"
        if path.exists(p):
            with open(p,'r') as file:
                data = json.load(file)
        else:
            makedirs(f"qna/{self.ver}/{self.category}")
            
        data["qnas"].append({"question":self.question,"answer":self.answer})
        with open(p,'w') as file:
            file.write(json.dumps(data))
    
    def create(self):
        self.ver = "ver1"
        self.category = "WAP WAP WAP"
        self.value = "10"
        self.question = ""
        self.answer = ""
        self.write()
    
qnaCreator= CreateQNA()
qnaCreator.create()
print("DOne")