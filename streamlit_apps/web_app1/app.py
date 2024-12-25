# Core Pkgs
import streamlit as st

# NLP Pkgs
from textblob import TextBlob
import spacy
import neattext as nt

# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud

# Write a function that uses the spacy packages to extract Tokens and Lemmas from a sentence
def text_analyzer(my_text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
    return allData

def main():
    """NLP Based App with Streamlit """

    title_template = """
    <div style="background-color:blue; padding:8px;">
    <h1 style="color:cyan">NLP Web App</h1>
    </div>
    """

    st.markdown(title_template,unsafe_allow_html=True)

    subheader_template = """
    <div style="background-color:cyan; padding:8px;">
    <h3 style="color:blue">Powered by streamlit</h1>
    </div>
    """

    st.markdown(subheader_template,unsafe_allow_html=True)

    st.sidebar.image("logo.png",use_column_width=True)

    #st.title("NLP Web App")
    activity = ["Text Analysis","Translation","Sentiment Analysis","About"]
    choice = st.sidebar.selectbox("Menu", activity)

    if choice == "Text Analysis":
        st.subheader("Text Analysis")
        st.write("")
        raw_text = st.text_area("Write something..","Enter a text in english.", height=300)
        if st.button("Analyze"):
            if len(raw_text) == 0:
                st.warning("Please enter some text.")
            else:
                blob = TextBlob(raw_text)
                st.info("Basic Function")

                col1,col2 = st.columns(2)

                with col1:
                    with st.expander("Basic Info"):
                        st.info("Text Stats")
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {"Length of Text": word_desc['Length of Text'],
                                       "Num of Vowels": word_desc['Num of Vowels'],
                                       "Num of Consonants": word_desc['Num of Consonants'],
                                       "Num of Stopwords": word_desc['Num of Stopwords']}
                        st.write(result_desc)
                    with st.expander("Stopwords"):
                        st.success("Stop Words List")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)

                with col2:
                    with st.expander("Processed text.."):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)

                    with st.expander("Plot WordCloud"):
                        st.success("Wordcloud")
                        wordcloud = WordCloud().generate(processed_text)
                        fig = plt.figure(1, figsize=(20, 10))
                        plt.imshow(wordcloud, interpolation='bilinear')
                        plt.axis("off")
                        st.pyplot(fig)

                st.write("")
                st.write("")

                col3, col4 = st.columns(2)

                with col3:
                    with st.expander("Tokens&Lemmas"):
                        st.write("T&K")
                        processed_text = nt.TextFrame(raw_text).remove_stopwords()
                        processed_text = nt.TextFrame(processed_text.text).remove_puncts()
                        processed_text = nt.TextFrame(processed_text.text).remove_special_characters()
                        tkandlem = text_analyzer(processed_text.text)
                        st.json(tkandlem)

                with col4:
                    with st.expander("Summarize"):
                        st.success("Summarize")

    if choice == "Translation":
        st.subheader("Translation")
        st.write("")
    if choice == "Sentiment Analysis":
        st.subheader("Sentiment Analysis")
        st.write("")
    if choice == "About":
        st.subheader("About")
        st.write("")

    st.markdown("""
        ### NLP Web App made with Streamlit

        For info:

        - [streamlit](https://streamlit.io)
    """)

if __name__ == '__main__':
    main()
