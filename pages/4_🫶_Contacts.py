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

if 'initialized' in st.session_state:
        del st.session_state['initialized']

st.markdown("# The Weighted Climate Data Repository")
st.markdown("## Contacts")

"""
Feel free to send questions, bug reports, documentation issues, and other comments info@weightedclimatedata.com.

### Our Team

- Marco Gortan (marco [dot] gortan [at] unisg [dot] ch) 

- [Lorenzo Testa](https://testalorenzo.github.io) (l [dot] testa [at] sssup [dot] it)

- Giorgio Fagiolo (g [dot] fagiolo [at] sssup [dot] it)

- Francesco Lamperti (f [dot] lamperti [at] sssup [dot] it)

"""

cols = st.columns(2)
with cols[0]:
    st.image("LogoLEMbeDS.jpg", use_column_width=True)
with cols[1]:
    st.image("Inst.Economics.jpg", use_column_width=True)
    
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """