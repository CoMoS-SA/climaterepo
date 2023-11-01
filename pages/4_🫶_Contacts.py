import streamlit as st

st.set_page_config(page_title="Weighted Climate Data Repository", page_icon="🌎", initial_sidebar_state="expanded")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown("# The Weighted Climate Data Repository")
st.markdown("## Contacts")

"""
Feel free to send questions, bug reports, documentation issues, and other comments to Marco Gortan (marco.gortan@unisg.ch) and [Lorenzo Testa](https://testalorenzo.github.io) (l.testa@sssup.it)
"""

cols = st.columns(2)
with cols[0]:
    st.image("Embeds logo.png", use_column_width=True)
with cols[1]:
    st.image("download.jpeg", use_column_width=True)
    
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """