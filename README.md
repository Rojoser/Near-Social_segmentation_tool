Near Social Segmentation Tool
==============================

This project intends to build a tool/dashboard which can be used to analyse the segmentation of [Near Social](http://near.social) users, an on-chain social network. 

It will identify the potential user base for the social network as addresses signing in for the first time to the `near.social` contract and will explore different segmentation profiles.

In its first iteration, it will be submitted to the [MetricsDAO](https://metricsdao.xyz/) bounty program *NEAR 18. Social Segmentation*. Further development will take place as needed.



Project Organization
------------

    ├── LICENSE            <- Mozilla Public License Version 2.0
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── queries        <- SQL queries of the on-chain data.
    │   └── csv            <- Results of SQL queries that will be loaded to the app.
    │
    ├── notebooks          <- Jupyter notebooks used to query the on-chain data via API.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │                         Generated with `pip freeze --format=freeze > requirements.txt` 
    │   		       to avoid odd path references.
    │
    └── app.py             <- Python script to deploy the app in Streamlit


Future improvements
------------

- Analyse Near Social Activity using on-chain data
- Explore ways to analyse developer activity (GitHub or on-chain data)
