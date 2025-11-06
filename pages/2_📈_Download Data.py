# ------------ #
# Download tab #
# ------------ #

import streamlit as st
import pandas as pd
import numpy as np
import duckdb as db
import pickle

# --------------------- #
# Initial Session State #
# --------------------- #

if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    st.session_state['variable'] = 'avg. temperature'
    st.session_state['source'] = 'CRU TS'
    st.session_state['geo_resolution'] = 'gadm0'
    st.session_state['weight'] = 'population density'
    st.session_state['weight_year'] = '2015'
    st.session_state['threshold_dummy'] = 'False'
    st.session_state['threshold_kind'] = 'percentile'
    st.session_state['threshold'] = 90
    st.session_state['time_frequency'] = 'monthly'
    st.session_state['starting_year'] = 1951
    st.session_state['ending_year'] = st.session_state.starting_year + 1
    st.session_state['row_range'] = tuple(['USA'])

# ------------ #
# Data imports #
# ------------ #

@st.cache_data(ttl=180, show_spinner="Fetching country names...")
def load_country_list():
    """
    Load country list from the repository and return a pandas dataframe

    Returns:
    country_list (pandas dataframe): Dataframe containing the country list
    """
    country_list = pd.read_csv('./poly/country_list.csv')
    return country_list

@st.cache_data(ttl=180, show_spinner="Fetching data...")
def load_data(geo_resolution, variable, source, weight, weight_year, row_range, col_range, time_frequency, threshold_dummy):
    if weight == 'un' or weight == 'concurrent':
        weight_year = ''

    if time_frequency in ('yearly','monthly'):
        freq = 'monthly'
        time_idx = pd.date_range(start=str(st.session_state.starting_year) + "-01-01",
                                 end= str(st.session_state.ending_year) + "-12-31", freq='MS')
    if time_frequency == 'daily' or threshold_dummy == "True":
        freq = 'daily'
        time_idx = pd.date_range(start=str(st.session_state.starting_year) + "-01-01",
                                 periods=len(row_range), freq='D')

    if col_range == '*':
        cols = '*'
    else:
        if geo_resolution == 'gadm_world':
            cols = '*'
        if geo_resolution == 'gadm0':
            cols = str(col_range)[1:-1].replace("'", "")
        elif geo_resolution == 'gadm1':
            regions = pd.read_csv('./poly/gadm1_adm.csv')
            cols = regions.loc[regions.GID_0.isin(col_range), 'GID_1'].tolist()
            cols = str(cols)[1:-1].replace("'", "").replace(".", "_")
        else:
            provinces = pd.read_csv('./poly/gadm2_adm.csv')
            cols = provinces.loc[provinces.GID_0.isin(col_range), 'GID_2'].tolist()
            cols = str(cols)[1:-1].replace("'", "").replace(".", "_")

    db.sql('INSTALL httpfs')
    db.sql('LOAD httpfs')
    db.sql("SET s3_endpoint='storage.googleapis.com'")
    db.sql("SET s3_access_key_id=" + st.secrets['duckdb']['id'])
    db.sql("SET s3_secret_access_key=" + st.secrets['duckdb']['password'])

    # file = 'https://gitlab.com/climate-project1/climate-data-test/-/raw/main/' + geo_resolution + '_' + source + '_' + variable + '_' + weight + '_' + weight_year + '_' + freq + '.parquet'
    file = 's3://climatedata_bucket/' + geo_resolution + '_' + source + '_' + variable + '_' + weight + '_' + weight_year + '_' + freq + '.parquet'

    query = f"SELECT {cols} FROM '{file}' WHERE Date IN {row_range}"
    imported_data = db.query(query).fetch_arrow_table() #.df()
    imported_data = imported_data.to_pandas()
    imported_data.index = time_idx

    return imported_data

