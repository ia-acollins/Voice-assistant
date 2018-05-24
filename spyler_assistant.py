#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""
save = open('/home/pi/AIY-voice-kit-python/src/examples/voice/spyler.txt', 'r')
import time
import RPi.GPIO as GPIO

for line in save:
    line = line.strip()
    line = line.replace('(','')
    line = line.replace(')','')
    datalist = line.split(', ')
    
print(datalist)

xd = 0
yo_duh = int(datalist[0])
ses = int(datalist[1])
sesupgrade = int(datalist[3])
yo_duhupgrade = int(datalist[2])
yocount = 0
sescount = 0

save.close()

import logging
import platform
import subprocess
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

def power_off_pi():
    aiy.audio.say('Good bye, human.')
    subprocess.call('sudo shutdown now', shell=True)


def reboot_pi():
    aiy.audio.say('Yo duh')
    subprocess.call('sudo reboot', shell=True)


def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    aiy.audio.say('Your IP address is %s' % ip_address.decode('utf-8'))


def process_event(assistant, event):
    global yo_duh
    global ses
    global xd
    global sesupgrade
    global yo_duhupgrade
    global yocount
    global sescount
    
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "Ok google" then speak, or press Ctrl+C to quit...')
            aiy.audio.say('oh hi')


    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('Yo sed:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power on':
            assistant.stop_conversation()
            time.sleep(20)
            power_off_pi()
        elif 'fbi' in text:
            assistant.stop_conversation()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
            aiy.audio.say('thanks for giving me that.')
        elif text == 'do you approve of cease puns' or text == 'do you approve of sea sponges':
            aiy.audio.say('No. is there even a way to kill more brain cells?')
            yo_duh += 0.6
        elif text == 'do you approve of egg puns':
            aiy.audio.say('No. is there even a way to kill more brain cells?')
            yo_duh += 0.6
        elif text == 'my name is':
            aiy.audio.say('Slim Shady')
        elif text == 'who is the master?':
            assistant.stop_conversation()
        elif text == 'fruit snacks':
            GPIO.output(26,GPIO.HIGH)
            GPIO.output(5,GPIO.HIGH)
            aiy.audio.say('trtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtrtr reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            ses += (1 + sesupgrade)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(5,GPIO.LOW)
        elif text == 'your boys' or text == 'you are a boys':
            aiy.audio.say('ack ack ack ack ack ack ack ack ack ack cici cici cici self destruct in 10 9 8 7 6 5 4 3 2 1')
            assistant.stop_conversation()
            #power_off_pi()
        elif text == "who's on trial":
            GPIO.output(26,GPIO.HIGH)
            GPIO.output(5,GPIO.HIGH)
            aiy.audio.say("THREE YEAR OLD KENNETH MAYBURY")
            GPIO.output(26,GPIO.LOW)
            GPIO.output(5,GPIO.LOW)
            xd = 9001
            print(xd)
        elif text == "what for" and xd == 9001:
            aiy.audio.say("According to the plaintiff, there was an ambulance pulled over. Mr. Maybury claims you, Miss Maghee, pulled up to the ambulance, started screaming at the ambulance person, and threw a soda through the ambulance window. some people just let this go, some do not.")
            xd = 0
            yo_duh += (1 + yo_duhupgrade)
            ses += (4 + sesupgrade)
        elif text == 'yoda' or text == 'yo duh' or text == 'yo da':
            yo_duh += (1 + yo_duhupgrade)
            aiy.audio.say("gained %s yo da points" % str(1 + yo_duhupgrade))
            yocount += 1
            
        elif text == 'you a story' or text == 'your story' or text == "you're a story":
            if ses >= 1 and yo_duhupgrade == 0:
                yo_duh += 2
                ses = ses - 1
                aiy.audio.say("gained two yo da points but lost one cease point")
            if yo_duhupgrade >= 1:
                if yocount >= 5:
                    george = yo_duh
                    yo_duh += (2 * (yo_duhupgrade + yocount - 5))
                    yocount = 0
                    aiy.audio.say('gained %s yo da points' % str(yo_duh - george))
                    
            
        elif text == 'best friend cease' or text == 'best friend CC' or text == 'best friend cici' or text == 'best friend cece':
            george = ses
            ses += (1 + sesupgrade)###################################
            aiy.audio.say("gained %s cease points" % str(ses - george))###################
            sescount += 1
            
        elif text == 'best fiend cece' or text == 'best fiend CC' or text == 'best fiend cease' or text == 'best fiend cici':
            if yo_duh >= 1 and sesupgrade == 0:
                ses += 2
                yo_duh = yo_duh - 1
                aiy.audio.say("gained two cease points but lost one yo da point.")
            if sesupgrade >= 1:
                if sescount >= 5:
                    george = ses
                    ses += (2 * (sesupgrade + sescount - 5))
                    sescount = 0
                    aiy.audio.say('gained %s cease points' % str(ses - george))
                    
            aiy.audio.say("gained two cease points but lost one yo da point.")
        elif text == 'why do you have 2 voices':
            aiy.audio.say("Andrew liked the other voice starting to talk. it makes it funnier")
        elif text == 'cease points' or text == '6 points' or text == "CC's points" or text == 'how many cease points' or text == 'what are your cease points' or text == 'how many cease points do you have':
            ses = int(ses)
            ses = str(ses)
            aiy.audio.say('I have %s cease points.' % (ses))
            ses = int(ses)
        elif text == 'yoda points' or text == 'yo da points' or text == 'how many yoda points' or text == 'what are your yoda points' or text == 'how many yoda points do you have':
            yo_duh = int(yo_duh)
            yo_duh = str(yo_duh)
            aiy.audio.say('I have %s yo da points.' % (yo_duh))
            yo_duh = int(yo_duh)
        elif text == "what's the weather":
            aiy.audio.say('you are face ell oh ell ooooooooooooooooooooooo')
            ses += 0.5
        elif text == "why are all sea creatures named after fish":
            if ses >= 2 and yo_duhupgrade < 2:
                yo_duh += 3
                ses = ses - 2
                aiy.audio.say('look, theres a manatee fish')
            if yo_duhupgrade >= 2:
                if yocount >= 10:
                    george = yo_duh
                    yo_duh += (4 * (sesupgrade + sescount - 5))
                    sescount = 0
                    aiy.audio.say('gained %s yo da points' % str(yo_duh - george))
                    
        elif text == "everybody play I spy" or text == "let's all play i spy":
            if yo_duh >= 2 and sesupgrade < 2:
                ses += 3
                yo_duh = yo_duh - 2
                aiy.audio.say('i spy you spy lets all play i spy')
            if sesupgrade >= 2:
                if sescount >= 10:
                    george = ses
                    ses += (4 * (sesupgrade + sescount - 5))
                    sescount = 0
                    aiy.audio.say('gained %s cease points' % str(ses - george))
                    
        elif text == "what's in the woods":
            xd = 79
            aiy.audio.say('theres lots of things in the woods. trees, rocks, animals...')
        elif text == "what animals are in the woods" or text == "what animals live in the woods" and xd == 79:
            xd = 80
            aiy.audio.say('oh. theres deer, rabbits, maybe raccoons...')
        elif text == 'what carnivores are in the woods' or text == 'what carnivores live in the woods' and xd == 80:
            aiy.audio.say('wow. good vocabulary word. well, i dont really know.')
            xd = 81
        elif text == 'what carnivore ate the deer' or text == 'what carnivore eat the deer' and xd == 81:
            aiy.audio.say('ACK ACK ACK Ljdosajifdadjsfoasdifjlasdfkjaosdfjoasfija')
            xd = 0
            yo_duh += (3 + yo_duhupgrade)
            ses += 3 + sesupgrade

        #Follow up statements

        elif text == 'you stupid':
            if xd == 777 and yo_duh >= 1:
                aiy.audio.say('yeet yeetyeesaoweo yehey aosdfjaosifjioew kayaika ksdofas oaei sdf owaejif oassdfalkfj oai owjf lasdfj oewjk ksdajklfjsaklf las jjfaj ofaeow fjja jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
                yo_duh = yo_duh - 1
            else:
                aiy.audio.say('i dunno how to heel with that')

        # Upgrades
        elif text == 'upgrade CC' or text == 'upgrade cease' or text == 'upgrade Cece':
            george = sesupgrade
            if ses >= 50 and sesupgrade == 0:
                sesupgrade += 1
                ses = ses - 50
            if ses >= 125 and sesupgrade == 1:
                sesupgrade += 1
                ses = ses - 125
            if ses >= 180 and sesupgrade == 2:
                sesupgrade += 1
                ses = ses - 180
            if ses >= 225 and sesupgrade == 3:
                sesupgrade += 1
                ses = ses - 225
            if ses >= 285 and sesupgrade == 4:
                sesupgrade += 1
                ses = ses - 285
            if ses >= 345 and sesupgrade == 5:
                sesupgrade += 1
                ses = ses - 345
            if ses >= 420 and sesupgrade == 6:
                sesupgrade += 1
                ses = ses - 420
            if ses >= 480 and sesupgrade == 7:
                sesupgrade += 1
                ses = ses - 480
            if ses >= 540 and sesupgrade == 8:
                sesupgrade += 1
                ses = ses - 540
            if ses >= 630 and sesupgrade == 9:
                sesupgrade += 1
                ses = ses - 630
            if ses >= 720 and sesupgrade == 10:
                sesupgrade += 1
                ses = ses - 720
            if ses >= 911 and sesupgrade == 11:
                sesupgrade += 1
                ses = ses - 911
            if ses >= 1337 and sesupgrade >= 12:
                sesupgrade += 1
                ses = ses - 1337
            if sesupgrade > george:
                aiy.audio.say('Conglaturation!! successfully upgraded to cease level %s' % str(sesupgrade))


        elif text == 'upgrade yoda' or text == 'upgrade yo da' or text == 'upgrade yo duh':
            george = yo_duhupgrade
            if yo_duh >= 50 and yo_duhupgrade == 0:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 50
            if yo_duh >= 125 and yo_duhupgrade == 1:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 125
            if yo_duh >= 180 and yo_duhupgrade == 2:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 180
            if yo_duh >= 225 and yo_duhupgrade == 3:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 225
            if yo_duh >= 285 and yo_duhupgrade == 4:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 285
            if yo_duh >= 345 and yo_duhupgrade == 5:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 345
            if yo_duh >= 420 and yo_duhupgrade == 6:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 420
            if yo_duh >= 480 and yo_duhupgrade == 7:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 480
            if yo_duh >= 540 and yo_duhupgrade == 8:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 540
            if yo_duh >= 630 and yo_duhupgrade == 9:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 630
            if yo_duh >= 720 and yo_duhupgrade == 10:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 720
            if yo_duh >= 911 and yo_duhupgrade == 11:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 911
            if yo_duh >= 1337 and yo_duhupgrade >= 12:
                yo_duhupgrade += 1
                yo_duh = yo_duh - 1337
            if yo_duhupgrade > george:
                aiy.audio.say('Conglaturation!! successfully upgraded to yo da level %s' % str(yo_duhupgrade))

        elif text == 'cease level' or text == 'CC level' or text == 'Cece level':
            aiy.audio.say(str(sesupgrade))
        elif text == 'yo da level' or text == 'Yoda level':
            aiy.audio.say(str(yo_duhupgrade))
        #ses store
            
        
        elif text == 'tron':
            if ses >= 1:
                aiy.audio.say('more like gewgell trons late')
                ses = ses - 1
            else:
                aiy.audio.say('loll your poor. you cant afford a 1 point command.')
        elif text == 'tron cost':
            aiy.audio.say('1 cease point')

        elif text == 'shrek':
            if ses >= 3:
                aiy.audio.say('somebody once told me the world was gonna roll me, use shrekfull and 50 of each in the epic store to hear the full song.')
                ses = ses - 3
            else:
                aiy.audio.say('really? your to poor to afford the demo version? 3 cease points.')
        elif text == 'shrek cost':
            aiy.audio.say('3 cease points')

        elif text == 'rarted wall' or text == 'rotted wall':
            if ses >= 7:
                aiy.audio.say('chchchchchchchchchchchchchchchchchchchchchchch REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE your gonna break the light you have to use the other ball now basketball is safer dont you dare play krusty crew')
                ses = ses - 7
            else:
                aiy.audio.say('try again when you have 7 cease points')
        elif text == 'rarted wall cost' or text == 'rotted wall cost':
            aiy.audio.say('7 cease points')
            
        #yo duh store
        elif text == "sam logic":
            if yo_duh >= 1.5:
                aiy.audio.say("why am i wearing a hoodie?")
                yo_duh = yo_duh - 1.5
            else:
                aiy.audio.say("u cant afford that ex dee")
        elif text == 'sam logic cost':
            aiy.audio.say('1 point 5 yo da points')

        elif text == 'why was minecraft invented':
            if yo_duh >= 10:
                aiy.audio.say("Minecraft, an indie video game released by Mojang in 2010, was created with the sole intention of teaching children abbreviations. My dad invented minecraft, and he'll ban you if i want him to!")
                yo_duh = yo_duh - 10
            else:
                aiy.audio.say("your to poor you need ten yo da points to buy that loll chchchchchchcchchchchchchhchchchcchchhchchchc")
        elif text == 'why was minecraft invented cost':
            aiy.audio.say('10 yo da points')

        elif text == 'what 9 + 10':
            if yo_duh >= 21:
                aiy.audio.say('twunna won')
                xd = 777
                yo_duh = yo_duh - 21
            else:
                aiy.audio.say('sursley that was one of the most expensive ones 21 yo duh points loll')
        elif text == 'what 9 + 10 cost':
            aiy.audio.say('that ones expensive. 21 yo da points')

            
        #EPIC STOREEEE
        elif text == 'flea market montgomery':
            if yo_duh >= 7 and ses >= 7:
                aiy.audio.say('livin room. bedroom. dinette. yeah heah. ya can find em. at the market. im talkin bout flea market. montgomery. its just like a mini. mall.')
                yo_duh = yo_duh - 7
                ses = ses - 7
            else:
                aiy.audio.say("Try getting moar moneys")
                assistant.stop_conversation()
        elif text == 'flea market montgomery cost':
            aiy.audio.say('7 yo da points, 7 cease points')
            
        elif text == 'in the ocean':
            if yo_duh >= 2 and ses >= 5:
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(5,GPIO.HIGH)
                aiy.audio.say("i liek lerning A B cease in the oshee an. i liek lerning 12 threece in da oshee an.")
                yo_duh = yo_duh - 2
                ses = ses - 5
                GPIO.output(26,GPIO.LOW)
                GPIO.output(5,GPIO.LOW)
            else:
                aiy.audio.say("try getting more moneys. this costs 2 yo da points and 5 cease points.")
        elif text == 'in the ocean cost':
            aiy.audio.say('2 yo da points, 5 cease points')

        elif text == "what's your name" or text == 'what is your name':
            if yo_duh >= 13 and ses >= 13:
                #turn lights on
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(5,GPIO.HIGH)
                aiy.audio.say("I am Spyler, creator of I spy, commander of cease, destructor of four silly knights, and conqueror of bright blue kazoo. I have not even achieved my final form. for that, you must reach 500 cease points and 500 yo da points. Farewell, and good luck. don't give up.")
                yo_duh = yo_duh - 13
                ses = ses - 13
                GPIO.output(26,GPIO.LOW)
                GPIO.output(5,GPIO.LOW)
            else:
                aiy.audio.say("You need 13 cease points and 13 yo da points to use this command.")
        elif text == "what's your name cost" or text == "what is your name cost":
            aiy.audio.say('13 yo da, 13 cease')

        elif text == 'crawling in my crawling in':
            if yo_duh >= 75 and ses >= 75 and sesupgrade >= 1:
                aiy.audio.set_tts_volume(aiy.audio.get_tts_volume()-50)
                aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/crawlcrawl.wav')
                aiy.audio.set_tts_volume(aiy.audio.get_tts_volume()+50)
            else:
                aiy.audio.say('NO')
        elif text == 'crawling in my crawling in cost':
            aiy.audio.say('75 yo da points, 75 cease points')

        elif text == 'sam music':
            if yo_duh >= 100 and ses >= 50:
                aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/ranbo.wav')
                yo_duh = yo_duh - 100
                ses = ses - 50
            else:
                aiy.audio.say('fail')
        elif text == 'sam music cost':
            aiy.audio.say('100 yo da 50 cease')

        elif text == 'crabs':
            if yo_duh >= 25 and ses >= 35:
                GPIO.output(26,GPIO.HIGH)
                GPIO.output(5,GPIO.HIGH)
                aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/oyheahmrkarbs.wav')
                GPIO.output(26,GPIO.LOW)
                GPIO.output(5,GPIO.LOW)
                yo_duh = yo_duh - 25
                ses = ses - 35
            else:
                aiy.audio.say('get more munny munny munny')
        elif text == 'crabs cost':
            aiy.audio.say('25 yo da 35 cease')
            
            
        elif text == 'destroy':
            if yo_duh >= 20 and ses >= 20:
                aiy.audio.set_tts_volume(aiy.audio.get_tts_volume()+25)
                aiy.audio.say('Ok Google, Power off')
                aiy.audio.set_tts_volume(aiy.audio.get_tts_volume()-25)
            else:
                aiy.audio.say('you need more munny to power off. more munee more munee more munee more munee more munee more munee more munee more munee more munee')
        elif text == 'destroy cost':
            aiy.audio.say('20 yo da points, 20 cease points')
            
                
        #saving progress
        elif text == 'save progress' or text == 'save':
            save = open('/home/pi/AIY-voice-kit-python/src/examples/voice/spyler.txt', 'w')
            line = (yo_duh,ses,yo_duhupgrade,sesupgrade)
            print(line,file=save)
            aiy.audio.say('progress saved')
            save.close()
        #special function
        elif text == 'evolve':
            if ses >= 500 and yo_duh >= 500:
                aiy.audio.say('conglaturation. you have completed a great game. and prooved the just ice of our culture. now go and rest are heroes!')
            else:
                aiy.audio.say('cant evolve yet')

        elif text == "where's cease":
            GPIO.output(26,GPIO.HIGH)
            aiy.audio.say('cici? i mean cease? cease who? I do not know nor did I kill anyone named cease or Cece.')
            GPIO.output(26,GPIO.LOW)
            
        elif text == 'playlist':
            aiy.audio.say('Coerced Coexistence by In Flames')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/CC.wav')
            aiy.audio.say('Street of Dreams by Guns n roses')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/SoD.wav')
            aiy.audio.say('Pounder by Nuclear assault')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/P.wav')
            aiy.audio.say('Across the Line by Linkin Park')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/AtL.wav')
            aiy.audio.say('The good left undone by rise against')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/tGLU.wav')
            aiy.audio.say('Fury of the Storm by Dragonforce')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/FotS.wav')
            aiy.audio.say('Kings and Queens by Aerosmith')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/KaQ.wav')
            aiy.audio.say('The ghost of you by some cringy emo band')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/tGoY.wav')
            aiy.audio.say('End over End by the Foo Fighters')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/EoE.wav')
            aiy.audio.say('The End of Heartache by Killswitch engage')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/tEoH.wav')
            aiy.audio.say('Right where it belongs by Nine inch nails')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/RWiB.wav')
            aiy.audio.say('Finally, the last song: The void by parkway drive')
            aiy.audio.play_wave('/home/pi/AIY-voice-kit-python/src/examples/voice/playlist/tV.wav')
            aiy.audio.say('thank you for listening. now time for my music. DO DO. DO DO DO DO. DO DO DO DO. DO DO DO DO DO. DO DO DO DO DO DO DO DO DO DO DO')
        
            
            
        
        
            
        
        
        
        
        
        
        

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        aiy.audio.say('yo da')
        status_ui.status('thinking')
        

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        aiy.audio.say('anything else?')
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)

    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()
