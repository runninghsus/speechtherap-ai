import pandas as pd
import streamlit as st
import os

import streamlit.components.v1 as components

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Chinese speech therapy assisted by AI")
# st.sidebar.markdown("Chinese")

import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

import PyPDF2
import random
import pandas as pd
import regex as re
from translate import Translator

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "../st_audiorec/frontend/build")
st_audiorec = components.declare_component("st_audiorec", path=build_dir)


def remove_punctuation(text):
    return re.sub(r"\p{P}+", "", text)
punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
# punc = punc
# re.sub(ur"[%s]+" %punc, "", line.decode("utf-8"))


text_2_trans = st.text_input('請輸入英文句子，此網頁會翻譯成中文讓你對著練習')
translator= Translator(to_lang="zh")
if text_2_trans:
    text_2_repeat = translator.translate(text_2_trans)
    # if text_2_repeat is None:

    st.success(text_2_repeat)
else:
    st.warning('請輸入你想要練習的中文，此網頁會幫你英翻中')
# uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
# if uploaded_file is not None:
#     # Launch pdf reader object
#     pdfReader = PyPDF2.PdfFileReader(uploaded_file)
#     # number of pages in pdf
#     n_pages = pdfReader.numPages
#     Texts = []
#     for p in range(n_pages):
#       # Open the page
#       pageObj = pdfReader.getPage(p)
#       # Add the text in your list
#       Texts.append(pageObj.extractText())
#
#
#     phrase_length = st.number_input('多少個字', min_value=2, max_value=50, value=10)
#
#     try:
#         with open('./test.txt', encoding='utf8') as f:
#             for line in f:
#                 text_2_repeat = line.strip()
#             #     st.write(line.strip())
#             # text_2_repeat = f.strip()
#         # st.success(text_2_repeat)
#         st.success(text_2_repeat)
#         if st.checkbox('重選'):
#             if st.button('下一個'):
#                 random_text_start = random.choice(range(len(Texts[0])))
#                 text_2_repeat = Texts[0][random_text_start:random_text_start + phrase_length]
#             st.info(text_2_repeat)
#             with open("./test.txt", "w", encoding='utf-8') as text_file:
#                 text_file.write(text_2_repeat)
#     except:
#         if st.button('下一個'):
#             random_text_start = random.choice(range(len(Texts[0])))
#             text_2_repeat = Texts[0][random_text_start:random_text_start + phrase_length]
#         st.info(text_2_repeat)
#         with open("./test.txt", "w", encoding='utf-8') as text_file:
#             text_file.write(text_2_repeat)

    # if st.button('選定'):
    #     print(text_2_repeat)
    # with open("./test.txt", "w") as text_file:
    #     text_file.write(text_2_repeat)

colL, colM, colR = st.columns([1, 3, 1])
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


with colR:
    stt_button2 = Button(label="停止!", width=125, button_type="danger")
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
    stt_button = Button(label="跟著我重複!", width=125, button_type="primary")

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
            colM.info(f"你說了:  {result.get('GET_TEXT')}")
            if result.get("GET_TEXT") == remove_punctuation(text_2_repeat):
                colM.success('非常好!')
                result = None
            else:
                colM.error('繼續加油!')



    # stop_button = colR.button('停止')



# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
#
# text = st.text_input("Say what ?")
#
# tts_button = Button(label="Speak", width=100)
#
# tts_button.js_on_event("button_click", CustomJS(code=f"""
#     var u = new SpeechSynthesisUtterance();
#     u.text = "{text}";
#     u.lang = 'zh-CN';
#
#     speechSynthesis.speak(u);
#     """))
#
# st.bokeh_chart(tts_button)

# st.bokeh_chart(tts_button)
# if st.button('跟著我重複!'):
#     colL.info(text_2_repeat)
    # st_audiorec()

    # try:
    #     colR.info("A moment of silence, please...")
    #     with m as source: r.adjust_for_ambient_noise(source)
    #     colR.info("Set minimum energy threshold to {}".format(r.energy_threshold))
    #     while True:
    #         with st.empty():
    #             colR.write("Say something!")
    #             with m as source: audio = r.listen(source)
    #             colR.success("Got it! Now to recognize it...")
    #             try:
    #                 # recognize speech using Google Speech Recognition
    #                 value = r.recognize_google(audio, language="zh-CN")
    #                 # value = r.recognize_whisper(audio, language="chinese")
    #                 # we need some special handling here to correctly print unicode characters to standard output
    #                 if str is bytes:  # this version of Python uses bytes for strings (Python 2)
    #                     colR.write(u"You said {}".format(value).encode("utf-8"))
    #                 else:  # this version of Python uses unicode for strings (Python 3+)
    #                     colR.write("You said {}".format(value))
    #             except sr.UnknownValueError:
    #                 colR.warning("Oops! Didn't catch that")
    #             except sr.RequestError as e:
    #                 colR.error("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    #             if value == remove_punctuation(text_2_repeat):
    #                 st.success('非常好!')
    #                 break
    #
    # except KeyboardInterrupt:
    #     pass

bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)