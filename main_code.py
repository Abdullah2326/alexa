from gtts import gTTS
import speech_recognition as sr
import datetime
import requests
import os
import webbrowser
import pygame
import pyautogui
import paperclip
import time
import pytz

# pip install gtts speachrecognition pygame pyaudio pyautogui paperclip setuptools requests pytz



def speak(text):    # speaks the text thats entered
    tts = gTTS(text)
    tts.save("audio.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("audio.mp3")  



def audio(timeout = 10):   # converts the user speach into text
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2 # Time of silence to decide speech has ended
    recognizer.non_speaking_duration = 0.5 # Extra silence kept before and after speech
    recognizer.dynamic_energy_ratio = 1.1 # Makes the mic less sensitive to background noise
    while True:
        with sr.Microphone() as source:
            print("Listening...")
 
            recognizer.adjust_for_ambient_noise(source,duration=1) #calibrates the mic accoording to your suroundings
            audio_data = recognizer.listen(source,timeout=timeout,phrase_time_limit=None)

        try:
            command = recognizer.recognize_google(audio_data)   
            print("You said: ",command) # this prints the command you have said
            return (command.lower())
        
        except sr.WaitTimeoutError:
            print("speach not detected")
            continue

        # except TimeoutError:
        #     continue

        except sr.UnknownValueError:
            print("\033[31mSorry couldn't understand, speak again\033[0m")
            speak("sorry couldn't understand, speak again")
            continue



def genral_chat(question):
    
    API_KEY_FOR_GEMINI = "YOUR_API"
    url = "https://api.a4f.co/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY_FOR_GEMINI}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "provider-5/gemini-3-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a voice assistant AI named Alexa. "
                    "Give short, precise, and accurate answers only. "
                    "Maximum 3 lines normally. "
                    "If explanation is required, maximum 6 lines. "
                    "Do NOT add greetings, commentary, or extra words. "
                    "Only give the direct answer."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.3,     # Lower = more accurate, less creative
        "max_tokens": 120       # Limits answer length
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        # Print status for debugging (you can remove later)
        # print("Status Code:", response.status_code)

        data = response.json()

        if response.status_code == 200 and "choices" in data:
            answer = data["choices"][0]["message"]["content"].strip()
            speak(answer)
            print(f"\033[34mAI's Response: {answer}\033[0m")
        else:
            return (f"\033[31mAPI Error: {data}\033[0m")

    except requests.exceptions.RequestException as e:
        return (f"\033[31mRequest Failed: {e} \033[0m")



def scroll_down(): # this scrolls the page down
    pyautogui.press("pagedown")



def scroll_up(): # this scrolls the page up
    pyautogui.press("pageup")
   


def click_image(image_location,confidence = 0.7):
    location = pyautogui.locateCenterOnScreen(image_location,confidence) #finds the center of the icon in the image 
    if location:
        return location
    else:
        print("Image not found")
        return False
    


def date():
    raw_date = datetime.datetime.now(tz=pytz.timezone("Asia/Karachi"))
    date = raw_date.strftime("%A %d %B ,%Y")
    print(f"The date is : {date}")
    speak(date)



def current_time():
    current_time = datetime.datetime.now(tz=pytz.timezone("Asia/Karachi"))
    time = current_time.strftime("%I : %M %p")
    print(f"The time is : {time}")
    speak(time)



def tab(number_of_presses): # press tab button as many times as specified
    for _ in range (number_of_presses): # _ shows a unused variable or whenthe loop variable is not needed
        pyautogui.press("tab")



def weather():
    api_key_for_weather = "YOUR_API"
    city_name = "Lahore"

    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID={api_key_for_weather}")

    temperature = weather_data.json()['main']['temp']
    speak(f"The temperature is {round(temperature)}°C")
    print(f"The temperature is {round(temperature)}°C")



def app_changer():
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    while True:
        app_dission = audio(30)
        if "go to next" in app_dission:
            pyautogui.press("tab")
        elif "select" in app_dission:
            pyautogui.keyUp("alt")
            break
        elif TimeoutError:
            pyautogui.keyUp("alt")
            pyautogui.hotkey("alt","tab")
            break

    
    
def chatgpt_text(text):
    time.sleep(4)   # help comunicate with chat gpt
    pyautogui.hotkey("ctrl", "a")   # clear chatgpt chat box
    pyautogui.press("backspace")
    key_word = "what is"
    user_input = text
    start = text.find(key_word) + len(key_word)
    extracted_text  = user_input[start:].strip()
    pyautogui.write(extracted_text)
    pyautogui.press("enter")



def chatgpt_audio():
    time.sleep(4)
    pyautogui.hotkey("ctrl", "a")   # clear chatgpt chat box
    pyautogui.press("backspace")
    time.sleep(1)
    tab(2)
    pyautogui.press("enter")
    time.sleep(15)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")

                

def whatsapp():
    pyautogui.hotkey("win","s") # this opens windows search bar         
    time.sleep(1)
    pyautogui.write("whatsapp")
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.hotkey("ctrl","f")
    pyautogui.hotkey("ctrl","a")
    pyautogui.press("backspase")
    speak("who do you want to message")
    contact = audio(20)
    pyautogui.write(contact)
    pyautogui.press("enter")
    speak("do you want to send text message or voice message")
    message_choise = audio(20)

    if "text" in message_choise:
        while True:
            speak("speak your message")
            message = audio(20)
            pyautogui.write(message)
            speak("do i send the message")
            send_message = audio()
            if "send" in send_message:
                pyautogui.press("enter")
            else:
                None
            speak("do you want to send another message")
            new_message = audio(20)
            if "yes please" or "message" in new_message:
                pyautogui.hotkey("ctrl","a")
                pyautogui.press("backspase")
                continue
            elif "no" in new_message:
                break
            else:
                break

    elif "voice" in message_choise:
        speak("ok start speaking")
        tab(1)
        pyautogui.press("enter")
        time.sleep(10)
        tab(2)
        pyautogui.press("enter")



def process(command):

    if "tell" in command and "me" in command: # this is used for genral chat/questions
        genral_chat(command)

    elif "close" in command and "app" in command : # this closes the opend app
        pyautogui.hotkey("alt","f4")
        print("Task complete : App closed\n")
                       
    elif "close" in command and "tab" in command : # this closes the opend tab
        pyautogui.hotkey("ctrl","w")    
        print("Task complete : Tab closed\n")

    elif "open whatsapp" in command : # this opens Whatsapp
        pyautogui.hotkey("win","s")                    
        time.sleep(1)
        pyautogui.write("whatsapp")
        pyautogui.press("enter") 
        print("Task complete : Whatsapp opened\n")

    elif "open google" in command : # this opens Google
        webbrowser.open("https://www.google.com")
        print("Task complete : Google opened\n")
  
    elif "alexa" in command and "message" in command : # this opens Whatsapp directly to message
        whatsapp()
        print("Task complete : Whatsapp opened for messaging\n")

    elif "open youtube" in command : # this opens Youtube
        webbrowser.open("https://www.youtube.com")     
        print("Task complete : Youtube opened\n")

    elif "play music" in command : # this opens Youtube Music
        webbrowser.open("https://music.youtube.com")   
        print("Task complete : Youtube music opened\n")

    elif "open chat" in command : # this opens Chatgpt
        webbrowser.open("https://www.chatgpt.com")     
        print("Task complete : Chatgpt opened\n")

    elif "ask" in command and "chat" in command : # this opens Chatgpt directly to chat  
        webbrowser.open("https://www.chatgpt.com")     
        chatgpt_text(command)
        print("Task complete : Chatgpt opened for chat\n")

    elif "voice" in command and "chat" in command : # this opens Chatgpt directly to chat  
        webbrowser.open("https://www.chatgpt.com")     
        chatgpt_audio()
        print("Task complete : Chatgpt opened for chat\n")

    elif "change" in command and ("tab" in command or "app" in command) : # this changes the app to the last opened app
        pyautogui.hotkey("alt","tab")
        print("Task complete : App changed\n")

    elif "show" in command and "open" in command and ("apps"in command or "app"in command) : # this shows the opened apps and opens the desiered one
        app_changer()
        print("Task complete : App changed\n")

    elif "scroll" in command and "down" in command : # this scrolls the page down
        scroll_down()
        print("Task complete : Page scrolled down\n")

    elif "scroll" in command and "up" in command : # this scrolls the page up
        scroll_up()
        print("Task complete : Page scrolled up\n")

    elif ("tell" in command or "what" in command ) and "date" in command : # this tell the date
        date()

    elif ("tell" in command or "what" in command ) and "time" in command : # this tell the date
        current_time()

    elif "weather" in command or "temperature" in command: # this tells the weather/temprature
        weather()

    elif "open gmail" in command : # this opens Gmail  
        webbrowser.open("https://www.mail.google.com") 
        print("Task complete : Gmail opened\n")

    elif "open github" in command : # this opens Github
        webbrowser.open("https://www.github.com")      
        print("Task complete : Github opened\n")

    else: # this runs if command is not defined
        speak("command not in directory !")
        print("\033[31mCommand not in directory !\033[0m")




if __name__ == "__main__" :

    print("\n\n\tInitilizing Alexa....\n\n")
    speak("Initilizing Alexa....")

    while True:  
        # listne for the wake word
        # get voice from mic
        try:

            wake_word_and_command = audio(2)

            # if("alexa" == wake_word_and_command):                 
            #     speak("yes")
            #     print("\nAlexa actiwated !")

            #     command = audio()
            #     process(command)

            if("alexa" in wake_word_and_command and "close" in wake_word_and_command and "program" in wake_word_and_command):
                speak("ok")
                print("ALexa is now powering off")
                print("Thank you!")
                break

            elif(wake_word_and_command.startswith("alexa")):
                process(wake_word_and_command)

        except sr.WaitTimeoutError:
            continue

        except Exception as e:
            print(f"\033[31mUnexpected error {e} !\033[0m")














