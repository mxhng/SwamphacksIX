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
from cloudVisionTest import main, vLikely, percentLikely, total, likely, possible
import imageHTML 
from nlpTest import nlpCategorize

st.set_page_config(page_title="Sus or Safe", page_icon="resources/mzgmqc1qc3t51.png", layout="wide")

col1, col2 = st.columns([4,1], gap="large")

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

with col1:
    #HEADER
    st.markdown('<p class="big-font">Sus or Safe?</p>', unsafe_allow_html=True)

    #SEARCH BAR
    url = st.text_input("Enter Website URL Here :point_down:", placeholder="https://www.ufl.edu/")
    #st.write("this is the url: " + url)

    if(url != ""):

        badbad = False
        hasSensitive = False

        
        # Using NLP on the url and displaying the interpretation

        nlpTags = nlpCategorize(url)
        
        for key in nlpTags:
            if key == "/Adult" or key=="/Sensitive Subjects":
                hasSensitive = True
        if hasSensitive:
            st.markdown("**:red[We have detected something sus.]**")
        for key in nlpTags:
            if(key[1:len(key)] == "Sensitive Subjects" or key[1:len(key)] == "Adult"): 
                pctg = '<string style="font-size: 20px; color:Red">' + nlpTags[key] + '%</string>'
                badbad = True
            else:
                pctg = '<string style="font-size: 20px; color:Green">' + nlpTags[key] + '%</string>'
            st.markdown("We are " + pctg + " confident that this website is about " + key[1:len(key)] + ".", unsafe_allow_html=True)


        # Running Cloud Vision on all images in url
        main(url)
        veryLikely = vLikely()
        isPossible = possible()
        isLikely = likely()
        percentages = percentLikely()

        st.write(str(total()) + " images were discovered.")
        st.write("Images contain the following types of content:")

        # Assigning data from Cloud Vision processing
        racynum = percentages[4]
        spoofednum = percentages[2]
        violencenum = percentages[3]
        adultnum = percentages[0]
        medicalnum = percentages[1]
        categories = [racynum, spoofednum, violencenum, adultnum, medicalnum]
        categories2 = [racynum*100, spoofednum*100, violencenum*100, adultnum*100, medicalnum*100]


        # Displaying image data to the user
        for i in range(5): 
            temp = categories.index(max(categories))

            if(max(categories) == racynum): 
                st.subheader("Racy:  " + "%.2f" % (racynum * 100)  + "% of images are possibly, likely, or very likely to be racy")
                st.progress(racynum)
                st.write("\t" + str(veryLikely[4]) + " images are very likely, " + str(isLikely[4]) + " images are likely, and " + str(isPossible[4]) + " are possibly racy.") 
                racynum = -1
        
            elif (max(categories) == spoofednum):
                st.subheader("Spoofed: " + "%.2f" % (spoofednum * 100) + "% of images are possibly, likely, or very likely to be spoofed")
                st.progress(spoofednum)
                st.write("\t" + str(veryLikely[2]) + " images are very likely, " + str(isLikely[2]) + " images are likely, and " + str(isPossible[2]) + " are possibly spoofed.") 
                spoofednum = -1

            elif(max(categories) == violencenum):
                st.subheader("Violence: " + "%.2f" % (violencenum * 100) + "% of images are possibly, likely, or very likely to be violent")
                st.progress(violencenum)
                st.write("\t" + str(veryLikely[3]) + " images are very likely, " + str(isLikely[3]) + " images are likely, and " + str(isPossible[3]) + " are possibly violent.") 
                violencenum = -1

            elif(max(categories) == adultnum):
                st.subheader("Adult: " + "%.2f" % (adultnum * 100) + "% of images are possibly, likely, or very likely to be adult")
                st.progress(adultnum)
                st.write("\t" + str(veryLikely[0]) + " images are very likely, " + str(isLikely[0]) + " images are likely, and " + str(isPossible[0]) + " are possibly adult.") 
                adultnum = -1

            elif(max(categories) == medicalnum):
                st.subheader("Medical: " + "%.2f" % (medicalnum * 100)+ "% of images are possibly, likely, or very likely to be medical")
                st.progress(medicalnum)
                st.write("\t" + str(veryLikely[1]) + " images are very likely, " + str(isLikely[1]) + " images are likely, and " + str(isPossible[1]) + " are possibly medical.") 
                medicalnum = -1
            
            categories.pop(temp)

    else:
        st.write("No information to show.")
        st.write(":exclamation: Please wait for data to load :exclamation:")
        

# Determining what icon to display based on NLP and CV data
with col2:
    if(url != ""):
        superbadbad = False
        for i in range(5):
            #st.write(str(categories2[i]))
            if(categories2[i] >= 60):
                superbadbad = True
        if(badbad == True or superbadbad == True):
            st.subheader("Safety:????")
            st.image("resources/Stop.png", width=250)
        else:
            printed = False
            for i in range(5):
                if(categories2[i] >= 20):
                    st.subheader("Safety:??????")
                    st.image("resources/5a81af7d9123fa7bcc9b0793.png", width=250)
                    printed = True
                    break
            if printed == False:
                st.title("Safety::smile:")
                st.image("resources/smiley.png", width=250)