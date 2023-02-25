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


TIMEOUT=20
MAX_TOKENS=200
MAX_STRING=140

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = apikey

# alien aesthetics reading
# modelReceive = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"

# environmental literature
# modelReceive = "davinci:ft-parsons-school-of-design-2023-01-20-01-37-01"

# latour
# modelReceive = "davinci:ft-parsons-school-of-design-2023-02-06-15-16-50"

# generic models
modelReceive = "text-davinci-003"
modelSend = "text-davinci-003"
   
stop = ["."]

promptArray = ["Who is a human?\n"]
prepromptSend = "Ask a question about the following statement from the perspective of a houseplant: "
prepromptReceive = "Answer this question from the perspective of a houseplant who hates humans: "

def arrayToString(input):
    output = ""
    for x in input:
        output = output + x
    return output 

def getMessagePart(inputText, config):
    partRegex = re.compile(r'(\d)[:](\d)[/](\d)') 
    regexOut = partRegex.search(inputText)

    if regexOut == None:
        print("no message marker")
        return 0, 1, 1, inputText
    else:
        # extract the message number and and number of parts 
        recipient = regexOut.group(1)
        msgNumber = regexOut.group(2)
        msgParts = regexOut.group(3)

        if "se" + str(recipient) == config.get("name"):
            # strip the part numbers from the message
            messageText = re.sub('\d[:]\d[/]\d:', '', inputText)
            return recipient, msgNumber, msgParts, messageText
        else:
            print("message not meant for me")
            return 0, 1, 3, inputText
 

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

def sendGGWave(config, inputText):
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

def sendGGWaveUT(config, inputText):

    os.system("touch hello.mp3")

    # get the recipient number from config file
    recipient =  re.sub('\D', '', config.get('pair_name'))

    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    
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
        channels=2, 
        samplerate=48000)
    
    stream.start()
    
    # send the array of strings
    for i in range(0, len(toSend)):

        header = str(recipient) + ":" + str(i + 1) + "/" + str(len(toSend)) + ": "
        print(header)
        
        stringToSend = header + toSend[i]
        
        # generate audio waveform for encoded text
        ggwaveWaveform = ggwave.encode(stringToSend, protocolId = config.get('protocol'), volume = 50) #config.get('volume'))
    
        ggwaveOut = np.frombuffer(ggwaveWaveform, 'float32')

        print("gtts")
        print(time.perf_counter())

        # GTTS
        # ttsWaveform = gTTS(stringToSend, tld='co.in', slow=True)
        # ttsWaveform.save('hello.mp3')
        # cmd = "ffmpeg -hide_banner -loglevel error -i hello.mp3 -ar 40000 hello48k.mp3"
        # os.system(cmd)
        # ttsOut, sampleRate = a2n.open_audio('hello48k.mp3')
        # # ttsOut, sampleRate = a2n.open_audio('hello.mp3')
        # os.system("rm *.mp3")

        # PYTTSX3
        engine = pyttsx3.init()
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 0.8)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 50)
        engine.runAndWait()
        print(engine.getProperty('rate'))
        print(engine.getProperty('volume'))
        engine.save_to_file(stringToSend, "hello.mp3")
        engine.runAndWait()
        # sampleRate, ttsOut = mp3tonp("hello.mp3")
        ttsOut, sampleRate = a2n.open_audio('hello.mp3')
        print(sampleRate)
        
        os.system("rm *.mp3")

        ttsOut = ttsOut.astype('float32')


        # print("librosa")
        # print(time.perf_counter())
        # ttsOut = librosa.effects.pitch_shift(ttsOut, sr=48000, n_steps=config.get('pitch'))
        # print(time.perf_counter())
        

        # reformat
        ttsOut32 = np.frombuffer(ttsOut, 'float32')

        print("array size")
        print(time.perf_counter())
        # make sure they're the same length
        print(len(ttsOut32), len(ggwaveOut))
        if len(ttsOut32) > len(ggwaveOut):
            ttsOut32 = ttsOut32[0:len(ggwaveOut)]
        else:
            zeroArray = np.zeros(len(ggwaveOut) - len(ttsOut32), dtype=np.float32)
            ttsOut32 = np.append(ttsOut32, zeroArray)
        
        print(time.perf_counter())
        
        # format the data into an array appropriately
        finalOutput = [ttsOut32, ggwaveOut]
        aa = np.array(finalOutput)
        a = np.ascontiguousarray(aa.T)
        print(a.shape)
        print("transmitting text... " + toSend[i])

        # write to the pyaudio stream
        stream.write(a)

    # close the audio stream
    stream.stop()
    stream.close()