@st.cache_data(ttl=180, show_spinner="Fetching shapes...")
def load_shapes(geo_resolution):
    """
    Load shapefiles from the repository and return a geopandas dataframe

    Parameters:
    geo_resolution (str): Geographical resolution of the data

    Returns:
    world (geopandas dataframe): Geopandas dataframe containing the gadm0 shapes
    """
    if geo_resolution == 'gadm0':
        layer = '0'
        idx_name = 'GID_0'
    elif geo_resolution == 'gadm1':
        layer = '1'
        idx_name = 'NAME_1'
    else:
        layer = '2'
        idx_name = 'NAME_2'

    picklefile = open('./poly/gadm' + layer + '.pickle', 'rb')
    shapes = pickle.load(picklefile)
    shapes.index = shapes[idx_name]
    picklefile.close()
    return shapes.reset_index(drop=True)

# ----- #
# Utils #
# ----- #

info = {'cru': 'DOI: 10.1038/s41597-020-0453-3',
        'era': 'DOI: 10.1002/qj.3803',
        'csic': 'DOI: 10.1175/2009JCLI2909.1',
        'dela': 'https://climate.geog.udel.edu/',
        'tmp': 'measured in °C',
        'tmpmin': 'measured in °C',
        'tmpmax': 'measured in °C',
        'pre': 'measured in mm',
        'gust': 'measured in m/s',
        'spei': 'unitless',
        'lights': 'DOI: 10.1038/s41597-020-0510-y',
        'pop': 'DOI: 10.1080/23754931.2015.1014272',
        'concurrent': 'DOI: 10.17026/dans-25g-gez3',
        'cropland': 'DOI: 10.17026/dans-25g-gez3',
        'un': 'no external source needed'}

# ------------- #
# Page settings #
# ------------- #

st.set_page_config(page_title="Weighted Climate Dataset", page_icon="🌎")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("# The Weighted Climate Dataset")
st.markdown("## Download Data")

# ---------- #
# Parameters #
# ---------- #

# Cols
col1, col2, col3, col4, col5 = st.columns([1,1,1.3,1.1,1])
if st.session_state['variable'] != 'SPEI':
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

# Climate variable
if st.session_state.geo_resolution != 'gadm_world' and st.session_state.geo_resolution != 'gadm2':
    with col1:
        st.selectbox('Climate variable', ("avg. temperature", "min. temperature", "max. temperature", "precipitation", "SPEI", "max. wind gust"),
                    index=0, help='Measured climate variable of interest', key='variable')
else:
    with col1:
        st.selectbox('Climate variable', ("avg. temperature", "min. temperature", "max. temperature", "precipitation"),
                    index=0, help='Measured climate variable of interest', key='variable')

# Variable source
if st.session_state.geo_resolution != 'gadm_world' and st.session_state.geo_resolution != 'gadm2' and st.session_state.variable != "SPEI" and st.session_state.variable != "min. temperature" and st.session_state.variable != "max. temperature" and st.session_state.variable != "max. wind gust":
    with col2:
        st.selectbox('Variable source', ("CRU TS", "ERA5", "UDelaware"), index=0,
                     help='Source of data for the selected climate variable', key='source')
elif st.session_state.variable == "SPEI":
    with col2:
        st.caption("Variable source")
        st.markdown("CSIC")
        st.session_state.source = 'CSIC'
else: 
    with col2:
        st.caption("Variable source")
        st.markdown("ERA5")
        st.session_state.source = 'ERA5'

# Geographical resolution
with col3:
    st.selectbox('Geographical resolution', ('gadm_world', 'gadm0', 'gadm1'), index=0,
                 help="Geographical units of observation. gadm_world stands for the whole planet; \
                 gadm0 stands for countries; gadm1 stands for the first administrative level (states, regions, etc.)", 
                 key='geo_resolution')

# Weighting scheme
with col4:
    st.selectbox('Weighting variable', ('population density', 'night lights', 'cropland use', 'concurrent population', 'unweighted'), index=0,
                 help='Weighting variable specification', key='weight')

