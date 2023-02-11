import streamlit as st
from streamlit_option_menu import option_menu
import os

import re
import string
import pandas as pd

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

# Default Wide Mode Appearance Streamlit
st.set_page_config(layout='wide')

# Default Dataset
text_data = "UPPERCASE MENJADI lowercase\nangka 1 2 3 akan hilang\ntanda baca ! ? . @ # $ % & akan hilang \nKata-kata alay: aer aing\nStopword yang akan hilang adalah menjadi, akan, aku\nStemming kata menghilang dan mencintai"
csv_data = pd.read_csv("data.csv", encoding = 'ISO-8859-1')

# Import kamus alay
df_kamusalay = pd.read_csv("new_kamusalay.csv", encoding = 'ISO-8859-1', header=None,index_col=0,squeeze=True)
dict_kamusalay = df_kamusalay.to_dict()

#Import Stopwords Indonesia
df_stopwords = pd.read_csv("stopwordbahasa.csv", encoding = 'ISO-8859-1')
list_stopwords = df_stopwords["stopwordbahasa"].tolist()

# Sidebar
with st.sidebar:
    selected = option_menu ("Text Cleaner App",
    ["Input Text",
    "Input Text from CSV",
    "Input Multiple Text from CSV",
    "Update Kamus Alay",
    "Update Stopwords"])

    # Checkbox
    st.header("Select Option :")
    all_option_check = st.checkbox ("EXECUTE ALL OPTION")
    lowercase_check = st.checkbox ("Lowercase")
    threeormore_check = st.checkbox ("Three or More")
    stemming_check = st.checkbox ("Stemming")
    tokenization_check = st.checkbox ("Tokenization")
    normalization_check = st.checkbox ("Normalization (using Kamus Alay)")
    remove_number_check = st.checkbox ("Remove Number")
    remove_punctuation_check = st.checkbox ("Remove Punctuation")
    stopwords_check = st.checkbox ("Stopwords")
    to_string_check = st.checkbox ("List to String")
    
# FUNCTION
# Lowercase
def lowercase (data):
    data = data.lower()
    st.success("Success to Run 'Lowercase'", icon="✅")
    return data
# Three or More
def threeormore (data):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    data = pattern.sub(r"\1", data)
    st.success("Success to Run 'Three or More'", icon="✅")
    return data
# Stemming
def stemming (data) :
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data = stemmer.stem(data)
    st.success("Success to Run 'Stemming'", icon="✅")
    return data
 # Tokenization
def tokenization (data) :
    data = data.split()
    st.success("Success to Run 'Tokenization'", icon="✅")
    return data
# Normalization (Kamus Alay)
def normalization (data) :
    for i in data :
        for key, value in dict_kamusalay.items():
            if key not in data:
                continue
            index = data.index(key)
            data[index] = value
    st.success("Success to Run 'Normalization'", icon="✅")
    return data
# Remove Number
def remove_number (data):
    data = str(data)
    data = re.sub(r'\d+','',data)
    data = data.split() 
    st.success("Success to Run 'Remove Number'", icon="✅")
    return data
# Remove Punctuation
def remove_punctuation (data) :
    data = str(data)
    data = re.sub('-', ' ', data)
    data = re.sub(r'[^\w\s]', ' ', data)
    data = data.split()
    st.success("Success to Run 'Remove Punctuation'", icon="✅")
    return data
# Stopwords
def stopwords (data) :
    for i in reversed (data) :
        if i in list_stopwords :
            data.remove(i)
    st.success("Success to Run 'Stopwords'", icon="✅")
    return data
# List to String
def to_string (data) :
    data = ' '.join(map(str,data))
    st.success("Success to Run 'List to String'", icon="✅")
    return data
# Update file CSV text cleansing
def update_csv (uploadedfile):
    with open (os.path.join("data.csv"),"wb") as f:
        f.write (uploadedfile.getbuffer())
        return st.success ("Saved file:{} ".format(uploadedfile.name))
