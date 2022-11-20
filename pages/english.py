import streamlit as st

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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


colL, colM, colR = st.columns([1, 3, 1])
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


with colR:
    stt_button2 = Button(label="stop!", width=125, button_type="danger")
    stt_button2.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "zh-CN";
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT2", {detail: value}));
            }
        }
        recognition.start();
        recognition.stop();
        """))

    result2 = streamlit_bokeh_events(
        stt_button2,
        events="GET_TEXT2",
        key="listen2",
        refresh_on_update=False,
        override_height=45,
        debounce_time=0)




with colL:
    stt_button = Button(label="repeat after me!", width=125, button_type="primary")

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "zh-CN";
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))



    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=45,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            colM.info(f"You said:  {result.get('GET_TEXT')}")
            if result.get("GET_TEXT").lower() == text_2_repeat.lower():
                colM.success('Good job!')
                result = None
            else:
                colM.error('Keep going!')

# if st.button('repeat after me!'):
#     colL.info(text_2_repeat)
#     try:
#         colR.info("A moment of silence, please...")
#         with m as source: r.adjust_for_ambient_noise(source)
#         colR.info("Set minimum energy threshold to {}".format(r.energy_threshold))
#         while True:
#             with st.empty():
#                 colR.write("Say something!")
#                 with m as source: audio = r.listen(source)
#                 colR.success("Got it! Now to recognize it...")
#                 try:
#                     # recognize speech using Google Speech Recognition
#                     value = r.recognize_google(audio)
#                     # value = r.recognize_whisper(audio, language="chinese")
#                     # we need some special handling here to correctly print unicode characters to standard output
#                     if str is bytes:  # this version of Python uses bytes for strings (Python 2)
#                         colR.write(u"You said {}".format(value).encode("utf-8"))
#                     else:  # this version of Python uses unicode for strings (Python 3+)
#                         colR.write("You said {}".format(value))
#                 except sr.UnknownValueError:
#                     colR.warning("Oops! Didn't catch that")
#                 except sr.RequestError as e:
#                     colR.error("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
#                 if value == text_2_repeat:
#                     st.success('Very good!')
#                     break
#
#     except KeyboardInterrupt:
#         pass

bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)