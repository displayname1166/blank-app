import streamlit as st
import pandas as pd

user_name = ""
user_classes = []

sheet_path = "sheet.xlsx"

dingus = pd.read_excel("sheet.xlsx")

st.title("WA 27-28 Class Doc")

st.write(
    "Input your name into the box below and submit. Then, add your classes into the \"Class\" column of the table **exactly as written on your schedule** and submit them by pressing the button below."
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

with st.form("entry_form"):
    name = st.text_input("Name")
    submit = st.form_submit_button("Submit")

    if submit:
        user_name = name

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

submit = st.button("Submit")

if submit:
    user_classes = edited_df["Class"].tolist()

st.write(user_classes)

st.write("### Current Spreadsheet Content")
st.dataframe(dingus)