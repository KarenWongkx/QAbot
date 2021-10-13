import os
import pickle
from flask import Flask, request, jsonify
import logging
from Bani.Bani import Bani
from Bani.core.FAQ import FAQ

logging.basicConfig(level=logging.ERROR)

FAQSTORE_PATH = "/faq_store"
MODEL_PATH = "/model"

def load_faq():
    faq_list = []
    # this look at the faqStore for .pkl extension, create faq with the file_name
    for file_name in os.listdir(FAQSTORE_PATH):
        if file_name.endswith(".pkl"):
            faq_name = file_name.partition('.')[0]
            print(f"FAQ name: {faq_name}")
            faq_name = FAQ(name=faq_name)
            faq_name.load(FAQSTORE_PATH)
            faq_list.append(faq_name)
            print(f"FAQ created from {file_name}")
    return faq_list

loaded_faq_list = load_faq()
masterBot = Bani(FAQs=loaded_faq_list, modelPath=MODEL_PATH)
print(f"MasterBot created")

app = Flask(__name__)

@app.route("/")
def main():
    return jsonify(result="hello world")


@app.route("/answer", methods=["GET"])
def getAnswer():
    global masterConfig
    global interfaces
    params = request.args
    if "question" not in params:
        return "Question not found.", 400
    question = params["question"]

    outputs = masterBot.findClosest(question, K=1)

    code = -1
    answer = None
    similarQns = []

    if outputs[0].maxScore < 0.5:
        # if confidence level not high enough
        # get closest question from each FAQ
        code = 1
        answer = ""
        for out in outputs:
          similarQns.append(out.question.text)

    elif outputs[0].maxScore - outputs[1].maxScore < 0.05:
        code = 2
        answer = outputs[0].answer.text
        similarQns.append(outputs[0].question.text)
        for out in outputs[1:]:
            if outputs[0].maxScore - out.maxScore < 0.05:
                similarQns.append(out.question.text)
            else:
                break

    code = 0 if code==-1 else code
    answer = outputs[0].answer.text.strip() if answer==None else answer
    similarQns = outputs[0].similarQuestions if len(similarQns)==0 else similarQns

    return jsonify(code=code, result=answer, similarQuestions=similarQns)
    

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=os.getenv("PORT", 1995), threaded=True) 
    app.run(host="0.0.0.0", port=8057, threaded=True) 
    
