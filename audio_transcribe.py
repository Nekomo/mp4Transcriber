import os
import ffmpeg
import speech_recognition as sr

###Hyper Paramaters###
recog_audio_path = "./aps-smp.wav"
input_name='00121'

#動画の読み込み
stream = ffmpeg.input(input_name+'.mp4')
stream = ffmpeg.output(stream,'aps-smp.wav')
stream = ffmpeg.overwrite_output(stream)
stream.run()

AUDIO_FILE = recog_audio_path

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

result=r.recognize_google(audio, language='en-US')

try:
    #print(AUDIO_FILE + ": \"" + result + "\n\n")
except sr.UnknownValueError:
    print("AUDIO_FILE:Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#テキストの保存
with open(input_name + '.txt', mode='w') as f:
    f.write(result)

os.remove(recog_audio_path)