import streamlit as st

st.set_page_config(page_title="Weighted Climate Data Repository", page_icon="🌎", initial_sidebar_state="expanded")
st.markdown("# The Weighted Climate Data Repository")
st.markdown("## Guide")
st.warning("Page under construction!", icon="⚠️")

"""
* *geo_resolution*: choose among administrative units GADM0 (countries) and GADM1 (bigger administrative units after countries);
* *starting_year* and *ending_year*: window size. Notice that each source provides data for a peculiar time window;
* *time_frequency*: choose among yearly or monthly climate data;
* *source*: select source of data (available: CRU TS, UDelaware, HERA5, CSIC);
* *variable*: select variable of interest (available: temperature, precipitation, SPEI);
* *weight*: weight aggregation values by population density;
* *threshold_dummy*: True or False. Number of months over a given threshold for each year in the time window;
* *threshold_kind*: choose among a percentile or an absolute threshold;
* *threshold*: cutoff value.
"""

# Side bar images
# st.sidebar.image("Embeds logo.png", use_column_width=True)
# st.sidebar.image("download.jpeg", use_column_width=True)
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """