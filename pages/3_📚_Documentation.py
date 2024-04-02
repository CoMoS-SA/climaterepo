import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weighted Climate Dataset", page_icon="🌎")

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
st.markdown("## Documentation")

bib = """@article{gortan2023climate,
title={A unified repository for pre-processed climate data weighted by gridded economic activity},
author={Gortan, Marco and Testa, Lorenzo and Fagiolo, Giorgio and Lamperti, Francesco},
journal={ArXiv:2312.05971},
year={2023},
url={https://arxiv.org/abs/2312.05971},
}"""

with st.expander("References and Technical Details", expanded=True):
    """
    This is the paper that describes the methodology behind the Weighted Climate Dataset:\n
    Gortan, M., Testa, L., Fagiolo, G., Lamperti, F., [**A unified repository for pre-processed climate data weighted by gridded economic activity**](https://arxiv.org/abs/2312.05971), *ArXiv:2312.05971* (2023)\n
    Please remember to cite it if you use the data in your research!
    """
    st.download_button(label="Download BibTeX", data = bib, file_name= 'bib.txt')

with st.expander("GADM abbreviations"):
    cols = st.columns(2)
    with cols[0]:
        countries = pd.read_csv('./poly/country_list.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM0", data=countries, file_name='gadm0.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/gadm1_adm.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM1", data=regions, file_name='gadm1.csv')

with st.expander("Aggregated weights"):
    cols = st.columns(2)
    with cols[0]:
        countries = pd.read_csv('./poly/gadm0_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM0", data=countries, file_name='gadm0_weights_values.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/gadm1_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM1", data=regions, file_name='gadm1_weights_values.csv')

with st.expander("Economic data"):
    """
    The GADM0 GDP data are from the [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD), and are measured in current dollars. The GADM1 GRP data are from [Wenz et al. (2023)](https://www.nature.com/articles/s41597-023-02323-8), and are measured in 2015 dollars.
    """
    cols = st.columns(2)
    with cols[0]:
        countries = pd.read_csv('./poly/gadm0_gdp.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM0", data=countries, file_name='gadm0_gdp.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/gadm1_gdp.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM1", data=regions, file_name='gadm1_gdp.csv')

# Side bar images
# st.sidebar.image("Embeds logo.png", use_column_width=True)
# st.sidebar.image("download.jpeg", use_column_width=True)
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """