# This file listens for words every 3 seconds and looks for "Fluffy Cloud" or "Christmas Tree"
# In the event that either phrase is heard, an image of those pops up
import time
import speech_recognition as sr
import popup


def callback(recognizer, audio):
    """
    The function to be called by the speech recognizer
    
    :param recognizer: The recognizer itself
    :param audio: The audio it should recognize
    """
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        # Sphinx SUCKS
        recognition = recognizer.recognize_sphinx(audio)
        print("Sphinx Speech Recognition thinks you said '" + recognition + "'")
        if "fluffy cloud" in recognition:
            popup.open_popup("Fluffy Cloud")
        elif "christmas tree" in recognition:
            popup.open_popup("Christmas Tree")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    """
    The main entrypoint into the program
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    stop_listening = recognizer.listen_in_background(microphone, callback)

    # while True:
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        # `stop_listening` is now a function that, when called, stops background listening
        
        
        # for _ in range(30):
        #     time.sleep(0.1) # This only applies to the main thread

        # calling this function requests that the background listener stop listening
        # stop_listening(wait_for_stop=True)

    # Let other computations happen, but check this thread every 0.1 seconds
    while True: 
        time.sleep(0.1)  # Pause the main thread

main()