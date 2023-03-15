# Import
import pandas as pd
import numpy as np
import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import plotly.io as pio
from datetime import datetime, timedelta

# Streamlit

# Set st title and header
st.set_page_config(page_title='Near Social Segmentation Tool',
                   page_icon='random',
                   layout='wide')
st.title('Near Social Segmentation Tool')

# Define functions with caching
@st.cache_data # decorator to add caching
def load_data(csv):
    df = pd.read_csv(csv)
    df['first_social_sign'] = df['first_social_sign'].astype('datetime64[ns]')
    return df.copy(deep=True)

@st.cache_data
def select_data(df, column, begin, end):
    return df[(df[column]>= np.datetime64(begin)) & (df[column]<= np.datetime64(end))]

@st.cache_data
def agg_by_column(df, column):
    return df.groupby(column).count().reset_index()

## Dataframe for global variables - all-time signers
df1 = load_data('data/csv/auths_raw_df.csv')

df1_agg = agg_by_column(df1[['user', 'first_social_sign']],'first_social_sign').rename({'first_social_sign': 'Date', 'user':'Daily Users'}, axis=1)

since = np.min(df1_agg['Date'])
last_updated = np.max(df1_agg['Date'])
total_users = np.max(df1_agg['Daily Users'].cumsum())

# Set sidebar to select timeframe
with st.sidebar:
    st.write("Analysed Timeframe")

    timeframe = st.radio('Select timeframe:',
                        ('Last 30 days', 'Last 60 days', 'Last 90 days', 'Custom timeframe', 'All-time'),
                        index=4
                        )

    if timeframe == 'Last 30 days':
        begin_date = datetime.today() - timedelta(days=30) - timedelta(days=1)
        end_date = datetime.today() - timedelta(days=1)
        st.write('Selected timeframe is last 30 days')

    if timeframe == 'Last 60 days':
        begin_date = datetime.today() - timedelta(days=60) - timedelta(days=1)
        end_date = datetime.today() - timedelta(days=1)
        st.write('Selected timeframe is last 60 days')

    if timeframe == 'Last 90 days':
        begin_date = datetime.today() - timedelta(days=90) - timedelta(days=1)
        end_date = datetime.today() - timedelta(days=1)
        st.write('Selected timeframe is last 90 days')

    if timeframe == 'Custom timeframe':
        col1, col2, col3 = st.columns(3)

        begin_date = st.date_input('Select begin date:',
                                    value=datetime.today()- timedelta(days=91),
                                    #min_value=datetime.date(2022,2,16),
                                    max_value=datetime.today()- timedelta(days=1)
                                )
        end_date = st.date_input('Select end date:',
                                    value=datetime.today()- timedelta(days=1),
                                    min_value=begin_date,
                                    max_value=datetime.today()- timedelta(days=1)
                                )

        if begin_date != end_date:
            st.write(f'Selected timeframe is between {begin_date} and {end_date}')
        else:
            st.write(f'Selected timeframe is on {begin_date}')

    if timeframe == 'All-time':
        begin_date = since
        end_date = last_updated
        st.write(f'Selected timeframe is between {str(begin_date)[:11]} and {str(end_date)[:11]}')

# Load Filtered Dataframes

## Dataframe for wallet age histogram and metrics
df2 = select_data(df1, 'first_social_sign' , begin_date, end_date)

## Dataframe for wallet age category pie chart
df3 = agg_by_column(df2[['user', 'age_category']], 'age_category').rename({'user': 'wallets'}, axis=1)

## Dataframe for human-readable addresses pie 
df4 = agg_by_column(df2[['user', 'human_readable']], 'human_readable').rename({'user': 'wallets'}, axis=1)

## Dataframe for same day signers by human-readable
df5 = agg_by_column(df2[df2['age_days']==0][['user', 'human_readable']], 'human_readable').rename({'user': 'wallets'}, axis=1)

## Dataframes for DeFi
df6_load = load_data('data/csv/defi_raw_df.csv')
df6 = select_data(df6_load,'first_social_sign', begin_date, end_date)

df7 = agg_by_column(df6[['user', 'swaps_category']], 'swaps_category').rename({'user': 'wallets'}, axis=1)
df8 = agg_by_column(df6[['user', 'swapped_before_social']], 'swapped_before_social').rename({'user': 'wallets'}, axis=1)

