
from flask import Flask
import cv2
import torch
from gtts import gTTS
import os
from datetime import datetime
from PIL import Image
import numpy as np
import pyttsx3
import ffmpeg
import shutil
from pydub import AudioSegment
app = Flask(__name__, static_folder='static')


app.config['AUDIO_FOLDER'] = 'static/audio'



def adjust_brightness_contrast(img, alpha=1.0, beta=0):

    # Apply brightness and contrast adjustment
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    return adjusted_img

  
def perform_object_detection():
    cap = cv2.VideoCapture(0)
    
    # Load a pre-trained model. Here, we're assuming YOLOv5; adjust as needed.
    #model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    #model=torch.load('F:\\huaweiOBS\\WeSee-main\\yolov5\\yolov5s.pt')
    #model = torch.hub.load('F:/huaweiOBS/WeSee-main/yolov5', 'custom', path='./yolov5s.pt',source='local')
    #model = torch.hub.load('.', 'custom',r'yolov5s.pt',source='local')
    #model=torch.load('./yolov5s.pt',map_location=torch.device('cpu'))['model'].float
    model = torch.hub.load('F:/huaweiOBS/WeSee-main/yolov5', 'custom', './yolov5s.pt', source='local')
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            img_path = 'static/captured/captured_image.jpg'
            cv2.imwrite(img_path, frame)
            print("Image captured and saved.")

            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)

            adjusted_img_path = 'static/captured/adjusted_captured_image.jpg'

            cv2.imwrite(adjusted_img_path, adjusted_frame)
            print("Adjusted Image captured and saved.")

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

            cap.release()
            cv2.destroyAllWindows()
            break

        elif key == 27:  # Press 'Esc' to exit
            cap.release()
            cv2.destroyAllWindows()
            break
        
    return description_text, img_filename, audio_filename


