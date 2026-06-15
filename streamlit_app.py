import streamlit as st
import pandas as pd

st.title("WA 27-28 Class Doc")

st.write(
    "Input your classes into the \"Class\" column **exactly as written on your schedule**."
)

df = pd.DataFrame(
    [
        {"Block": "A", "Class": ""},
        {"Block": "B", "Class": ""},
        {"Block": "C", "Class": ""},
        {"Block": "D", "Class": ""},
        {"Block": "E", "Class": ""},
        {"Block": "F", "Class": ""},
        {"Block": "G", "Class": ""},
    ]
)

edited_df = st.data_editor(
    df, 

    column_config={
        "Block": st.column_config.TextColumn(
            width = -400
        ),

        "Class": st.column_config.TextColumn(
        )
    },

    hide_index=True, 

    disabled=["Block"], 
 )