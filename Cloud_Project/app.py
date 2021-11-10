from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import boto3

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/sound", methods = ["POST"])
@cross_origin()
def sound():
    if request.method == "POST":
        text = request.form['texttospeech']    
        polly = boto3.client(service_name='polly',region_name='us-east-1')  
        response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Joanna',Text=text)
        file = open('static/audio/speech.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()
    return render_template("index.html",conversion="Your Text has been converted to speech...")

@app.route("/emotion", methods = ["POST"])
@cross_origin()
def emotion():
    if request.method == "POST":
        text = request.form['texttospeech']    
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1') 
        emotions=comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return render_template("index.html", sentiment=emotions['Sentiment'], pos=emotions['SentimentScore']['Positive'], neg=emotions['SentimentScore']['Negative'], neu=emotions['SentimentScore']['Neutral'], mix=emotions['SentimentScore']['Mixed'])
@app.route("/translation", methods = ["POST"])
@cross_origin()
def translation():
    if request.method == "POST":
        text = request.form['texttospeech']    
        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
        result = translate.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode="de")
    return render_template("index.html", trans=result.get('TranslatedText'))
  
if __name__ == "__main__":
    app.run(debug=True)
