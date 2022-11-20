import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("English speech therapy assisted by AI")

text_2_repeat = st.text_input('input english text you wish to practice')
if text_2_repeat:
    st.success(text_2_repeat)
else:
    st.warning('please enter english text you would like to practice with')

colL, colM, colR = st.columns([1, 3, 1])

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
                colM.info(f"You said:  {result.get('GET_TEXT')}")
                if result.get("GET_TEXT").lower() == text_2_repeat.lower():
                    colM.success('Good job!')
                    result = None
                else:
                    colM.error('Keep going!')
    except:
        pass


bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)
