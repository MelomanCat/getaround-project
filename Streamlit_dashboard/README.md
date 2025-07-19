---
title: Getaround Delay Analysis
emoji: "🚗"
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.22.0"  
app_file: app.py
pinned: false
---


🧠 Getaround Dashboard – Rental Threshold Analysis

This dashboard analyzes the impact of introducing a minimum threshold time between rentals on the Getaround platform. It explores trade-offs between:

Efficiency: Percentage of avoided incidents per percentage of revenue loss. A higher value means better impact-cost tradeoff.

Revenue loss: Share of potentially lost revenue due to skipped rentals

Scope and thresholds: Simulations for different delay thresholds (30-180 min) and scope (all cars vs. Connect only)

🚀 Live Demo
👉 Open the Dashboard on Streamlit


📁 Files
app.py – main Streamlit app

requirements.txt – dependencies

style.css – custom styling


💡 Features

Dual analysis: all cars vs. Connect only

Visualizations for revenue loss and saved rentals

Interactive controls: change buffer thresholds

Recommendations section


📦 How to run locally

pip install -r requirements.txt
streamlit run app.py
