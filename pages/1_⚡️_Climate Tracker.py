# -------------------- #
# Climate Tracker tab   #
# -------------------- #

import streamlit as st
import pandas as pd
import duckdb as db
import plotly.graph_objects as go

# --------------------- #
# Initial Session State #
# --------------------- #

if "ct_initialized" not in st.session_state:
    st.session_state['ct_initialized'] = True
    st.session_state['ct_variable'] = 'avg. temperature'
    st.session_state['ct_weight'] = 'population density'
    st.session_state['ct_geo_resolution'] = 'gadm0'
    st.session_state['ct_country'] = 'United States'
    st.session_state['ct_window'] = 'last 30 available days'

# ------------ #
# Data imports #
# ------------ #

VARIABLE_MAP = {
    'avg. temperature': 'tmp',
    'min. temperature': 'tmpmin',
    'max. temperature': 'tmpmax',
}

# weight -> (file token, weight year token)
WEIGHT_MAP = {
    'population density': ('pop', '2015'),
    'night lights': ('lights', '2015'),
    'cropland use': ('cropland', '2015'),
    'concurrent population': ('concurrent', ''),
    'unweighted': ('un', ''),
}

@st.cache_data(ttl=180, show_spinner="Fetching country names...")
def load_country_list():
    return pd.read_csv('./poly/country_list.csv')

@st.cache_data(ttl=180, show_spinner="Fetching region names...")
def load_gadm1_list():
    regions = pd.read_csv('./poly/gadm1_adm.csv')
    regions['GID_1'] = regions['GID_1'].apply(lambda x: str(x).replace(".", "_"))
    return regions

def _connect_duckdb():
    db.sql('INSTALL httpfs')
    db.sql('LOAD httpfs')
    db.sql("SET s3_endpoint='storage.googleapis.com'")
    db.sql("SET s3_access_key_id=" + st.secrets['duckdb']['id'])
    db.sql("SET s3_secret_access_key=" + st.secrets['duckdb']['password'])

@st.cache_data(ttl=180, show_spinner="Fetching tracker data...")
def load_tracker_series(geo_resolution, variable, weight, weight_year, col):
    _connect_duckdb()
    file = f"s3://climatedata_bucket/tracker/tracker_{geo_resolution}_era_{variable}_{weight}_{weight_year}_daily.parquet"
    query = f'SELECT Date, "{col}" AS value FROM \'{file}\' ORDER BY Date'
    data = db.query(query).fetch_arrow_table().to_pandas()
    data['Date'] = pd.to_datetime(data['Date'].str.lstrip('X'), format='%Y%m%d')
    return data

@st.cache_data(ttl=180, show_spinner="Fetching historical reference...")
def load_historical_series(geo_resolution, variable, weight, weight_year, col):
    _connect_duckdb()
    file = f"s3://climatedata_bucket/{geo_resolution}_era_{variable}_{weight}_{weight_year}_daily.parquet"
    query = f'SELECT Date, "{col}" AS value FROM \'{file}\' ORDER BY Date'
    data = db.query(query).fetch_arrow_table().to_pandas()
    data['Date'] = pd.to_datetime(data['Date'].str.lstrip('X'), format='%Y%m%d')
    return data

# ------------- #
# Page settings #
# ------------- #

st.set_page_config(page_title="Climate Tracker", page_icon="⚡")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("# The Weighted Climate Dataset")
st.markdown("## Climate Tracker")
st.caption("Near-real-time ERA5 daily temperature, updated daily with a 6-day processing lag. "
           "Historical reference bands and median are computed from the 1940-2025 ERA5 daily record.")
st.warning("This is an experimental feature. Near-real-time values are provisional: ERA5 may revise its underlying "
           "data for recent days, so figures shown here can change (this is not something we control).")

# ---------- #
# Parameters #
# ---------- #

col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox('Climate variable', tuple(VARIABLE_MAP.keys()), index=0,
                 help='Measured climate variable of interest', key='ct_variable')

with col2:
    st.selectbox('Weighting variable', tuple(WEIGHT_MAP.keys()), index=0,
                 help='Weighting variable specification (base year 2015)', key='ct_weight')

with col3:
    st.selectbox('Geographical resolution', ('gadm0', 'gadm1'), index=0,
                 help="gadm0 stands for countries; gadm1 stands for the first administrative level (states, regions, etc.)",
                 key='ct_geo_resolution')

country_list = load_country_list()
country_names = sorted(country_list['COUNTRY'].unique().tolist())

st.selectbox('Country', country_names, key='ct_country', help='Country to visualize')

country_gid0 = country_list.loc[country_list.COUNTRY == st.session_state.ct_country, 'GID_0'].iloc[0]

if st.session_state.ct_geo_resolution == 'gadm1':
    gadm1_list = load_gadm1_list()
    region_names = sorted(gadm1_list.loc[gadm1_list.GID_0 == country_gid0, 'NAME_1'].unique().tolist())
    if not region_names:
        st.warning('No GADM1 administrative units available for the selected country.')
        st.stop()
    region_name = st.selectbox('GADM1 administrative unit', region_names, key=f'ct_region_{country_gid0}',
                                help='First administrative level unit to visualize')
    col = gadm1_list.loc[(gadm1_list.GID_0 == country_gid0) & (gadm1_list.NAME_1 == region_name), 'GID_1'].iloc[0]
    location_label = f"{region_name}, {st.session_state.ct_country}"
else:
    col = country_gid0
    location_label = st.session_state.ct_country

st.selectbox('Time window', ('previous month', 'current month', 'last 30 available days'), index=2,
             help='Period of the tracker series to display', key='ct_window')

# --------------------- #
# Matching file names   #
# --------------------- #

variable = VARIABLE_MAP[st.session_state.ct_variable]
weight, weight_year = WEIGHT_MAP[st.session_state.ct_weight]

# --------- #
# Load data #
# --------- #

tracker = load_tracker_series(st.session_state.ct_geo_resolution, variable, weight, weight_year, col)
historical = load_historical_series(st.session_state.ct_geo_resolution, variable, weight, weight_year, col)

# Determine the full date axis for the selected time window.
# For "current"/"previous month" the axis spans the whole calendar month, so the
# historical reference bands are shown even for days the tracker hasn't reached yet;
# the tracked value line then simply stops where data runs out.
today = pd.Timestamp.today().normalize()
if st.session_state.ct_window == 'current month':
    month_start = today.replace(day=1)
    month_end = month_start + pd.offsets.MonthEnd(0)
    full_dates = pd.date_range(month_start, month_end, freq='D')
elif st.session_state.ct_window == 'previous month':
    month_end = today.replace(day=1) - pd.Timedelta(days=1)
    month_start = month_end.replace(day=1)
    full_dates = pd.date_range(month_start, month_end, freq='D')
else:
    full_dates = tracker.tail(30)['Date']

available = tracker[tracker.Date.isin(full_dates)]
if available.empty:
    st.warning('No tracker data available yet for the selected time window.')
    st.stop()

# ------------------------- #
# Historical reference bands #
# ------------------------- #

historical['month_day'] = historical.Date.dt.strftime('%m-%d')
hist_quantiles = historical.groupby('month_day')['value'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).unstack()
hist_quantiles.columns = ['q05', 'q25', 'median', 'q75', 'q95']

plot_df = pd.DataFrame({'Date': full_dates})
plot_df = plot_df.merge(tracker[['Date', 'value']], on='Date', how='left')
plot_df['month_day'] = plot_df.Date.dt.strftime('%m-%d')
plot_df = plot_df.merge(hist_quantiles, left_on='month_day', right_index=True, how='left').sort_values('Date')

# ---------------- #
# Plot time series #
# ---------------- #

st.markdown(f"### {location_label} — {st.session_state.ct_variable} ({st.session_state.ct_weight})")

fig = go.Figure()

# 5th-95th historical percentile band
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['q95'], mode='lines',
                          line=dict(width=0), showlegend=False, hoverinfo='skip'))
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['q05'], mode='lines',
                          line=dict(width=0), fill='tonexty', fillcolor='rgba(157,197,244,0.35)',
                          name='5th-95th pct (historical, 1940-2025)', hoverinfo='skip'))

# 25th-75th historical percentile band
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['q75'], mode='lines',
                          line=dict(width=0), showlegend=False, hoverinfo='skip'))
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['q25'], mode='lines',
                          line=dict(width=0), fill='tonexty', fillcolor='rgba(109,167,236,0.55)',
                          name='25th-75th pct (historical, 1940-2025)', hoverinfo='skip'))

# Historical median (dashed)
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['median'], mode='lines',
                          line=dict(color='#52514e', width=2, dash='dash'),
                          name='Historical median (1940-2025)'))

# Tracker value
fig.add_trace(go.Scatter(x=plot_df['Date'], y=plot_df['value'], mode='lines+markers',
                          line=dict(color='#eb6834', width=2.5), marker=dict(size=6),
                          name='Tracked value'))

fig.update_layout(
    xaxis_title='Date',
    yaxis_title=f"{st.session_state.ct_variable} (°C)",
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
    margin=dict(l=10, r=10, t=40, b=10),
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------- #
# Average vs. historical years    #
# ------------------------------- #

current_year = int(available['Date'].dt.year.iloc[-1])
current_avg = available['value'].mean()
available_month_days = set(available['Date'].dt.strftime('%m-%d'))

hist_same_days = historical[historical['month_day'].isin(available_month_days)].copy()
hist_same_days['year'] = hist_same_days['Date'].dt.year
yearly_avg = hist_same_days.groupby('year')['value'].mean().reset_index()

percentile = (yearly_avg['value'] < current_avg).mean() * 100

all_years = pd.concat(
    [yearly_avg, pd.DataFrame({'year': [current_year], 'value': [current_avg]})],
    ignore_index=True
).sort_values('value', ascending=False).reset_index(drop=True)
all_years['rank'] = all_years.index + 1
current_rank = int(all_years.loc[all_years.year == current_year, 'rank'].iloc[0])
total_years = len(all_years)

st.markdown("### Average vs. historical years")
st.caption(
    f"Average computed over {len(available)} available day(s) "
    f"({available['Date'].min().date()} to {available['Date'].max().date()}), "
    f"compared against the same calendar day(s) in each year of the 1940-2025 historical record."
)

st.metric(
    label=f"{current_year} average ({st.session_state.ct_variable})",
    value=f"{current_avg:.2f} °C",
    delta=f"{current_avg - yearly_avg['value'].mean():+.2f} °C vs. historical mean",
)
st.caption(f"{current_year} is warmer than {percentile:.0f}% of the 1940-2025 historical years for this same period, "
           f"ranking #{current_rank} out of {total_years} years (1 = warmest).")

col_hist, col_top = st.columns([1.5, 1])

with col_hist:
    hist_fig = go.Figure()
    hist_fig.add_trace(go.Histogram(x=yearly_avg['value'], nbinsx=20,
                                     marker_color='rgba(109,167,236,0.7)',
                                     name='Historical years (1940-2025)'))
    hist_fig.add_vline(x=current_avg, line_width=2.5, line_dash='dash', line_color='#eb6834',
                        annotation_text=f"{current_year}: {current_avg:.2f} °C ({percentile:.0f}th pct.)",
                        annotation_position='top')
    hist_fig.update_layout(
        xaxis_title=f"Average {st.session_state.ct_variable} (°C)",
        yaxis_title='Number of years',
        bargap=0.05,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
    )
    st.plotly_chart(hist_fig, use_container_width=True)

with col_top:
    st.markdown("**Top 5 warmest years**")
    top5 = all_years.head(5).copy()
    top5['value'] = top5['value'].round(2)
    top5 = top5.rename(columns={'rank': 'Rank', 'year': 'Year', 'value': 'Avg (°C)'})
    top5['Year'] = top5['Year'].apply(lambda y: f"{y} ←" if y == current_year else str(y))
    st.dataframe(top5[['Rank', 'Year', 'Avg (°C)']], hide_index=True, use_container_width=True)
    if current_rank > 5:
        st.caption(f"{current_year} is not in the top 5 (rank #{current_rank}).")

# Side bar
with st.sidebar:
    """
    [Institute of Economics](https://www.santannapisa.it/en/istituto/economia) and [L'EMbeDS Department](https://www.santannapisa.it/en/department-excellence/embeds)

    Sant'Anna School of Advanced Studies (Pisa, Italy)
    """
