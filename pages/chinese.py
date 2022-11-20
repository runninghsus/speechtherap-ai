import regex as re
import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events
from translate import Translator

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Chinese speech therapy assisted by AI")


def remove_punctuation(text):
    return re.sub(r"\p{P}+", "", text)


punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."

text_2_trans = st.text_input('請輸入英文句子，此網頁會翻譯成中文讓你對著練習')
translator = Translator(to_lang="zh")
if text_2_trans:
    text_2_repeat = translator.translate(text_2_trans)
    st.success(text_2_repeat)
else:
    st.warning('請輸入你想要練習的中文，此網頁會幫你英翻中')

colL, colM, colR = st.columns([1, 3, 1])

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

    try:
        if result:
            if "GET_TEXT" in result:
                colM.info(f"你說了:  {result.get('GET_TEXT')}")
                if result.get("GET_TEXT") == remove_punctuation(text_2_repeat):
                    colM.success('非常好!')
                    result = None
                else:
                    colM.error('繼續加油!')
    except:
        pass



bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)
