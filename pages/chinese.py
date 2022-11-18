import pandas as pd
import streamlit as st


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

colL, colR = st.columns(2)
if st.button('跟著我重複!'):
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
                    value = r.recognize_google(audio, language="zh-CN")
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
                if value == remove_punctuation(text_2_repeat):
                    st.success('非常好!')
                    break

    except KeyboardInterrupt:
        pass

bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)