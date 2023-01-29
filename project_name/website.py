#Configurations
#download anaconda
#create an environment
#open environment terminal
#pip install streamlit
#streamlit hello
#makesure streamlit is not on laptop by running pip uninstall streamlit and checking it with pip list and conda list
#run with 'python -m streamlit run your_script.py' in cmd when in file directory
import streamlit as st
import base64
#from test import trivialFunction
#import cloudVisionTest
#import imageHTML 
import nlpTest
from nlpTest import nlpCategorize

st.set_page_config(page_title="Sus or Safe", page_icon="resources/mzgmqc1qc3t51.png", layout="wide")

col1, col2 = st.columns([3,1])

st.markdown("""
<style>
.big-font {
    font-size:80px;
    font-family:Monospace;
}
</style>
""", unsafe_allow_html=True)

#BACKGROUND 
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
#add_bg_from_local('resources/blank-wall-psd-japandi-living-room-interior_53876-109284.jpg')   

with col1:
    #HEADER
    st.markdown('<p class="big-font">Sus or Safe</p>', unsafe_allow_html=True)
    #st.title("SUS or SAFE")

    #BUTTON
    #result = st.button("This is a button")
    #st.write(result)
    #if result:
    #    st.write(":smile:")

    #SEARCH BAR
    url = st.text_input("Enter Website URL Here :point_down:", placeholder="https://www.ufl.edu/")
    #st.write("this is the url: " + url)

    if(url != ""):

        #main(url)
        #veryLikely = vLikely()
        #NLP STUFF
        result = nlpCategorize(url)
        print(result.values())
        st.write("This website is described as: [TONY STUFF]")
        
        #VISION STUFF
        st.write("Images contain the following types of content:")
        
        #PERCENTAGE BARS
        #racy, spoofed, violence, adult, medical
        #racynum = veryLikely[4]

        racynum = 5
        spoofednum = 10
        violencenum = 40
        adultnum = 70
        medicalnum = 100


        st.subheader("Racy:  " + str(racynum) + "%")
        st.write("\t" + str(racynum) + " images are very likely to be racy.") 
        st.progress(racynum)
        
        st.subheader("Spoofed: " + str(spoofednum) + "%")
        st.write("\t" + str(spoofednum) + " images are very likely to be spoofed.")
        st.progress(spoofednum)
        
        st.subheader("Violence: " + str(violencenum) + "%")
        st.write("\t" + str(violencenum) + " images are very likely to be violent.")
        st.progress(violencenum)
        
        st.subheader("Adult: " + str(adultnum) + "%")
        st.write("\t" + str(adultnum) + " images are very likely to be adult.")
        st.progress(adultnum)
        
        st.subheader("Medical: " + str(medicalnum) + "%")
        st.write("\t" + str(medicalnum) + " images are very likely to be medical.")
        st.progress(medicalnum)
        
    else:
        st.write("No information to show.")
        
    #TEST WITH OUTSIDE FILES
    #text = trivialFunction(url)
    #st.write(text)

with col2:
    if(url != ""):
        rating = "great"
        if rating == "great":
            st.title("Safety:")
            st.image("resources/smiley.png", width=300)
        if rating == "iffy":
            st.subheader("Safety::warning:")
        if rating == "badbad": 
            st.subheader("Safety::octagonal_sign:")

#ERROR
#e = RuntimeError('HTML Link Invalid')
#st.exception(e)

#TO DO: make bars on same line as text, center image, make error for invalid html 