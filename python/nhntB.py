import ggwave
import os
import os.path
import re
import sys
import openai
from ctypes import *
import ggwave
import numpy as np
import sounddevice as sd
import time
import datetime
import pyttsx3
import pydub
import librosa
import yaml
import subprocess
from gtts import gTTS
import audio2numpy as a2n


TIMEOUT = 20
MAX_TOKENS=200
MAX_STRING=140

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = apikey
   
stop = ["."]

promptArray = ["Who is a human?\n"]
prepromptSend = "Ask a question about the following statement from the perspective of a houseplant: "
prepromptReceive = "Answer this question from the perspective of a houseplant who hates humans: "

def arrayToString(input):
    output = ""
    for x in input:
        output = output + x
    return output 

def parseMsg(inputText, config):
    partRegex = re.compile(r'(\d)[:](\d)[:](\d)[/](\d)') 
    regexOut = partRegex.search(inputText)

    if regexOut == None:
        print("no message marker")
        return 0, 0, 1, 1, inputText
    else:
        # extract the message number and and number of parts 
        msgCount = regexOut.group(1)
        recipient = regexOut.group(2)
        msgNumber = regexOut.group(3)
        msgParts = regexOut.group(4)
        return msgCount, recipient, msgNumber, msgParts, messageText
 
def py_error_handler(filename, line, function, err, fmt):
    pass

def alsaErrorHandling():
    # From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
    # $ grep -rn snd_lib_error_handler_t
    # include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
    # Define our error handler type
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p) 
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)

def speak(config, inputText):
    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    
    # print(inputText)
    # print(len(inputText))

    # get the recipient number from config file
    recipient =  re.sub('\D', '', config.get('pair_name'))

    toSend = []
    if len(inputText) > MAX_STRING:
        i = 0
        while i < len(inputText):
            i += MAX_STRING
            toSend.append(inputText[i - MAX_STRING:i])
    else:
        toSend.append(inputText)


    # print(toSend) 
    
    stream = sd.OutputStream(
        dtype='float32', 
        device=config.get('output_device'), 
        channels=1, 
        samplerate=48000)
    
    stream.start()
    
    # send the array of strings
    for i in range(0, len(toSend)):

        header = str(recipient) + ":" + str(i + 1) + "/" + str(len(toSend)) + ": "
        
        stringToSend = header + toSend[i]
        
        waveform = ggwave.encode(stringToSend, protocolId = config.get('protocol'), volume = config.get('volume'))

        print("transmitting text... " + toSend[i])

        # write to the pyaudio stream
        towrite = np.frombuffer(waveform, 'float32')

        stream.write(towrite)

    # close the audio stream
    stream.stop()
    stream.close()

def listen(msgCountIn, config):

    stream = sd.InputStream(
        dtype='float32', 
        device=config.get('input_device'), 
        channels=1, 
        samplerate=48000, 
        blocksize=1024)

    # start the sound decive input stream    
    stream.start()

    print('listening ... press Ctrl+C to stop')

    # ggwave instace
    instance = ggwave.init()

    # initialize function to expect three parts
    msgParts = 3
    msgNumber = 1

    # array to store the messages 
    msgs = []

    # keep the start time for timeout
    startTime = time.time()

    try:
        # until we've received all parts, call this function
        while msgNumber < msgParts:

            # get data from the stream
            data, overflow = stream.read(1024)

            # convert from numpy to bytes  
            databytes = bytes(data[:, 0])

            # decode the bytes
            res = ggwave.decode(instance, databytes)

            # increment the msg count if the timeout happens
            if time.time() - startTime > TIMEOUT:
                print("exceeded timeout, incrementing count")
                msgCountOut = msgCountIn + 1
                break

            # if decode is successful
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    print('received text: ' + res.decode("utf-8"))

                    # get the message number / parts and contents
                    msgCountOut, recipient, msgNumber, msgParts, outputTextClean = parseMsg(outputText, config)

                    print(msgCountOut, recipient, msgNumber, msgParts, outputTextClean)

                    # append the cleaned output text to the message array
                    msgs.append(outputTextClean)

                except KeyboardInterrupt:
                    pass

    except KeyboardInterrupt:
        pass
    
    # successful decode
    ggwave.free(instance)
    stream.stop()
    stream.close()

    # concatenate all the message parts into a single string
    return msgCountOut, recipient, arrayToString(msgs)

def queryModel(config, currentResponses):
    
    responses = []

    responses = responses + currentResponses

    preprompt = config.get('pre_prompt')
    model = config.get('model')

    prompt = preprompt + responses[-1] + "\n"
    
    print(prompt)
    
    # get the completion from model
    completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=MAX_TOKENS, stop=stop)

    responseString = completion.choices[0].text.strip()
    
    fullResponse = responseString + "\n"

    # add the formatted string to the list
    responses.append(fullResponse)
    
    return responses

def waitForStart(config):
    print("waiting for start command...")
    while True:
        if(listen(config) == "start"):
            break

def getConfig():
    username = subprocess.check_output(['whoami'], encoding='utf-8').strip()
    configName = "config/" + username + ".yaml"

    with open(configName, 'r') as file:
        config = yaml.safe_load(file)

    return config

# state machine:
#   query gpt3
#   send data over sound
#   listen
#   receive data over sound

# if "se" + str(recipient) == config.get("name"):
#     # strip the part numbers from the message
#     messageText = re.sub('\d[:]\d[:]\d[/]\d:', '', inputText)
#     return msgCount, recipient, msgNumber, msgParts, messageText
# else:
#     print("message not meant for me")
#     return 0, 0, 1, 3, inputText


# while msgCount < exchangeCount
#
#   if msgCount == sendCount
#       
#       sendGGWave()               
#
#       sendCount = countList.pop()
#
#   else
#
#       msgCount, recipient, msg = listen()
#   
#       if recipient == me
#       
#           responses.append(msg)
#               
#
#
#
#
#




def main(): 
    # read the yaml file
    config = getConfig()

    # prevent alsa audio errors
    alsaErrorHandling()

    # create a log file
    os.makedirs("logs/", exist_ok = True)
    t = datetime.datetime.now()
    filename = "logs/" + t.strftime("%m_%d_%H_%M_%S") + ".txt"
    f = open(filename, "w")
    
    # wait for start command
    waitForStart(config)

    # wait three second before starting
    time.sleep(3)

    # if we're in receive mode first then just start with a blank array
    responses = []

    # a flag to keep track
    if config.get('mode') == "send":
        sendReceive = True
    else:
        sendReceive = False

    # if send mode load a question from the prompt
    if config.get('mode') == "send":

        time.sleep(1)
        responses = responses + promptArray 

        speak(config, responses[0])

        # write to logfile
        f.write(responses[0] + "\n")

        sendReceive = False

    # start the conversation
    for i in range(0, config.get('exchange_count')):
        
        if sendReceive == True:
            # get a response from the API
            responses = queryModel(config, responses)
            
            # give some time to improve cadence
            time.sleep(1)

            print("\nsending...\n")

            speak(config, responses[-1])

            # write to logfile
            f.write(responses[-1] + "\n")

            sendReceive = False

        elif sendReceive == False:
            print("\nreceiving...\n")

            outputText = listenTimeout(config)

            responses.append(outputText)

            # write to logfile
            f.write(outputText + "\n")
            
            sendReceive = True

    f.close()




if __name__ == "__main__":
    main()
