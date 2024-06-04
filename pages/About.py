import streamlit as st

from utils.custom_css import custom_css
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='❓')
custom_css()
show_main_menu(_)
st.header('About FunGA', divider=True)
st.write("Repository: [GitHub link](https://github.com/ticklish-caiman/FunGA)")
st.image('img/funga_img03.png')
st.write(
    _("The project was created using the Streamlit framework. The premise was simple: I focus on the back-end, "
      "so it\'s best to automate the front-end creation as much as possible. I chose Streamlit because it\'s a pure "
      "Python approach. Each page is rendered based on Python code \"from top to bottom\" with every change in variable "
      "values. This has its limitations. I bent over backwards to create a dynamic user interface for the \"TSP\"... "
      "and the result is quite poor. The idea of Streamlit is very tempting, and the project is constantly being "
      "developed and gaining functionality. However, it\'s important to carefully analyze whether its current features "
      "are enough to fulfill the project\'s goals. After 100 days of creating the project, I planned to deliver three "
      "games - I didn't succeed. I don\'t blame Streamlit for this (after all, I chose it myself), but struggling with "
      "its limitations, combined with overly ambitious game ideas and lack of time (new job), ultimately led to my "
      "failure. The two-dimensional knapsack problem with visualization turned out to be much more difficult to "
      "implement than I anticipated. The idea of something \"like Stable Diffusion\" based on genetic algorithms was "
      "complete madness - I tried to \"evolve\" shapes from noise. Unfortunately, choosing the right fitness function "
      "proved to be problematic. Something would occasionally come out, but I eventually abandoned the idea. Well... we"
      "have TSP and my interpretation of Biomorphs. Both games still need some polishing. What will the future of the "
      "project be? I don't know. It's possible that I'll finish it in its current form. It's also possible that, "
      "enriched with new experiences, I'll create something similar from scratch. Time will tell :)"))

st.header('About me', divider=True)

st.write(
    _("I am a graduate of the University of Silesia in Katowice, Poland, and currently work as an IT specialist in a "
      "large logistics company. My responsibilities are broad, including fixing computer hardware and software, "
      "troubleshooting networking issues, and developing scripts and software for internal use. My current job "
      "requires me to be on-site daily and doesn't offer significant opportunities for professional growth. Therefore, "
      "I am seeking a position as a software developer or data analyst where I can further develop my skills and "
      "advance my career."))

st.header(_('Contact'), divider=True)

col1, col2 = st.columns(2)
with col1:
    st.write(_('My LinkedIn:'))
    st.markdown(
        f"""[<img src="https://media.licdn.com/dms/image/D4E12AQEud3Ll5MI7cQ/article-inline_image-shrink_1500_2232/0/1660833954461?e=1723075200&v=beta&t=LopQK91BgUYaQJPJnq4GkxeZBL0z0dnz2gTaPziZxqU" width=200px 
        style="background-color:grey" >](https://www.linkedin.com/in/michal-stanicki/)""",
        True)
with col2:
    st.write(_('My Github:'))
    st.markdown(
        f"""[<img src="https://avatars.githubusercontent.com/u/91501936?v=4" width=200px 
        style="background-color:grey" >](https://github.com/ticklish-caiman)""",
        True)


st.header('100Commitów', divider=True)
st.text(_('This project takes part in:'))
st.markdown(
    f"""[<img src="https://100commitow.pl/img/100-comittow_long.png" width=400px >](https://100commitow.pl/)""",
    True)
st.text('Competition organized by:')
st.markdown(
    f"""[<img src="https://100commitow.pl/img/devmentors-logo.png" width=400px 
    style="background-color:grey" >](https://devmentors.io/)""",
    True)
st.divider()