df11 = agg_by_column(df6[['user', 'stake_category']], 'stake_category').rename({'user': 'wallets'}, axis=1)
df9 = agg_by_column(df6[['user', 'staked_before_social']], 'staked_before_social').rename({'user': 'wallets'}, axis=1)

df10 = agg_by_column(df6[['user', 'defi_category']], 'defi_category').rename({'user': 'wallets'}, axis=1)

# Set st tabs
tabs = st.tabs(["Introduction", "Wallet age and address type", "DeFi", "Social.NEAR activity", "Keys Insights and Methodology"])

with tabs[0]: # Introduction
    st.write('''Social.NEAR is an on-chain social network built on the NEAR blockchain that has recently seen a surge 
    in the number of users signing in for the first time. 
    This dashboard presents a tool to analyze the new user segmentation for a given timeframe. 
    To operate it, select a timeframe on the left sidebar and navigate through the tabs to analyze different profile categories.
    ''')

    cols = st.columns([1,2,2,2,1])
    cols[1].metric("Total users", total_users, help='First-time signers of social.near contract')
    cols[2].metric("Available data since", str(since)[:11], help='On-chain data first record')
    cols[3].metric("Data last updated on", str(last_updated)[:11], help='On-chain data last record')

    # Plot all-time signers
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    
    fig.add_trace(
                go.Scatter(x=df1_agg['Date'], y=df1_agg['Daily Users'].cumsum(), name='Cumulative'), 
                secondary_y=False
                )

    fig.add_trace(
                go.Bar(x=df1_agg['Date'], y=df1_agg['Daily Users'], name='Daily'),    
                secondary_y=True
                )

    fig.update_xaxes(title_text="<b>Date</b>")

    fig.update_yaxes(title_text="<b>Cumulative Users</b> ", secondary_y=False)

    fig.update_yaxes(title_text="<b>Daily Users</b> ", secondary_y=True)

    fig.update_layout(
                    title='<b>All-time New Users Signing to the Social.NEAR Contract</b>',
                    autosize=False,
                    width=900,
                    height=600,
                    margin=dict(
                        l=100,
                        r=100,
                        b=100,
                        t=100,
                        pad=4
                    ),
                    paper_bgcolor="white",
                    hovermode='x unified'
                    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('''For more info on Social.Near visit http://near.social or 
    this wonderful [article on NEAR wiki](https://thewiki.near.page/PastPresentAndFutureOfNearSocial)''')

with tabs[1]: # "Wallet age and address type
    # Wallet age at sign in plot
    st.write('''This tab analyses the wallet age when signing to social.near contract for the first time and 
    whether the addresses are human-readable or not (user chosen or 64 alphanumeric characters cryptographically created)''')

    with st.container():
        cols = st.columns([1,2,2,2,2,1])
        cols[1].metric("Total users in timeframe", df2['age_days'].size, help='First-time signers of social.near contract in selected timeframe')
        cols[2].metric("Wallet average age", round(df2['age_days'].mean(),2), help='Average wallet age at first sign-in')
        cols[3].metric("Wallet mode age", round(df2['age_days'].mode(),2), help='Mode wallet age at first sign-in')
        cols[4].metric("Same day signers", df2['age_days'][df2['age_days']==0].size, help='Wallets signing to Near Social the same day they were created')

    with st.container():
        cols = st.columns(3)

        with cols[0]:
            fig = px.pie(df3,
                        values='wallets',
                        names='age_category',
                        title='Wallets by age category')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        with cols[1]:
            fig = px.pie(df4,
                        values='wallets',
                        names='human_readable',
                        title='Human readable addresses')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        with cols[2]:
            fig = px.pie(df5,
                        values='wallets',
                        names='human_readable',
                        title='Human readable addresses of same day signers')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        fig = px.histogram(df2, 
                        x='age_days',
                        color='human_readable',
                        #marginal='box',
                        nbins=20)

        fig.update_layout(bargap=0.1,
                        title='Distribution of users by wallet age in days when signing in Social.NEAR for the first time',
                        font=dict(color='black'
                                ),
                        hoverlabel=dict(bgcolor='white',
                                        font_size=12
                                        )
                        )

        fig.update_xaxes(title='Wallet Age [days]',
                        title_font=dict(size=14,
                                        color='black'
                                        )
                        )

        fig.update_yaxes(title='Number of Wallets',
                        title_font=dict(size=14, 
                                        color='black'
                                        )
                        )

        #fig.update_traces(hovertemplate =
        #                '<i>Age</i>: ' + '%{x} days<br>' +
        #                '<i>Count</i>: ' + '%{y} wallets' + '<extra></extra>',
        #
        #                selector=dict(type="histogram"))

        st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # DeFi
    st.write('''This Tab takes a look at the users DeFi activity. It will compare wallets based on swap and stake activity 
    and whether the users had swapped or staked before signing to Near Social.''')

    with st.container():
        cols = st.columns([1,2,2,2,2,1])
        cols[1].metric("Total users in timeframe", df2['age_days'].size, 
                        help='First-time signers of social.near contract in selected timeframe')
        cols[2].metric("Average number of swaps", round(df6['number_of_swaps'].mean(),2), 
                        help='Average number of swaps of all signers')
        cols[3].metric("Average number of stake actions", round(df6['number_stake_actions'].mean(),2), 
                        help='Average number of stake actions of all signers')
        cols[4].metric("Average stake of current stakers", str(round(df6[df6['current_stake']!=0]['current_stake'].mean(),2)) + ' NEAR', 
                        help='Average stake amount of users currently staking NEAR')

    with st.container():
        cols = st.columns(3)

        with cols[0]:
            fig = px.pie(df7,
                        values='wallets',
                        names='swaps_category',
                        title='Wallets by number of swaps')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        with cols[1]:
            fig = px.pie(df11,
                        values='wallets',
                        names='stake_category',
                        title='Wallets by stake category')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)
            
        with cols[2]:
            fig = px.pie(df10,
                        values='wallets',
                        names='defi_category',
                        title='Wallets by DeFi usage')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        cols = st.columns([1,2,2,1])

        with cols[1]:
            fig = px.pie(df8,
                        values='wallets',
                        names='swapped_before_social',
                        title='Did users swap before signing to Near Social?')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)
            
        with cols[2]:
            fig = px.pie(df9,
                        values='wallets',
                        names='staked_before_social',
                        title='Did users stake before signing to Near Social?')

            fig.update_traces(textinfo='percent+label')

            fig.update(layout_showlegend=False)

            st.plotly_chart(fig, use_container_width=True)


