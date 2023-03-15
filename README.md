Near Social Segmentation Tool
==============================

This project intends to build a tool/dashboard which can be used to analyse the segmentation of [Near Social](http://near.social) users, an on-chain social network. 

It will identify the potential user base for the social network as addresses signing in for the first time to the `near.social` contract and will explore different segmentation profiles.

In its first iteration, it will be submitted to the [MetricsDAO](https://metricsdao.xyz/) bounty program *NEAR 18. Social Segmentation*. Further development will take place as needed.



Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── queries        <- SQL queries of the on-chain data.
    │   └── csv            <- Results of SQL queries that will be loaded to the app.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │                         Generated with `pip freeze --format=freeze > requirements.txt` to avoid odd path references
    │
    ├── near_social_segment_app.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


# TODO
1. deploy first iteration on Streamlit
2. add DeFi, NFT, Social Activity Tabs
3. publish the dahsboard in Twitter and LinkedIn 
