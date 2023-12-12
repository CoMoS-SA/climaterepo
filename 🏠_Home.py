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

st.markdown("# Welcome to the Weighted Climate Data Repository Dashboard!")


"""
---
> 📚 12/12/2023: We have just released a preprint which describes the methodology behind the Weighted Climate Data Repository! Check it out [here](https://arxiv.org/abs/2312.05971)!
>
> 🎃 10/22/2023: Halloween update! We have introduced several backend improvements to make the dashboard faster! Also, we are now computing thresholds based on daily data!
>
> 📢 09/23/2023: We are thrilled to announce that our dashboard now offers DAILY data for specific gadm0 specifications! Check it out!
>
> 🤓 09/18/2023: Introducing *parquet* behind the scenes! Navigate through the dashboard and download data in a faster and more efficient way!
---
"""

"""
The Weighted Climate Data Repository (WCDR) provides a user-friendly dashboard to explore and download climate data weighted by measures of economic activity and aggregated at the national or subnational scale.
The dashboard allows users to:
* Choose to retrieve raw climate data about temperature, precipitation and SPEI (Standardized Precipitation-Evapotranspiration Index) from different sources and geographical/time resolutions;
* Weight raw climate data using alternative gridded measures of economic activity;
* Explore and download the resulting dataset in a single, accessible, and organized repository in a flexible way.

The project is run within the [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS](https://www.santannapisa.it/en/department-excellence/embeds) at [Sant'Anna School of Advanced Studies](https://www.santannapisa.it/en) (Pisa, Italy) by [Giorgio Fagiolo](https://sites.google.com/view/giorgiofagiolo/home), Marco Gortan, [Francesco Lamperti](http://www.francescolamperti.eu/) and [Lorenzo Testa](https://testalorenzo.github.io/).

## The Dashboard
Within the WCDR dashboard, the user can choose:
* *Climate variable*: available climate variables are temperature and precipitation (daily, monthly and annual observations) and SPEI (standardized precipitation-evapotranspiration index; monthly observations);
* *Data source*: we currently support data from [Climatic Research Unit (CRU TS)](https://www.uea.ac.uk/groups-and-centres/climatic-research-unit), [Delaware Climate Office](https://climate.udel.edu/), [ECMWF's ERA5](https://www.ecmwf.int/) and [CSIC](https://spei.csic.es/index.html);
* *Geographical resolution*: data can be downloaded at both the [GADM](https://gadm.org/) geographical resolution of GADM0 (World countries) and GADM1 administrative areas (i.e. regions within World countries);
* *Weighting type*: we provide the possibility of weighting climate data by measures of economic activity linking grid data to administrative units. There are currently three options: (i) **no weights** (i.e., download raw climate data); or weighting climate data by gridded (ii) **population density** from [NASA's SEDAC](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11); (iii) **night lights usage** (from [Li et al. 2020](https://www.nature.com/articles/s41597-020-0510-y));
* *Weighting year*: users can select the base year for the weighting variable according to which climate variables will be weighted;
* *Time resolution*: daily, monthly, and yearly observations can be employed;
* *Threshold*: If activated, this option allows to specify a threshold type (percentile or absolute value) and a threshold value for the historical time-series of a geographic unit; only days whose climate-variable observations are over the threshold value are retained.

Resulting data can be:
* Graphically explored as time series or using choropleth maps;
* Downloaded as *csv* or *json* files, in both **long** or **wide** data format.

Learn more about the WCDR by reading our [preprint](https://arxiv.org/abs/2312.05971)!

Users willing to run our pipelines on their own data are very welcome to reach out to us!

Stay tuned for updates!
"""

with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """