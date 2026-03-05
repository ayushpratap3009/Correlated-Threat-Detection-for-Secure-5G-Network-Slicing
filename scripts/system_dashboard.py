import streamlit as st
import pandas as pd
import json
import plotly.express as px
import time

st.set_page_config(
    page_title="5G Threat Monitoring Dashboard",
    layout="wide"
)


# -----------------------
# Load Alerts
# -----------------------
def load_alerts():

    try:
        with open("alerts_log.json") as f:
            data = json.load(f)
            return pd.DataFrame(data)

    except:
        return pd.DataFrame(
            columns=["time", "slice", "attack", "confidence", "severity"]
        )


# -----------------------
# Dashboard Title
# -----------------------

st.title("5G Network Threat Monitoring Dashboard")

df = load_alerts()

if len(df) == 0:

    st.warning("No alerts detected yet.")

else:

    # -----------------------
    # Metrics
    # -----------------------

    total_flows = len(df)

    attacks_detected = len(df)

    coordinated_attacks = len(df[df["severity"] == "CRITICAL"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Flows Processed", total_flows)

    col2.metric("Attacks Detected", attacks_detected)

    col3.metric("Coordinated Attacks", coordinated_attacks)

    st.divider()

    # -----------------------
    # Charts
    # -----------------------

    col4, col5 = st.columns(2)

    # Slice distribution
    slice_counts = df["slice"].value_counts()

    fig1 = px.pie(
        values=slice_counts.values,
        names=slice_counts.index,
        title="Slice Distribution"
    )

    col4.plotly_chart(fig1, use_container_width=True)

    # Attack distribution
    attack_counts = df["attack"].value_counts()

    fig2 = px.bar(
        x=attack_counts.index,
        y=attack_counts.values,
        labels={"x": "Attack", "y": "Count"},
        title="Attack Types"
    )

    col5.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # -----------------------
    # Severity Chart
    # -----------------------

    severity_counts = df["severity"].value_counts()

    fig3 = px.bar(
        x=severity_counts.index,
        y=severity_counts.values,
        title="Threat Severity Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # -----------------------
    # Recent Alerts Table
    # -----------------------

    st.subheader("Recent Alerts")

    st.dataframe(df.tail(10), use_container_width=True)

# -----------------------
# Auto refresh
# -----------------------

time.sleep(5)

st.rerun()