import streamlit as st

hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.title("Speech TherapAI")
descriptor = st.expander('main purpose', expanded=True)
descriptor.write('Speech TherapAI is a working demo as an assistant technology to help subjects practice words using '
                 'state-of-the-art google translate and google speech recognition. '
                 'It is not meant to be commericialized, rather more of a push for AI-assisted therapy in medicine.')


bottom_cont = st.container()
with bottom_cont:
    st.markdown("""---""")
    st.write('')
    st.markdown('<span style="color:grey">{}</span>'.format('Speech TherapAI is developed by Alexander I. Hsu'),
                unsafe_allow_html=True)

