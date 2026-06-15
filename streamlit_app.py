import streamlit as st
import pandas as pd

user_name = ""
user_classes = []

sheet_path = "sheet.xlsx"

master_sheet = pd.read_excel("sheet.xlsx")

st.title("WA 27-28 Class Doc")

if "saved_name" not in st.session_state:
    st.session_state.saved_name = ""

st.write(
    "Input your name into the box below and submit. Then, add your classes into the \"Class\" column of the table **exactly as written on your schedule (no typos, capitalized correctly, etc.)** and submit them by pressing the button below."
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
    name = st.text_input("Name", value=st.session_state.saved_name)
    submit = st.form_submit_button("Submit")

    if submit:
        st.session_state.saved_name = name

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
    if not st.session_state.saved_name:
        st.error("Please enter and submit your name above before saving your schedule!")
    else:
        name_column = master_sheet.columns[0]
        name_exists = st.session_state.saved_name in master_sheet[name_column].values
        user_classes = edited_df["Class"].tolist()
        row_data = [st.session_state.saved_name] + user_classes
        new_row = pd.DataFrame([row_data]) 
        new_row.columns = master_sheet.columns[:len(row_data)] 

        if name_exists:
            # Remove the old row where the name matches
            master_sheet = master_sheet[master_sheet[name_column] != st.session_state.saved_name]
            st.warning(f"Existing schedule for '{st.session_state.saved_name}' was overwritten.")
        else:
            st.success("Schedule saved successfully!")

        master_sheet = pd.concat([master_sheet, new_row], ignore_index=True)
        master_sheet.to_excel(sheet_path, index=False)

if st.session_state.saved_name == "john dingleberry":
    st.write("### Master Class List")
    st.dataframe(master_sheet)

st.write(len(master_sheet))