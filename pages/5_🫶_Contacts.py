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
"""

st.markdown("## Our team")

cols = st.columns(4)
with cols[0]:
    st.image("fgx/marco.png", use_column_width='auto')
    """[Marco Gortan](https://www.linkedin.com/in/marco-gortan/) [✉️](mailto:marco.gortan@unibas.ch)"""
with cols[1]:
    st.image("fgx/lorenzo.png", use_column_width='auto')
    """[Lorenzo Testa](https://testalorenzo.github.io) [✉️](mailto:lorenzo@stat.cmu.edu)"""
with cols[2]:
    st.image("fgx/giorgio.png", use_column_width='auto')
    """[Giorgio Fagiolo](https://sites.google.com/view/giorgiofagiolo) [✉️](mailto:g.fagiolo@santannapisa.it)"""
with cols[3]:
    st.image("fgx/francesco.png", use_column_width='auto')
    """[Francesco Lamperti](http://www.francescolamperti.eu/) [✉️](mailto:f.lamperti@santannapisa.it)"""

cols = st.columns(2)
with cols[0]:
    st.image("fgx/LogoLEMbeDS.jpg", use_column_width=True)
with cols[1]:
    st.image("fgx/Inst.Economics.jpg", use_column_width=True)
    
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """