import streamlit as st

st.set_page_config(page_title="Weighted Climate Dataset", page_icon="🌎", initial_sidebar_state="expanded")

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

st.markdown("# The Weighted Climate Dataset")
st.markdown("## Contacts")

"""
Feel free to send us questions, bug reports, documentation issues, and other comments. You can find our contact information below.

### Our Team

- [Marco Gortan](https://www.linkedin.com/in/marco-gortan/) (marco [dot] gortan [at] unibas [dot] ch) 

- [Lorenzo Testa](https://testalorenzo.github.io) (l [dot] testa [at] santannapisa [dot] it)

- [Giorgio Fagiolo](https://sites.google.com/view/giorgiofagiolo) (g [dot] fagiolo [at] santannapisa [dot] it)

- [Francesco Lamperti](http://www.francescolamperti.eu/) (f [dot] lamperti [at] santannapisa [dot] it)

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