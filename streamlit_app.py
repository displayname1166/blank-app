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
    "Input your name into the box below and submit. Then, add your classes into the \"Class\" column of the table **exactly as written on your schedule (no typos, capitalized correctly, etc.) but without course numbers** and submit them by pressing the button below."
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
        "Block": st.column_config.TextColumn(width=-400),
        "Class": st.column_config.TextColumn()
    },
    hide_index=True, 
    disabled=["Block"], 
)

submit = st.button("Submit")

if submit:
    if not st.session_state.saved_name:
        st.error("Enter and submit your name above before saving your schedule.")
    else:
        name_column = master_sheet.columns[0]
        name_exists = st.session_state.saved_name in master_sheet[name_column].values
        user_classes = edited_df["Class"].tolist()
        row_data = [st.session_state.saved_name] + user_classes
        new_row = pd.DataFrame([row_data]) 
        new_row.columns = master_sheet.columns[:len(row_data)] 

        if name_exists:
            master_sheet = master_sheet[master_sheet[name_column] != st.session_state.saved_name]
            st.warning(f"Existing schedule for '{st.session_state.saved_name}' was overwritten.")
        else:
            st.success("Schedule saved successfully.")

        master_sheet = pd.concat([master_sheet, new_row], ignore_index=True)
        master_sheet.to_excel(sheet_path, index=False)
        
        for i in range(len(master_sheet)):
            other_student_name = master_sheet.iloc[i, 0]
            
            if other_student_name == st.session_state.saved_name:
                continue
                
            other_student_classes = master_sheet.iloc[i, 1:].tolist()
            
            matches = {i: item1 for i, (item1, item2) in enumerate(zip(user_classes, other_student_classes)) if item1 == item2}
            
            if matches:
                block_letters = ["A", "B", "C", "D", "E", "F", "G"]
        
                block_matches = {letter: [] for letter in block_letters}
                
                for i in range(len(master_sheet)):
                    other_student_name = master_sheet.iloc[i, 0]
                    
                    if other_student_name == st.session_state.saved_name:
                        continue
                        
                    other_student_classes = master_sheet.iloc[i, 1:].tolist()
                    
                    for idx, letter in enumerate(block_letters):
                        user_class = user_classes[idx]
                        other_class = other_student_classes[idx]
                        
                        if user_class == other_class and user_class != "" and pd.notna(user_class):
                            block_matches[letter].append(f'"{other_student_name}"')
                
                for letter in block_letters:
                    students_list = block_matches[letter]
                    
                    if students_list:
                        st.write(f"{letter}: {', '.join(students_list)}")
                    else:
                        st.write(f"{letter}: No matches yet")

if st.session_state.saved_name == "john dingleberry":
    st.write("### Master Class List")
    st.dataframe(master_sheet)
