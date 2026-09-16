import numpy as np
import cv2
import os
from os import walk
from os.path import join
import googletrans
from pprint import pprint
from keras.models import load_model
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,Flatten,Conv2D,MaxPooling2D,Dropout
from werkzeug.utils import secure_filename
from flask import Flask
from flask import Flask,render_template,request,redirect,url_for, Response,request,jsonify
import torch
from transformers import BertTokenizer, BertForSequenceClassification

UPLOAD_FOLDER = r'C:\Users\clair\Desktop\AI2down2\W11\static\img'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_model_and_tokenizer(model_path, tokenizer_name):
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
    model.eval()  # 將模型設定為評估模式
    return model, tokenizer

# 预处理文本
def preprocess_text(text, tokenizer, max_len=128):
    encodings = tokenizer(text, truncation=True, padding='max_length', max_length=max_len, return_tensors='pt')
    return encodings

# 预测文本情感
def predict_sentiment(text, model, tokenizer):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    encodings = preprocess_text(text, tokenizer)
    with torch.no_grad():
        inputs = {key: val.to(device) for key, val in encodings.items()}
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=-1)

    print(prediction)
    if prediction.item() == 1:
        return "正評"
    
    else:
        return "負評"

@app.route("/")
def index():
  
  return render_template('home.html')

@app.route("/upload",methods=["GET","POST"])
def upload():
  if request.method=="POST":
    upload_files=request.files.getlist("file[]")
    filenames=[]
  for file in upload_files:
    filename = secure_filename(file.filename)

    filenames.append(filename)
    file.save(UPLOAD_FOLDER+"\\"+file.filename)
  return render_template('home.html')

@app.route("/predict_image",methods=[ "GET",'POST'])
def predict_image():
  # model=load_model('sentence_base.h5')
  model = load_model('categorical_model.h5')
  result_str=[]
  mypath=r"C:\Users\clair\Desktop\AI2down2\W11\static\img"
  for files in walk(mypath):
    for f in files[2]:
  
      image_path=join(files[0],f)
      
      image=cv2.imread(image_path)
      image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

      image=cv2.resize(image,(400,400))
      image=image.astype('float32')/255.0
      image=np.expand_dims(image,axis=0)

      predictions=model.predict(image)

      predicted_class=np.argmax(predictions,axis=1)
      class_result=predicted_class
      pre_class=[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],[29],[30],[31],[32],[33],[34],[35]]
      char=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
      # pre_class=[[0],[1],[2],[3],[4],[5],[6],[7],[8]]
      # char=["a","e","f","l","o","r","s","u","v"]
      index=pre_class.index(class_result)
      char_class=char[index]
      
      result_str.append(char_class)
  arr=np.array(result_str)
  str=''.join(arr)

  for files in walk(mypath):
    for f in files[2]:
        image_path=join(files[0],f)
        os.remove(image_path)
            
  return jsonify({"result":str})

@app.route("/predict_text",methods=[ "GET",'POST'])
def predict_text():
  sentence_e=request.form.get('sentence')
  
  translator=googletrans.Translator()
  result=translator.translate(sentence_e,dest='zh-tw')
  translate=result.text
  model_path = 'W11/bert_chinese_model'
  tokenizer_name = 'bert-base-chinese'
  model, tokenizer = load_model_and_tokenizer(model_path, tokenizer_name)
  
  sentiment = predict_sentiment(translate, model, tokenizer)

  return jsonify({"result":f"*原手語辨識 : {sentence_e}* <br> *中文翻譯 : {translate}* <br> *文本情感為 : {sentiment}*"})
  

app.run()
