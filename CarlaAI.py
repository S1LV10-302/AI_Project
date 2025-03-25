import geocoder
import speech_recognition as sr
import pyttsx3
import requests
import wikipedia

API_KEY = "19f55e5377914195b9d163824252203"  

# Voice settings
VOICE_INDEX = 1  # 0- Male | 1 - Female
SPEECH_RATE = 200  
VOLUME = 1.0  

def get_location():
    g = geocoder.ip('me')
    return g.latlng

def get_weather():
    lat, lng = get_location()
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lng}&aqi=no"
    response = requests.get(url)
    data = response.json()

    
    location = data['location']['name']
    temperature = data['current']['temp_c']
    condition = data['current']['condition']['text']
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_kph']

   
    weather_info = (
        f"The current weather in {location} is {condition}. "
        f"The temperature is {temperature} degrees Celsius. "
        f"The humidity is {humidity} percent. "
        f"The wind speed is {wind_speed} kilometers per hour."
    )

    return weather_info

def search_internet(query, sentences=3):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Sorry, no results found for your query."

def initialize_tts():
    engine = pyttsx3.init()

    
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[VOICE_INDEX].id)   
    engine.setProperty('rate', SPEECH_RATE)
    engine.setProperty('volume', VOLUME)

    return engine

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

def listen_for_command(r, source):
    try:
        print("Listening for your command...")
        audio = r.listen(source, timeout=20)  
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

def main():
    engine = initialize_tts()

    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            command = listen_for_command(r, source)
            if not command:
                continue

            if command.startswith('hey carla'):
                speak("How can I help you?", engine)
                print('How can i help you?')
                continue  

            if command == 'weather' or command =='good morning':  # Weather option
                weather_info = get_weather()
                print(weather_info)
                speak(weather_info, engine)

            elif command == 'search':  # Search option
                speak("What do you want to search for?", engine)
                print("What do you want to search for?")
                query = listen_for_command(r, source)
                if not query:
                    continue

                sentences = 2
                results = search_internet(query, sentences)
                print("\n")
                print(results) 
                speak(results, engine)
                print("\n")

                # Option to add more information 
                while True:
                    print("Say 'add' to add more sentences or 'ok' to stop.")
                    additional_command = listen_for_command(r, source)
                    if additional_command == 'add':
                        sentences += 4  
                        results = search_internet(query, sentences)
                        print("\n")
                        print(results) 
                        speak(results, engine)
                        print("\n")
                    elif additional_command == 'okay' or additional_command == 'ok' or additional_command == 'stop' :
                        break
                    elif additional_command == 'stop':
                        break
                    else:
                        print("Invalid command. Please say 'more' or 'stop'.")

            elif command == 'stop' or command =='exit':  # Exit option
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
