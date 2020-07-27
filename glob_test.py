import glob
import ffmpeg
import speech_recognition as sr
import re
import os
import math
import csv
###Hyper Paramaters###
recog_audio_path = "./aps-smp.wav"


l_ = glob.glob('./**/id*',recursive=True)

l_name_without_ext=[]
for topPath in l_:
  l=glob.glob(topPath+'/**/*.mp4',recursive=True)

  #print(l)
  # ['temp/[x].txt', 'temp/1.txt', 'temp/123.txt']

  l_name_without_ext.extend(['.'+path.split('.')[-2] for path in l])

print(l)
print(l_name_without_ext)



totalsize = len(l_name_without_ext)
ketasu='0'+str(math.log10(totalsize)//1+1).split('.')[0]

#CSVファイルの用意
with open('./content.csv', mode='w') as csvfile:
  csvwriter = csv.writer(csvfile)
  for i, input_name in enumerate(l_name_without_ext,1):
    
    if (os.path.exists(input_name + '.txt')):
      print(input_name+'.mp4 already transcribed.')
      continue

    #動画の読み込み
    stream = ffmpeg.input(input_name+'.mp4')
    stream = ffmpeg.output(stream,'aps-smp.wav')
    stream = ffmpeg.overwrite_output(stream)
    stream.global_args('-loglevel', 'quiet').run()

    AUDIO_FILE = recog_audio_path

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    try:
      result=r.recognize_google(audio, language='en-US')

      #テキストの保存
      with open(input_name + '.txt', mode='w') as f:
          f.write(result)

      csvwriter.writerow([input_name,'success',result])
      #print(input_name + ": \"" + result + "\n\n")
    except sr.UnknownValueError:
      print(input_name+" : Google Speech Recognition could not understand audio")
      csvwriter.writerow([input_name,'UnknownValueError'])
    except sr.RequestError as e:
      print(input_name + " : Could not request results from Google Speech Recognition service; {0}".format(e))
      csvwriter.writerow([input_name,'RequestError'])
    
    print("{i_:{ketasu_}d}/{totalsize_:{ketasu_}d} Finished".format(i_=i,totalsize_=totalsize,ketasu_=ketasu))
    if i==1:break
    if (os.path.exists(recog_audio_path)):
      os.remove(recog_audio_path)
