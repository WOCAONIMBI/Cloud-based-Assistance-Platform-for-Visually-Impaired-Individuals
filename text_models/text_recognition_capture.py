
import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime
import pyttsx3
import ffmpeg
import shutil
from pydub import AudioSegment
pytesseract.pytesseract.tesseract_cmd = "F:\\tesseract\\tesseract.exe"


def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    # Apply brightness and contrast adjustment
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted_img

def perform_text_capture():
    cap = cv2.VideoCapture(0)

    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the original image
            cv2.imwrite('static/captured/original_image.jpg', frame)

            # Adjust brightness and contrast
            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)
            cv2.imwrite('static/captured/adjusted_image.jpg', adjusted_frame)

            cap.release()
            cv2.destroyAllWindows()
            print("Images captured and saved")

            break

        elif key == 27:  # Press 'Esc' to exit
            break

    img_path = 'static/captured/adjusted_image.jpg'
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        text_output = pytesseract.image_to_string(img)
        print("Recognized text:")
        print(text_output)

        if text_output.strip():  # Check if the recognized text is not empty

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Convert recognized text to speech using gTTS
            adjusted_img_path = 'static/captured/adjusted_image.jpg'
            description_text=text_output
            
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
            

            return text_output, img_path, audio_path, timestamp
        else:
            return "Error: No text detected in the captured image", "", "",""
    else:
        return "Error: Adjusted image not found", "", ""