# Update File Kamus Alay 
def update_kamusalay (uploadedfile):
    with open (os.path.join("new_kamusalay.csv"),"wb") as f:
        f.write (uploadedfile.getbuffer())
        return st.success ("Saved file:{} ".format(uploadedfile.name))
# Update Stopwords
def update_stopwords (uploadedfile):
    with open (os.path.join("stopwordbahasa.csv"),"wb") as f:
        f.write (uploadedfile.getbuffer())
        return st.success ("Saved file:{} ".format(uploadedfile.name))

# Main Page
st.title ("Text Cleaner App")


# Input Text
if selected == "Input Text":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader ("Input text :")
        text_data = st.text_area ("Input text :",text_data, height = 200,label_visibility="collapsed")
        st.write (f"Data Type of Input Text :  {type(text_data)}")
        running_cleansing_text = st.button ("Click to Run Text Cleansing")
        
        if running_cleansing_text:
            # EXECUTE ALL OPTION
            if all_option_check :
                if stemming_check or lowercase_check or remove_number_check or remove_punctuation_check or tokenization_check or normalization_check or stopwords_check == True :
                    st.error('"Failed to Run "Execute All Option". Please choose "Execute All Option" ONLY !', icon="🚨")
                else :
                    text_data = lowercase (text_data)
                    text_data = threeormore (text_data)
                    text_data = stemming (text_data)
                    text_data = tokenization (text_data)
                    text_data = normalization (text_data)
                    text_data = remove_number (text_data)
                    text_data = remove_punctuation (text_data)
                    text_data = stopwords (text_data)
                    text_data = to_string (text_data)
                    st.success("Success to Run 'Execute All Option'", icon="✅")

            # Lowercase
            if lowercase_check :
                text_data = lowercase (text_data)
            else:
                pass
            
            # Three or More
            if threeormore_check :
                text_data = threeormore (text_data)
            
            # Stemming
            if stemming_check :
                text_data = stemming (text_data)
            
            # Tokenization
            if tokenization_check :
                text_data = tokenization (text_data)

            # Normalization (Kamus Alay)
            if normalization_check :
                if tokenization_check == False :
                    st.error('"Failed to Run "Normalization". Normalization need Tokenization. Please choose Tokenization first !', icon="🚨")
                    #st.write ("Normalization need Tokenization. Please choose Tokenization first !")
                else :
                    pass
                text_data = normalization (text_data)

            # Remove Number
            if remove_number_check :
                text_data = remove_number (text_data)
                
            # Remove Punctuation
            if remove_punctuation_check :
                text_data = remove_punctuation (text_data)
                            
            # Stopwords
            if stopwords_check :
                if tokenization_check == False :
                    st.error('"Failed to Run "Stopwords". Stopwords need Tokenization. Please choose Tokenization first !', icon="🚨")
                    #st.write ("Stopwords need Tokenization. Please choose Tokenization first !")
                else :
                    text_data = stopwords (text_data)

            # List to String
            if to_string_check :
                text_data = to_string (text_data)
    
    with col2: 
        st.subheader ("Output text :")
        st.text_area ("Output text :", value = text_data, height = 200,label_visibility="collapsed")
        st.write (f"Data Type of Output Text :  {type(text_data)}")
    
