import json
from os import path,makedirs

class CreateQNA:
    def __init__(self):
        self.ver = "verInf"
        self.category = "default"
        self.value = "10"
        self.question = ""
        self.answer = ""
        self.qCode = ""
        self.aCode = ""
        self.qImage = ""
        self.aImage = ""
    
    def write(self):
        data = {"qnas":[]}
        val = {}
        
        p = f"qna/{self.ver}/{self.category}/{self.value}.json"
        if path.exists(p):
            with open(p,'r') as file:
                data = json.load(file)
        elif not path.exists(f"qna/{self.ver}/{self.category}"):
            makedirs(f"qna/{self.ver}/{self.category}")
        
        if self.question:
            val["question"] = self.question 
        if self.qCode:
            val["qcode"] = self.qCode 
        if self.qImage:
            val["qimage"] = self.qImage 
        if self.answer:
            val["answer"] = self.answer 
        if self.aCode:
            val["acode"] = self.aCode 
        if self.aImage:
            val["aimage"] = self.aImage 
        
        data["qnas"].append(val)
        with open(p,'w') as file:
            file.write(json.dumps(data))
    
    def create(self):
        self.ver = "ver1"
        self.category = "Memes"
        self.value = "50"
        
        self.question = "Explain the Meme"
        self.qCode = """"""
        self.qImage = """qna/ver1/img/infLoop.png"""
        
        self.answer = "The programmer keep buying milk."
        self.aCode = """"""
        self.aImage = """"""
        self.write()
    
qnaCreator= CreateQNA()
qnaCreator.create()
print("DOne")