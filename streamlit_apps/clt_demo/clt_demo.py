import streamlit as st
st.title("Streamlit Basics")
#st.header("This is the header")
#st.subheader("This is the subheader")
#st.text("This is the text")
#st.write("This is the write dimensiom")
#st.markdown("[This is the markdown](https://www.google.com)")

html_page = """
<div style="background-color:blue;padding:50px">
<p style="color:yellow;font-size:50px">Enjoy Streamlit!</p>
</div>
"""

#st.markdown(html_page, unsafe_allow_html=True)

#st.success("This is the success message")
#st.info("This is the info message")
#st.warning("This is the warning message")
#st.error("This is the error message")

#from PIL import Image
#img = Image.open("bus.jpg")
#st.image(img, caption="This is the image", width=500)

# Using a URL for video playback
# st.video("https://www.youtube.com/watch?v=q2EqJW8VzJo")

#if st.button("Play"):
#    st.text("hello world...")

#if st.checkbox("Checkbox"):
#    st.text("Checkbox selected")

#radio_but = st.radio("Your Selection", ["A", "B"])
#if radio_but == "A":
#    st.info("You selected A")
#else:
#    st.info("You selected B")

#city = st.selectbox("Your City", ["Napoli", "Palermo", "Catania"])

#occupation = st.multiselect("Your Occupation", ["Programmer", "Data Scientist", "IT Consultant", "DBA"])

#Name = st.text_input("Your Name", "Write something…")
#st.text(Name)

#Age = st.number_input("Your Age", 1, 100)

#message = st.text_area("Your Message", "Write something…")

#select_val = st.slider("Select a Value", 1, 10)

#if st.button("Balloons"):
#    st.balloons()

import pandas as pd

st.header("Dataframes and Tables")
df = pd.read_csv("auto.csv")
st.dataframe(df.head(10))
st.table(df.head(10))

st.area_chart(df[["mpg","cylinders"]])

st.bar_chart(df[["mpg","cylinders"]].head(20))

st.line_chart(df[["mpg","cylinders"]].head(20))

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
corr_plot = sns.heatmap(df[["mpg","cylinders", "displacement"]].corr(), annot= True)
st.pyplot(fig)

import datetime

today = st.date_input("Today is",datetime.datetime.now())

import time

hour = st.time_input("The time is", datetime.time())

data = {"name":"John","surname":"Wick"}
st.json(data)

st.code("import pandas as pd")

import time
my_bar = st.progress(0)
for value in range(100):
    time.sleep(0.01)
    my_bar.progress(value+1)

import time
with st.spinner("Please wait..."):
    time.sleep(1)
st.success("Done!")