# Weighting year
if st.session_state.weight != "unweighted" and st.session_state.weight != "concurrent population":
    with col5:
        if st.session_state.geo_resolution != 'gadm_world' and st.session_state.geo_resolution != 'gadm2' and st.session_state.variable != 'min. temperature' and st.session_state.variable != 'max. temperature' and st.session_state.variable != 'max. wind gust':
            st.selectbox('Weighting year', ('2000', '2005', '2010', '2015'), index=0,
                        help='Base year for the weighting variable', key='weight_year')
        else:
            st.caption("Weighting year")
            st.markdown("2015")
            st.session_state.weight_year = '2015'

# Threshold settings
if st.session_state.source == 'ERA5' and (st.session_state.weight_year == '2015' or st.session_state.weight == 'concurrent population'):
    # Activate threshold customization
    with subcol1:
        st.selectbox('Threshold', ("False", "True"),
                     help='Activate threshold customization', key='threshold_dummy')
    # Threshold customization
    if st.session_state.threshold_dummy == "True":
        with subcol2:
            st.selectbox('Threshold type', ("percentile", "absolute", "cumulative"), index=0,
                         help='Type of threshold specification', key='threshold_kind')
        with subcol3:
            st.number_input('Threshold', value = 90, help='Threshold value', key='threshold')
else:
    st.caption("Threshold")
    st.markdown("False")

# Time frequency
if st.session_state.variable == 'SPEI':
    st.session_state.time_frequency = 'monthly'
    st.caption('Time frequency')
    st.markdown("monthly")
elif st.session_state.threshold_dummy == 'True':
    st.selectbox('Time frequency', ("yearly", "monthly"), index = 0,
                 help = 'Time frequency of the data', key='time_frequency')
elif st.session_state.source == 'ERA5' and (st.session_state.weight_year == '2015' or st.session_state.weight == 'concurrent population'):
    st.selectbox('Time frequency', ("yearly", "monthly", "daily"), index = 0,
                 help = 'Time frequency of the data', key='time_frequency')
else:
    st.selectbox('Time frequency', ("yearly", "monthly"), index = 0,
                 help = 'Time frequency of the data', key='time_frequency')

# Time period, threshold and observations
if st.session_state.source == 'CRU TS':
    min_year = 1901
    max_year = 2022
    source = 'cru'
elif st.session_state.source == 'ERA5':
    min_year = 1940
    max_year = 2024
    source = 'era'
elif st.session_state.source == 'CSIC':
    min_year = 1901
    max_year = 2020
    source = 'spei'
else: # (UDelaware)
    min_year = 1900
    max_year = 2017
    source = 'dela'

col1, col2 = st.columns(2)
# Starting year
with col1:
    st.slider('Starting year', min_year, max_year, key='starting_year')
# Ending year
with col2:
    if max_year == st.session_state.starting_year:
        st.session_state.ending_year = max_year
        st.caption("Ending year")
        st.markdown(max_year)
    else:
        st.slider('Ending year', st.session_state.starting_year, max_year, key='ending_year')

# ------------------- #
# Matching file names #
# ------------------- #

# Rename variables as to match datasets names
if st.session_state.variable == 'avg. temperature':
    variable = 'tmp'
elif st.session_state.variable == 'min. temperature':
    variable = 'tmpmin'
elif st.session_state.variable == 'max. temperature':
    variable = 'tmpmax'
elif st.session_state.variable == 'precipitation':
    variable = 'pre'
elif st.session_state.variable == 'max. wind gust':
    variable = 'gust'
else:
    variable = 'spei'
# Introduce string for weights
if st.session_state.weight == 'unweighted':
    weight = 'un'
    st.session_state.weight_year = '2015' # Force weight year to avoid session state error
elif st.session_state.weight == 'night lights':
    weight = 'lights'
elif st.session_state.weight == 'cropland use':
    weight = 'cropland'
elif st.session_state.weight == 'concurrent population':
    weight = 'concurrent'
    st.session_state.weight_year = '2015' # Force weight year to avoid session state error
