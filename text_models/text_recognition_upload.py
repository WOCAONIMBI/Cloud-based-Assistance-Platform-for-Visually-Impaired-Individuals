

import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime
import pyttsx3
import ffmpeg
import shutil
from pydub import AudioSegment
from flask import Flask, render_template, request, Response



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/captured'
app.config['AUDIO_FOLDER'] = 'static/audio'

pytesseract.pytesseract.tesseract_cmd = "F:\\tesseract\\tesseract.exe"
def perform_ocr_and_audio(image_path):
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def adjust_brightness_contrast(image, alpha=1.0, beta=0):
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted

    # Increase brightness and contrast of the image
    img_adjusted = adjust_brightness_contrast(img, alpha=1.5, beta=20)

    # Save the adjusted image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    adjusted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'adjusted_image_{timestamp}.jpg')

    cv2.imwrite(adjusted_image_path, cv2.cvtColor(img_adjusted, cv2.COLOR_RGB2BGR))

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img_adjusted)

    # Print the extracted text
    print(text)

    # Convert the extracted text to speech
    


    # Save the audio file
        

   

    # Convert recognized text to speech using gTTS
    adjusted_img_path = adjusted_image_path
    description_text=text
    
    
    audio_path = os.path.join('static/audio', f'description_{timestamp}.mp3')
    engine = pyttsx3.init()
    wav_filename = 'output.wav'
    engine.save_to_file(description_text, wav_filename)
    engine.runAndWait()
    mp3_filename =audio_path
    audio = AudioSegment.from_wav(wav_filename)
    mp3_filenamepath=os.path.basename(audio_path)
    audio.export(mp3_filenamepath, format='mp3')

    print(f'音频文件已保存为: {mp3_filenamepath}')
    del audio
    
    shutil.copyfile(mp3_filenamepath,str(1)+mp3_filenamepath)
    destination_folder='static/audio'
    if not os.path.exists(destination_folder):
        try:
# 如果不存在，则创建目标目录
            os.makedirs(destination_folder)
            print(f'目录已创建: {destination_folder}')
        except Exception as e:
            print(f'创建目录时发生错误: {e}')
        else:
            print(f'目录已存在: {destination_folder}')

    shutil.move(str(1)+mp3_filenamepath,'static/audio/'+mp3_filenamepath)
    print(f"Audio description saved at: {audio_path}")

    img_filename = os.path.basename(adjusted_img_path)
    audio_filename = os.path.basename(audio_path)
    


    return text, audio_path, adjusted_image_path, timestamp


