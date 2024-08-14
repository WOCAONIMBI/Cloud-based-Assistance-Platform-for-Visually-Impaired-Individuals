

from gtts import gTTS
import torch
from PIL import Image
import os
from datetime import datetime
import pyttsx3
import ffmpeg
import shutil
from pydub import AudioSegment

from flask import Flask

app = Flask(__name__)

app.config['AUDIO_FOLDER'] = 'static/audio'


def detect_objects(image_path):
    # Load the YOLOv5 model
    model = torch.hub.load('F:/huaweiOBS/WeSee-main/yolov5', 'custom', './yolov5s.pt', source='local')
   
    
    # Load an image
    adjusted_frame = Image.open(image_path)
    adjusted_img_path = image_path
    
    # Perform detection
    results = model(adjusted_frame)

                  
    # Get detected objects and generate description
    detected_objects = results.pandas().xyxy[0]['name'].unique()
    if detected_objects.size > 0:
        objects_list = ", ".join(detected_objects)
        description_text = f"The objects detected in the image are: {objects_list}."
    else:
        description_text = "No objects detected."
    # Print the description

    # Generate audio from the description text
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
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
    
    return description_text, audio_path, timestamp
