import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data sweeper",layout="centered")

# custom css

st.markdown(
    """
    <style>
    .stApp{
       background-color:pink;
       color:white;
          }
          </style>
          """,
          unsafe_allow_html=True
)

# tittle and description
st.title("DATASWEEPER BY KINZA SAEED")
st.write("Transform your files between CSV, Excel, and JSON formats with built-in cleaning, visualization, and AI-powered suggestions.")

# file uploader
file_uploader=st.file_uploader("Upload your file (CSV, Excel): ", type=["cvs", "xlsx"], accept_multiple_files=(True))

if file_uploader:
    for file in file_uploader:
        file_ext=os.path.splitext(file.name)[-1].lower()
        if file_ext==".csv":
            df=pd.read_csv(file)
        elif file_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue        
        # file details
        st.write("Previwe")
        st.dataframe(df.head())

        # data cleaning options
        st.subheader("Data Cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1,col2=st.columns(2)

            with col1:
                if st.button(f"Remove duplicate from file : {file.name} 🗑️"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicate remove")
            with col2:

                if st.button(f"File missing value : {file.name} ❓"):
                    numerical_col=df.select_dtypes(include=["number"]).columns
                    df[numerical_col]=df[numerical_col].fillna(df[numerical_col].mean())
                  
                    st.write("✅ Missing values have been filled")        
        st.subheader("Select columns to keep")    
        columns = st.multiselect(f'Choose columns for {file.name}', df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader('📊 Data Visualization')
        if st.checkbox(f'Show Visualization for {file.name}'):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # Conversion Options
        st.subheader('✨ Conversion Options')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, '.csv')
                mime_type = 'text/csv'
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False, engine='openpyxl')  # Ensure openpyxl is used
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)

            st.download_button(
                label=f'Download {file.name} as {conversion_type}',
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success('🎉 All files processed successfully')        