with tabs[3]: # Near Social activity
    st.write('Coming Soon - users profile according to their activity on Near Social')

with tabs[4]: # Keys Insights and Methodology
    st.markdown('''
        ## Key Insights

        Based on a first look at the data in the different predefined timeframes, the following key points can be identified:

        - Social Near seems to onboard either very old or very new wallets.
        
        - Same day signers, i.e. users signing in to Social Near the same day they make their first on-chain transaction, could mean that a new user is
        onboarded on NEAR through the social platform or that an existing user creates a new account for social interactions.

        - Users who to chose their account ID name (human readable) vary between 75-80\% of total users. For same day signers though, 
        the field is almost leveled with implicit, 64-character addresses (55\% to 45\% split).

        - The majority of users didn't use swapped tokens (67\%-72\%) or staked NEAR tokens (80\%-85\%). The more recent that the chosen timeframe is,
        the less DeFi activity.

        - Amongst the ones that did use any of this DeFi products, swappers are more abundant than stakers.

        These are some observations made on the day on the publication of this tool and could be different in the future.

        ## Methodology

        This dashboard was done using [Flipside Crypto](https://flipsidecrypto.xyz/) [ShroomDK](https://sdk.flipsidecrypto.xyz/shroomdk) API. 
        The on-chain data was queried from the `fact_actions_events_addkey`, `fact_transactions`, `ez_dex_swaps` and `dim_staking_actions` tables
        from the `near.core` schema.

        All relevant project files can be accessed through its [GitHub public repo](https://github.com/Rojoser/Near-Social_segmentation_tool). 
        The SQL queries and csv files are available to anyone looking where the data came from:

        - Raw SQL queries are saved as .txt files under the `data/queries` folder.

        - Query results are saved as .csv files under the `data/csv` folder.

        - A Jupyter Notebook (.ipynb file) with the API calls and SQL queries can be found under the `/notebook` folder in the project's repo.

        You can contact me on [LinkedIn](https://www.linkedin.com/in/rojoserrano/) or in Twitter [@rojoser_data](https://twitter.com/rojoser_data) 
        for any question, suggestion or discussion.   
    ''')
