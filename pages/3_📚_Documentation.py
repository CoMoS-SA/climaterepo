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

bib = """@article{gortan2024climate,
title={A unified dataset for pre-processed climate indicators weighted by gridded economic activity},
author={Gortan, Marco and Testa, Lorenzo and Fagiolo, Giorgio and Lamperti, Francesco},
journal={Scientific Data},
year={2024},
url={https://www.nature.com/articles/s41597-024-03304-1},
volume={11},
number={533},
publisher={Nature Publishing Group UK London}
}"""

bib2 = """@inproceedings{gortan2024climate,
title={Climate Impact Assessment Requires Weighting: Introducing the Weighted Climate Dataset},
author={Gortan, Marco and Testa, Lorenzo and Fagiolo, Giorgio and Lamperti, Francesco},
booktitle={NeurIPS 2024 Workshop on Tackling Climate Change with Machine Learning},
url={https://www.climatechange.ai/papers/neurips2024/34},
year={2024}
}"""

with st.expander("References and Technical Details", expanded=True):
    """
    This is the original paper that describes the methodology behind the Weighted Climate Dataset:\n
    Gortan, M., Testa, L., Fagiolo, G., Lamperti, F., [**A unified dataset for pre-processed climate indicators weighted by gridded economic activity**](https://www.nature.com/articles/s41597-024-03304-1), *Scientific Data* 11, 533 (2024)\n

    Please remember to cite it if you use the data in your research!
    """
    st.download_button(label="Download BibTeX ", data = bib, file_name= 'bib.txt')
    """
    A follow-up paper that describes many new features has also been released:\n
    Gortan, M., Testa, L., Fagiolo, G., Lamperti, F., [**Climate Impact Assessment Requires Weighting: Introducing the Weighted Climate Dataset**](https://www.climatechange.ai/papers/neurips2024/34), *NeurIPS 2024 Workshop on Tackling Climate Change with Machine Learning* (2024)\n
    """
    st.download_button(label="Download BibTeX ", data = bib2, file_name= 'bib_neurips.txt')

with st.expander("GADM Abbreviations"):
    cols = st.columns(3)
    with cols[0]:
        countries = pd.read_csv('./poly/country_list.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM0", data=countries, file_name='gadm0.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/gadm1_adm.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM1", data=regions, file_name='gadm1.csv')
    with cols[2]:
        provinces = pd.read_csv('./poly/gadm2_adm.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM2", data=provinces, file_name='gadm2.csv')

with st.expander("NUTS Abbreviations"): 
    cols = st.columns(4)
    with cols[0]:
        countries = pd.read_csv('./poly/country_list_nuts0.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS0", data=countries, file_name='nuts0.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/country_list_nuts1.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS1", data=regions, file_name='nuts1.csv')
    with cols[2]:
        provinces = pd.read_csv('./poly/country_list_nuts2.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS2", data=provinces, file_name='nuts2.csv')
    with cols[3]:
        subprovinces = pd.read_csv('./poly/country_list_nuts3.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS3", data=subprovinces, file_name='nuts3.csv')

with st.expander("GADM aggregated weights"):
    cols = st.columns(3)
    with cols[0]:
        countries = pd.read_csv('./poly/gadm0_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM0", data=countries, file_name='gadm0_weights_values.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/gadm1_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM1", data=regions, file_name='gadm1_weights_values.csv')
    with cols[2]:
        provinces = pd.read_csv('./poly/gadm2_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download GADM2", data=provinces, file_name='gadm2_weights_values.csv')

with st.expander("NUTS aggregated weights"):
    cols = st.columns(4)
    with cols[0]:
        countries = pd.read_csv('./poly/nuts0_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS0", data=countries, file_name='nuts0_weights_values.csv')
    with cols[1]:
        regions = pd.read_csv('./poly/nuts1_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS1", data=regions, file_name='nuts1_weights_values.csv')
    with cols[2]:
        provinces = pd.read_csv('./poly/nuts2_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS2", data=provinces, file_name='nuts2_weights_values.csv')
    with cols[3]:
        subprovinces = pd.read_csv('./poly/nuts3_weights_values.csv').to_csv().encode('utf-8')
        st.download_button(label="Download NUTS3", data=subprovinces, file_name='nuts3_weights_values.csv')

with st.expander("GADM economic data"):
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