else:
    weight = 'pop'


# ------------------- #
# Filter before query #
# ------------------- #

# Extract selected years
if st.session_state.geo_resolution == 'gadm0':
    obs_id = 'GID_0'
elif st.session_state.geo_resolution == 'gadm1':
    obs_id = 'GID_1'
else:
    obs_id = 'GID_2'

if st.session_state.time_frequency == 'daily' or st.session_state.threshold_dummy == 'True':
    time_range = tuple(['X' + str(x).replace('-', '') for x in pd.date_range(start=str(st.session_state.starting_year) + "-01-01",end= str(st.session_state.ending_year) + '-12-31').format("YYYY.MM.DD") if x != ''])
    if st.session_state.geo_resolution in ['gadm_world', 'gadm2'] and variable == 'pre' and st.session_state.ending_year == 2024:
        time_range = time_range[:-1] # Remove last day of 2024 as missing from data
else:
    time_range = tuple(['X' + str(x) + str(y).rjust(2, '0') for x in range(st.session_state.starting_year, st.session_state.ending_year + 1) for y in range(1,13)])

# Observation filters
world0 = load_country_list()
observation_list = world0.COUNTRY.unique().tolist()
observation_list.sort()
if st.session_state.geo_resolution == 'gadm_world':
    options = ['ALL']
elif st.session_state.geo_resolution == 'gadm0':
    options = st.multiselect('Countries', ['ALL'] + observation_list, default='United States', help = 'Choose the geographical units to show in the plot')
else:
    options = st.multiselect('Countries', observation_list, default='United States', help = 'Choose the geographical units to show in the plot')

# Build row range
if 'ALL' in options:
    country_range = '*'
    if st.session_state.geo_resolution != 'gadm_world':
        cloro_indicator = tuple(world0['GID_0'].tolist())
else:
    country_range = tuple(world0.loc[world0.COUNTRY.isin(options), 'GID_0'].tolist())
    cloro_indicator = country_range

# --------- #
# Load data #
# --------- #

# Read data from GitHub
data = load_data(st.session_state.geo_resolution, variable, source, weight,
                 st.session_state.weight_year, time_range, country_range,
                 st.session_state.time_frequency, st.session_state.threshold_dummy)

if 'ALL' in options:
    data.drop('Date', axis=1, inplace=True)

if st.session_state.geo_resolution == 'gadm_world' and 'Date' in data.columns:
    data = data.drop(columns=['Date'])

if st.session_state.geo_resolution == 'gadm_world' and variable == 'pre':
    data /= 1000 # scale back to mm