# Input CSV
if selected == "Input Text from CSV":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader ("Update File CSV")
        upload_file1 = st.file_uploader ("Update File CSV", type = "csv", label_visibility="collapsed")
        if upload_file1 is not None :
            csv_data_uploaded = pd.read_csv(upload_file1, encoding = 'ISO-8859-1')
            st.dataframe (csv_data_uploaded)
        clicked = st.button ("Click to Update Database")
        if clicked :
            update_csv (upload_file1)
            csv_data = csv_data_uploaded
            st.subheader ("List File CSV After Update")
            st.dataframe (csv_data)

    with col2:
        # Default Data CSV
        st.subheader ("Data CSV Used:")
        st.dataframe (csv_data, height = 200)
        
        # Choose Row and Coloumn
        st.subheader ("Write the Row :")
        choose_row = st.text_input ("Write the Row :", value = "Tweet", label_visibility="collapsed" )
        st.subheader ("Pick the Column :")
        choose_column = st.number_input ("Pick the Number of Column :", value = 1, key = int, step = 1, min_value=None, max_value=None, label_visibility="collapsed" )
        st.write (f"Data yang dipilih adalah kolom '{choose_row}' baris ke-'{choose_column}'")
        text_data = csv_data[choose_row][choose_column]
           
    with col3: 
        # Input Text Used
        st.subheader ("Input Text Used :")
        st.text_area ("Input Text Used :", value = text_data, height =200, label_visibility ="collapsed" )
        st.write (f"Data Type :  {type(text_data)}")

        running_cleansing_text_2 = st.button ("Click to Run Text Cleansing")
    
        if running_cleansing_text_2:
            # EXECUTE ALL OPTION
            if all_option_check :
                if stemming_check or lowercase_check or remove_number_check or remove_punctuation_check or tokenization_check or normalization_check or stopwords_check == True :
                    st.error('"Failed to Run "Execute All Option". Please choose "Execute All Option" ONLY !', icon="🚨")
                else :
                    text_data = lowercase (text_data)
                    text_data = threeormore (text_data)
                    text_data = stemming (text_data)
                    text_data = tokenization (text_data)
                    text_data = normalization (text_data)
                    text_data = remove_number (text_data)
                    text_data = remove_punctuation (text_data)
                    text_data = stopwords (text_data)
                    text_data = to_string (text_data)
                    st.success("Success to Run 'Execute All Option'", icon="✅")

            # Lowercase
            if lowercase_check :
                text_data = lowercase (text_data)
            else:
                pass
            
            # Three or More
            if threeormore_check :
                text_data = threeormore (text_data)
            
            # Stemming
            if stemming_check :
                text_data = stemming (text_data)
            
            # Tokenization
            if tokenization_check :
                text_data = tokenization (text_data)

            # Normalization (Kamus Alay)
            if normalization_check :
                if tokenization_check == False :
                    st.error('"Failed to Run "Normalization". Normalization need Tokenization. Please choose Tokenization first !', icon="🚨")
                    #st.write ("Normalization need Tokenization. Please choose Tokenization first !")
                else :
                    pass
                text_data = normalization (text_data)

            # Remove Number
            if remove_number_check :
                text_data = remove_number (text_data)
                
            # Remove Punctuation
            if remove_punctuation_check :
                text_data = remove_punctuation (text_data)
                            
            # Stopwords
            if stopwords_check :
                if tokenization_check == False :
                    st.error('"Failed to Run "Stopwords". Stopwords need Tokenization. Please choose Tokenization first !', icon="🚨")
                    #st.write ("Stopwords need Tokenization. Please choose Tokenization first !")
                else :
                    text_data = stopwords (text_data)

            # List to String
            if to_string_check :
                text_data = to_string (text_data)
    
    with col4:
        st.subheader ("Output text :")
        st.text_area ("Output text :", value = text_data, height = 200,label_visibility="collapsed")
        st.write (f"Data Type of Output Text :  {type(text_data)}")    

# Input Multiple Text from CSV
if selected == "Input Multiple Text from CSV":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader ("Update File CSV")
        upload_file1 = st.file_uploader ("Update File CSV", type = "csv", label_visibility="collapsed")
        if upload_file1 is not None :
            csv_data_uploaded = pd.read_csv(upload_file1, encoding = 'ISO-8859-1')
            st.dataframe (csv_data_uploaded)
        clicked = st.button ("Click to Update Database")
        if clicked :
            update_csv (upload_file1)
            csv_data = csv_data_uploaded
            st.subheader ("List File CSV After Update")
            st.dataframe (csv_data)
        
        # Default Data CSV
        st.subheader ("Data CSV Used:")
        st.dataframe (csv_data, height = 200)
        
        # Choose Row and Coloumn
        st.subheader ("Write the Row :")
        choose_row = st.text_input ("Write the Row :", value = "Tweet", label_visibility="collapsed" )
        st.subheader ("Pick the Column :")
        values = st.slider('Select a range of values', 0, 500, (0, 1))
        st.write('Values:', values)
        a, b = values
                
        choose_row_series = csv_data[choose_row]
        
        selected_row = choose_row_series[a:(b+1)].tolist()
        text_data = ' '.join(selected_row)

         
    with col2: 
        # Input Text Used
        st.subheader ("Input Text Used :")
        st.text_area ("Input Text Used :", value = text_data, height =200, label_visibility ="collapsed" )
        st.write (f"Data Type :  {type(text_data)}")
        word_counts = ()

        text_data = lowercase (text_data)
        text_data = threeormore (text_data)
        text_data = stemming (text_data)
        text_data = tokenization (text_data)
        text_data = normalization (text_data)
        text_data = remove_number (text_data)
        text_data = remove_punctuation (text_data)
        text_data = stopwords (text_data)
        text_data = to_string (text_data)
        words = pd.Series(text_data.split())
        word_count = words.value_counts()
        st.success("Success to Run 'Execute Word Counter'", icon="✅")
    
    with col3:
        st.subheader ("Output text :")
        st.text_area ("Output text :", value = text_data, height = 200,label_visibility="collapsed")
        # Bar Chart
        st.subheader ("Bar Chart Top 5 Word :")
        top_5 = word_count[:5].reset_index()
        fig = plt.figure(figsize=(10,5))
        sns.barplot(x='index', y=0, data = top_5)
        st.pyplot(fig)
        # Word Cloud
        st.subheader ("Word Cloud :")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud = WordCloud(background_color = 'white').generate(text_data)
        plt.imshow(wordcloud)
        plt.axis('off')
        st.pyplot()

# Update Kamus Alay
if selected == "Update Kamus Alay":
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.subheader ("List Kamus Alay")
        st.dataframe (df_kamusalay)
        # Download Kamus Alay
        st.subheader ("Download Kamus Alay")
        @st.cache
        def convert_df(df):
            return df.to_csv(index_label=False).encode('utf-8')
            
        csv = convert_df(df_kamusalay)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='new_kamusalay.csv',
            mime='text/csv',)

    with col2 :
# Upload Kamus Alay
        st.subheader ("Update List Kamus Alay")
        upload_file2 = st.file_uploader ("Update List Kamus Alay", type = "csv", label_visibility="collapsed")
        if upload_file2 is not None :
            csv_data_uploaded = pd.read_csv(upload_file2, encoding = 'ISO-8859-1')
            st.dataframe (csv_data_uploaded)
        clicked = st.button ("Click to Update Database")
        if clicked :
            update_kamusalay (upload_file2)
            df_kamusalay = csv_data_uploaded
    with col3 :
        if clicked :
            st.subheader ("List Kamus Alay After Update")
            st.dataframe (df_kamusalay)

# Update Stopwords
if selected == "Update Stopwords":
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.subheader ("List Stopwords")
        st.dataframe (df_stopwords)

        # Download Stopwords
        st.subheader ("Download Stopwords")
        @st.cache
        def convert_df(df):
            return df.to_csv(index=False,index_label=False).encode('utf-8')
            
        csv = convert_df(df_stopwords)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='stopwordbahasa.csv',
            mime='text/csv',)
    with col2 :
# Upload File CSV
        st.subheader ("Update List Stopwords")
        upload_file3 = st.file_uploader ("Update List Stopwords", type = "csv", label_visibility="collapsed")
        if upload_file3 is not None :
            stopwords_uploaded = pd.read_csv(upload_file3, encoding = 'ISO-8859-1')
            st.dataframe (stopwords_uploaded)
        clicked = st.button ("Click to Update Database")
        if clicked :
            update_stopwords (upload_file3)
            df_stopwords = stopwords_uploaded
    with col3 :
        if clicked :
            st.subheader ("List Stopwords After Update")
            st.dataframe (df_stopwords)

# REFERENCES:
# 1. https://medium.com/product-ai/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
