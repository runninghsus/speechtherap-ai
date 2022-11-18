import streamlit as st

st.title("Main page")
descriptor = st.expander('main purpose', expanded=True)
descriptor.write('This app is a working demo as a assistant technology to help subjects practice words using '
                 'state-of-the-art google translate and google speech recognition. '
                 'It is not meant to be commericialized, rather more of a push for AI-assisted therapy in medicine.')


