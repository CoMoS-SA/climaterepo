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

st.markdown("# Welcome to the Weighted Climate Dataset Dashboard!")


"""
---
> 🚀 4/25/2025: We are sharing new data at the GADM world resolution! This new feature allows users to explore and download data at the most aggregated spatial detail.
>
> 📚 12/10/2024: The paper describing many of the new features of our Weighted Climate Dataset has been released in the NeurIPS 2024 Workshop on Tackling Climate Change with Machine Learning! Check it out [here](https://www.climatechange.ai/papers/neurips2024/34)!
>
> 📆 10/29/2024: We are going to present our work at the [NeurIPS 2024 Workshop on Tackling Climate Change with Machine Learning](https://www.climatechange.ai/events/neurips2024). The workshop will take place on December 15, 2024!
>
> 💨 7/23/2024: We released a new climate variable from ERA5: instantaneous wind gusts are now available on our dashboard! 
>
> 📟 7/22/2024: We have switched to Google Cloud Storage (GCS): access to data is now faster, more robust and secure. Thanks to our migration to GCS, we are now able to release new daily climate indicators. Check out the minimum and maximum temperatures!
>
> 📚 5/24/2024: The paper describing the methodology behind the Weighted Climate Dataset has been published on Nature Scientific Data! Check it out [here](https://www.nature.com/articles/s41597-024-03304-1)!
---
"""

"""
The Weighted Climate Dataset provides a user-friendly dashboard to explore and download climate data weighted by measures of economic activity and aggregated at the national and subnational scale.
The dashboard allows users to:
* Choose to retrieve raw climate data about (minimum, average, and maximum) temperature, precipitation, instantaneous wind gust, and SPEI (Standardized Precipitation-Evapotranspiration Index) from different sources and geographical/time resolutions;
* Weight raw climate data using alternative gridded measures of economic activity;
* Explore and download the resulting dataset in a single, accessible, and organized repository in a flexible way.

The project is run within the [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS](https://www.santannapisa.it/en/department-excellence/embeds) at [Sant'Anna School of Advanced Studies](https://www.santannapisa.it/en) (Pisa, Italy) by [Giorgio Fagiolo](https://sites.google.com/view/giorgiofagiolo/home), [Marco Gortan](https://www.linkedin.com/in/marco-gortan/), [Francesco Lamperti](http://www.francescolamperti.eu/), and [Lorenzo Testa](https://testalorenzo.github.io/).

## The Dashboard
Within the Weighted Climate Dataset dashboard, the user can choose:
* *Climate variable*: available climate variables are (minimum, average, and maximum) temperature, precipitation, and instantaneous wind gust (daily, monthly and annual observations), and SPEI (standardized precipitation-evapotranspiration index; monthly observations);
* *Data source*: we currently support data from [Climatic Research Unit (CRU TS)](https://www.uea.ac.uk/groups-and-centres/climatic-research-unit), [Delaware Climate Office](https://climate.udel.edu/), [ECMWF's ERA5](https://www.ecmwf.int/) and [CSIC](https://spei.csic.es/index.html);
* *Geographical resolution*: data can be downloaded at the [GADM](https://gadm.org/) geographical resolution of GADM World (whole Planet), GADM0 (World countries), and GADM1 (i.e. largest administrative units within World countries);
* *Weighting type*: we provide the possibility of weighting climate data by measures of economic activity linking grid data to administrative units. There are currently five options: (i) **no weights** (i.e., download raw climate data); or weighting climate data by gridded (ii) **population density** from [NASA's SEDAC](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11); (iii) **night lights usage** (from [Li et al. 2020](https://www.nature.com/articles/s41597-020-0510-y)); (iv)  **cropland use** (from [HYDE](https://www.pbl.nl/en/hyde-history-database-of-the-global-environment)); (v) **concurrent population count** (from [HYDE](https://www.pbl.nl/en/hyde-history-database-of-the-global-environment)).
* *Weighting year*: users can select the base year for the weighting variable according to which climate variables will be weighted;
* *Time resolution*: daily, monthly, and yearly observations can be employed;
* *Threshold*: If activated, this option allows to specify a threshold type (percentile or absolute value) and a threshold value for the historical time-series of a geographic unit; only days whose climate-variable observations are over the threshold value are retained.

Resulting data can be:
* Graphically explored as time series or using choropleth maps;
* Downloaded as *csv* or *json* files, in both **long** or **wide** data format.

Learn more about the Weighted Climate Dataset by reading our [paper](https://www.nature.com/articles/s41597-024-03304-1)!

Users willing to run our pipelines on their own data are very welcome to reach out to us!

Stay tuned for updates!
"""

with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """