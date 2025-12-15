import streamlit as st


class Canvas:
    def __init__(self):
        if 'blocks' not in st.session_state:
            st.session_state.blocks = []

    def render(self):
        pass