# Summarize if time frequency is yearly
if st.session_state.time_frequency == 'yearly' and st.session_state.threshold_dummy == 'False':
    if variable == 'pre':
        data = data.groupby(np.arange(data.shape[0])//12).agg(lambda x: np.sum(x) if sum(x.isna())==0 else np.nan)
    elif variable == 'tmp':
        data = data.groupby(np.arange(data.shape[0])//12).agg(lambda x: np.mean(x))
    elif variable == 'tmpmin':
        data = data.groupby(np.arange(data.shape[0])//12).agg(lambda x: np.min(x))
    elif variable == 'tmpmax' or variable == 'gust':
        data = data.groupby(np.arange(data.shape[0])//12).agg(lambda x: np.max(x))
    data.index = pd.date_range(start=str(st.session_state.starting_year) + "-01-01",end= str(st.session_state.ending_year) + "-12-31", freq="Y")

elif st.session_state.threshold_dummy == 'True':
    if st.session_state.threshold_kind == 'percentile':
        limit_values = data.quantile(q=st.session_state.threshold/100)
    else:
        limit_values = st.session_state.threshold
    days_over_threshold = data.gt(limit_values, axis=1)
    if st.session_state.threshold_kind == 'cumulative':
        days_over_threshold = data[days_over_threshold] - limit_values
    if st.session_state.time_frequency == 'yearly':
        n_aggregate_over_threshold = days_over_threshold.groupby(by=pd.Grouper(freq="Y")).sum()
    elif st.session_state.time_frequency == 'monthly':
        n_aggregate_over_threshold = days_over_threshold.groupby(by=pd.Grouper(freq="M")).sum()
    data = n_aggregate_over_threshold

# ------------- #
# Download data #
# ------------- #

col1, col2, col3 = st.columns(3)

with col1:    
	download_format = st.selectbox('Download format', ("Wide", "Long"), index=0)

with col2:
	download_extension = st.selectbox('Download extension', ("csv", "json", "parquet"), index=0)

if 'Date' in data.columns:
    data = data.drop('Date', axis=1)
if 'NA' in data.columns:
    data = data.drop('NA', axis=1)
if '?' in data.columns:
    data = data.drop('?', axis=1)

data.index = data.index.strftime('%Y-%m-%d')

if download_format == 'Long':
    data = data.reset_index()
    if st.session_state['time_frequency'] == 'daily':
        time_id = 'day'
    elif st.session_state['time_frequency'] == 'monthly':
        time_id = 'month'
    else:
        time_id = 'year'
    data = pd.melt(data, id_vars='index', var_name='geo_res', value_name=variable)
    data.columns = [time_id, st.session_state.geo_resolution, variable]

data_show = data

if download_extension == 'csv':
    data = data.to_csv().encode('utf-8')
elif download_extension == 'json':
    data = data.to_json(date_format='iso').encode('utf-8')
else:
    data = data.to_parquet()

with col3:
    if weight == 'un' or weight == 'concurrent':
        wgt_year = ''
    else:
        wgt_year = st.session_state.weight_year
    filename =  st.session_state.geo_resolution + '_' + source + '_' + variable + '_' + weight + '_' + wgt_year + '_' + st.session_state.time_frequency + '.'
    st.download_button(label = "Download data", data = data, file_name = './data/' + filename + download_extension)
    
    if source == 'spei':
        source2 = 'csic'
    else:
        source2 = source
    meta_text = f"""Metadata\n
Geographic resolution: {st.session_state.geo_resolution} (https://gadm.org/)
Climate variable source: {source2} ({info[source2]})
Climate variable: {variable} ({info[variable]})
Weighting variable: {weight} ({info[weight]})
Weighting base year: {wgt_year}\n\n
How to cite our work:
Gortan, M., Testa, L., Fagiolo, G., Lamperti, F., A unified dataset for pre-processed climate indicators weighted by gridded economic activity, Scientific Data (2024)
https://www.nature.com/articles/s41597-024-03304-1
"""
    st.download_button(label="Download metadata", data = meta_text, file_name= 'metadata_' + filename + 'txt')

# -------------- #
# Visualize data #
# -------------- #

st.markdown('### Preview of the data')
st.markdown('We are showing the first 100 rows and 50 columns of the data. If you want to see the full dataset, please download it.')
st.dataframe(data_show.iloc[0:100, 0:50].head(100))

with st.expander("Interested in bulk downloads?", expanded=False):
    """
    If you are interested in downloading the full dataset, you can visit the following Box folders.
    """
    # table for bulk download links
    df = pd.DataFrame(
    {
        "Resolution": ["gadm_world", "gadm0", "gadm1", "gadm2"],
        "Link": [
            "https://cmu.box.com/s/q566o1o4xjlin83jvgbupwv2tgbk73t4",
            "https://cmu.box.com/s/qaej7c5swi73fr24fkodtieq9qymh7bz",
            "https://cmu.box.com/s/qjflsyu33qcl1r9xw5ki4jtcmv2z9gx6",
            "https://cmu.box.com/s/1jlbcza7vrsm8r1x1sw80qo0k3q2io6b",
        ],
    }
    )
    st.table(df)
    """
    No authentication is required to access the folders. If you have any questions, please contact us!
    """
   

with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)
    
    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """

