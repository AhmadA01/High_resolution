# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:24:35 2020

@author: ahmed
"""
from flask import Flask, request, jsonify, render_templete
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
from telegram import File
import numpy as np
import pytube
import moviepy.editor as mp

app=Flask(__name__)

def get_music(link):
    url = link
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    path= video.download()
    clip = mp.VideoFileClip(path)
    clip.audio.write_audiofile(path[:-4]+'.mp3')
    return path[:-4]+'.mp3'


def get_link(update,context):
    try:
        print(update)
        link = update.message.text
        update.message.reply_text("Please wait 😊")
        update.message.reply_text("Your music will be ready in 20 sec")
        music = get_music(link)
        context.bot.send_audio(update.effective_chat.id, audio=open(music, 'rb')) 
    except Exception as e:
        print(str(e))

def start(update, context):
    print(update)
    update.message.reply_text("Hi "+ str(update['message']['chat']['first_name'])+" 😊")
    update.message.reply_text("Enter Youtube link to download music")
    
def main():
    updater = Updater('1223251794:AAG7BucXqNiDoasMCGh1hribnUJUtid31O8', use_context=True)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, get_link))
    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    main()
    return render_templete('index.html')

if __name__=='__main__':
    app.run(debug=True)
