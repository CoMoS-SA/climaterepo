import streamlit as st

st.set_page_config(page_title="Weighted Climate Data Repository", page_icon="🌎")

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
st.markdown("## Documentation")

"""
This is the paper that describes the methodology behind the Weighted Climate Data Repository:

[**A unified repository for pre-processed climate data weighted by gridded economic activity**](https://www.google.it)

Please remember to cite it if you use the data in your research!
"""

# Side bar images
# st.sidebar.image("Embeds logo.png", use_column_width=True)
# st.sidebar.image("download.jpeg", use_column_width=True)
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """