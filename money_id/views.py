from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image
import cv2, time
import boto3
# importing speech recognition package from google api 
import speech_recognition as sr 
import playsound # to play saved mp3 file 
from gtts import gTTS # google text to speech 
import os # to save/open files 
import wolframalpha # to calculate strings into formula 
from selenium import webdriver # to control browser operations 

# Create your views here.
num = 1
def assistant_speaks(output): 
	global num 

	# num to rename every audio file 
	# with different name to remove ambiguity 
	num += 1
	print("PerSon : ", output) 
	
	toSpeak = gTTS(text = output, lang ='fr', slow = False) 
	# saving the audio file given by google text to speech 
	file = str(num)+".mp3" 
	toSpeak.save(file) 
	
	# playsound package is used to play the same file. 
	print(playsound.playsound(file, True)) 
	os.remove(file)

def index(request): 

	return render(request, 'money_id/home.html') 

def uploader(request):
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 

        if form.is_valid():
            form.save()
            return redirect('money_id:detect') 
    else:
        form = ImageForm() 

    return render(request,'money_id/upload.html', {'form' : form})


def detect_text(photo):

    billets = [5,10,20,50,100,200,500,1000,2000,5000,10000]
    devise = ['EURO','CFA']

    billet_detecte =' '
    devise_detecte=' '

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            try:
                if( int(text['DetectedText']) in billets and text['Confidence'] > 90):
                    billet_detecte = text['DetectedText']
            except ValueError:
                pass

            if(text['DetectedText']  in devise and text['Confidence'] > 90 ):
                if(text['DetectedText'] == 'CFA'):
                    devise_detecte = 'FRANCS '+text['DetectedText']

            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return len(textDetections), billet_detecte, devise_detecte 

def main(request):

    if request.method == 'GET': 
  
        images = Image.objects.last()

    photo=images.image_to_detect.url

    text_count, billet, devise=detect_text(photo)
    print("Text detected: " + str(text_count))

    assistant_speaks("On a detecté un billet de "+billet+" "+devise)

    return render(request,"money_id/detected.html",{'billet':billet, 'devise':devise})

def capture(request):
    vc = cv2.VideoCapture(0)

    rval, frame = vc.read()

    if rval:
        cv2.imwrite('./media/images/img.png', frame)

        im = Image(image_to_detect='images/img.png')
        im.save()

        return redirect('money_id:detect') 
        
    return render(request,"money_id/capture.html")