import streamlit as st

st.title("English speech therapy assisted by AI")

import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

import PyPDF2
import random
import pandas as pd
import regex as re
from translate import Translator


text_2_repeat = st.text_input('input english text you wish to practice')
if text_2_repeat:
    st.success(text_2_repeat)
else:
    st.warning('please enter english text you would like to practice with')
colL, colR = st.columns(2)

if st.button('repeat after me!'):
    colL.info(text_2_repeat)
    try:
        colR.info("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        colR.info("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            with st.empty():
                colR.write("Say something!")
                with m as source: audio = r.listen(source)
                colR.success("Got it! Now to recognize it...")
                try:
                    # recognize speech using Google Speech Recognition
                    value = r.recognize_google(audio)
                    # value = r.recognize_whisper(audio, language="chinese")
                    # we need some special handling here to correctly print unicode characters to standard output
                    if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                        colR.write(u"You said {}".format(value).encode("utf-8"))
                    else:  # this version of Python uses unicode for strings (Python 3+)
                        colR.write("You said {}".format(value))
                except sr.UnknownValueError:
                    colR.warning("Oops! Didn't catch that")
                except sr.RequestError as e:
                    colR.error("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                if value == text_2_repeat:
                    st.success('Very good!')
                    break

    except KeyboardInterrupt:
        pass