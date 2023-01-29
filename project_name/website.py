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
from cloudVisionTest import main, vLikely, percentLikely, total
import imageHTML 
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
    st.markdown('<p class="big-font">Sus or Safe?</p>', unsafe_allow_html=True)
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

        #NLP STUFF
        nlpTags = nlpCategorize(url)
        hasSensitive = False
        for key in nlpTags:
            if key == "/Adult" or key=="/Sensitive Subjects":
                hasSensitive = True
        if hasSensitive:
            st.write("We detected something sus.")

        for key in nlpTags:
            pctg = '<string style="font-size: 20px; color:Red">' + nlpTags[key] + '%</string>'
            st.markdown("We are " + pctg + " confident that this website is about " + key[1:len(key)] + ".", unsafe_allow_html=True)
        
        #VISION STUFF
        #PERCENTAGE BARS
        #racy, spoofed, violence, adult, medical
        #racynum = veryLikely[4]
        main(url)
        veryLikely = vLikely()
        percentages = percentLikely()

        st.write(str(total()) + " images were discovered.")
        st.write("Images contain the following types of content:")

        racynum =  percentages[4]
        spoofednum = percentages[2]
        violencenum = percentages[3]
        adultnum = percentages[0]
        medicalnum = percentages[1]
        categories = [racynum, spoofednum, violencenum, adultnum, medicalnum]

        for i in range(5): 
            temp = categories.index(max(categories))
            #st.write(str(temp))
            #st.write("max: " + str(max(categories)))

            if(max(categories) == racynum): 
                st.subheader("Racy:  " + "%.2f" % racynum + "% of images are possibly, likely, or very likely to be racy")
                st.progress(racynum/100)
                st.write("\t" + str(veryLikely[4]) + " images are very likely to be racy.") 
                racynum = -1
        
            elif (max(categories) == spoofednum):
                st.subheader("Spoofed: " + "%.2f" % spoofednum + "% of images are possibly, likely, or very likely to be spoofed")
                st.progress(spoofednum/100)
                st.write("\t" + str(veryLikely[2]) + " images are very likely to be spoofed.")
                spoofednum = -1

            elif(max(categories) == violencenum):
                st.subheader("Violence: " + "%.2f" % violencenum + "% of images are possibly, likely, or very likely to be violent")
                st.progress(violencenum/100)
                st.write("\t" + str(veryLikely[3]) + " images are very likely to be violent.")
                violencenum = -1

            elif(max(categories) == adultnum):
                st.subheader("Adult: " + "%.2f" % adultnum + "% of images are possibly, likely, or very likely to be adult")
                st.progress(adultnum/100)
                st.write("\t" + str(veryLikely[0]) + " images are very likely to be adult.")
                adultnum = -1

            elif(max(categories) == medicalnum):
                st.subheader("Medical: " + "%.2f" % medicalnum + "% of images are possibly, likely, or very likely to be medical")
                st.progress(medicalnum/100)
                st.write("\t" + str(veryLikely[1]) + " images are very likely to be medical.")
                medicalnum = -1
            
            categories.pop(temp)
            #for category in categories:
                #st.write(str(category))

    else:
        st.write("No information to show.")
        
    #TEST WITH OUTSIDE FILES
    #text = trivialFunction(url)
    #st.write(text)

with col2:
    if(url != ""):
        rating = "badbad"
        if rating == "great":
            st.title("Safety:")
            st.image("resources/smiley.png", width=250)
        if rating == "iffy":
            st.subheader("Safety::warning:")
            st.image("resources/5a81af7d9123fa7bcc9b0793.png", width=250)
        if rating == "badbad": 
            st.subheader("Safety::octagonal_sign:")
            st.image("resources/Stop.png", width=250)

#ERROR
#e = RuntimeError('HTML Link Invalid')
#st.exception(e)

#TO DO: make bars on same line as text, center image, make error for invalid html 