def receiveGGWave(config):
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

    try:
        # until we've received all parts, call this function
        while msgNumber < msgParts:

            # get data from the stream
            data, overflow = stream.read(1024)

            # convert from numpy to bytes  
            databytes = bytes(data[:, 0])

            # decode the bytes
            res = ggwave.decode(instance, databytes)

            # if decode is successful
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    print('received text: ' + res.decode("utf-8"))

                    # get the message number / parts and contents
                    recipient, msgNumber, msgParts, outputTextClean = getMessagePart(outputText, config)

                    print(recipient, msgNumber, msgParts, outputTextClean)

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
    return arrayToString(msgs)

def receiveGGWaveTimeout(config):
    timeout = 40

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

            if time.time() - startTime > timeout:
                print("exceeded timeout")
                break

            # if decode is successful
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    print('received text: ' + res.decode("utf-8"))

                    # get the message number / parts and contents
                    recipient, msgNumber, msgParts, outputTextClean = getMessagePart(outputText, config)

                    print(recipient, msgNumber, msgParts, outputTextClean)

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
    return arrayToString(msgs)


def converseLoop(n_exchange, starterPrompt):
    
    responses = []

    responses = responses + starterPrompt

    prompt = arrayToString(responses)

    print(prompt)

    # loop will iterate for duration of conversation
    for x in range(n_exchange):
        # print("\n---------------------------------------------------------\n")
        # switch between model and prompts
        if x % 2 == 0:
            model = modelB
            preprompt = "AI2: "
            stop = ["AI1: "]
        else:
            model = modelA
            preprompt = "AI1: "
            stop = ["AI2: ", "."]
        
        # add the empty preprompt with newline to the response list
        responses.append(preprompt + "\n")

        # turn the array of responses into a long string
        prompt = arrayToString(responses)

        # for modelB use the entire prompt, for modelA only the last two responses 
        if x % 2 == 0:
          prompt = arrayToString(responses)
        else:
          prompt = arrayToString(responses[-2] + responses[-1])

        # print("\n** " + model + ": " + prompt + " **\n")
        
        # get the completion from model
        completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=100, stop=stop)

        responseString = completion.choices[0].text.strip()
        
        # add the preprompt to the response and make sure it has a new line 
        fullResponse = preprompt + responseString + "\n"

        # remove the empty preprompt from the list
        responses.pop()
        
        # add the formatted string to the list
        responses.append(fullResponse)
        
        print(fullResponse)

    return responses

def converseSingle(config, currentResponses):
    
    responses = []

    responses = responses + currentResponses

    # false means we're in receive mode and the plant is asking questions
    # if config.get('mode') == "send":
    #     preprompt = prepromptSend
    #     model = modelSend
    # else:
    #     preprompt = prepromptReceive
    #     model = modelReceive

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
        if(receiveGGWave(config) == "start"):
            break

def rxtxrxTest(config):
    outputText = receiveGGWave(config)
    print(outputText)
    sendGGWave("howdy I'm a raspberry pi")
    outputText = receiveGGWave(config)

def mp3tonp(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def getConfig():
    username = subprocess.check_output(['hostname'], encoding='utf-8').strip()
    configName = "config/" + username + ".yaml"

    with open(configName, 'r') as file:
        config = yaml.safe_load(file)

    return config

# state machine:
#   query gpt3
#   send data over sound
#   listen
#   receive data over sound

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

        if config.get('protocol') == 4:
            sendGGWaveUT(config, responses[0])
        else:
            sendGGWave(config, responses[0])

        # write to logfile
        f.write(responses[0] + "\n")

        sendReceive = False

    # start the conversation
    for i in range(0, config.get('exchange_count')):
        
        if sendReceive == True:
            # get a response from the API
            responses = converseSingle(config, responses)
            
            # give some time to improce cadence
            time.sleep(1)

            print("\nsending...\n")

            # send the most recent response
            if config.get('protocol') == 4:
                sendGGWaveUT(config, responses[-1])
            else:
                sendGGWave(config, responses[-1])

            # write to logfile
            f.write(responses[-1] + "\n")

            sendReceive = False

        elif sendReceive == False:
            print("\nreceiving...\n")

            outputText = receiveGGWaveTimeout(config)

            responses.append(outputText)

            # write to logfile
            f.write(outputText + "\n")
            
            sendReceive = True

    f.close()




if __name__ == "__main__":
    main()
