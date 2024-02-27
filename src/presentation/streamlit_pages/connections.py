import re
import streamlit as st
from src.domain.use_cases.get_all_connections.get_all_connections import (
    AllConnectionsGetter,
)
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from src.utils.mappers import job_position_mapper


def main():

    alt.Config(padding=50)

    st.set_page_config(
        page_title="Connections",
        page_icon="🧑‍💻",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    page_bg_img = """
    <style>
    .st-emotion-cache-13k62yr {
        background-size: cover;
        background-image: url("https://i.imgur.com/T5TympJ.png")
    }
    .st-emotion-cache-1xw8zd0 {
        background: rgba(0, 0, 0, 0.8);
    }
    [data-testid="stMetric"] {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(250, 250, 250, 0.2);
        border-radius: 0.5rem;
        padding: .5rem;
    }
    </style>
    """

    title_chart_config = {
        "font": {"family": "Source Sans Pro", "size": 20, "color": "white"},
        "pad": {"l": 0, "t": 0},
    }

    st.markdown(page_bg_img, unsafe_allow_html=True)

    connections_data = AllConnectionsGetter().get_all()
    connections_count = len(connections_data)

    weekly_connections_count_df = generate_weekly_count_connections_df(
        connections_data.copy()
    )

    new_connections_per_week = round(
        connections_count / len(weekly_connections_count_df.week_year.unique()), 1
    )

    proportion_recruiters_df = generate_recruiter_proportion_df(
        connections_data.copy(), job_position_mapper["Recruiter"]
    )

    positions_count = generate_positions_count_df(
        connections_data.copy(), job_position_mapper
    )

    group_by_companies_count = generate_companies_count(connections_data, 10)

    st.write("## Connections Analysis")

    row1 = st.columns([0.2, 0.2, 0.6])
    with row1[0]:
        st.metric("Number of Connections", connections_count)
    with row1[1]:
        st.metric("Average connections per week", new_connections_per_week)

    with st.container(border=True):
        fig = px.bar(
            weekly_connections_count_df,
            x="week_year",
            y="count",
            title="Number of new Connections by week-year",
            height=300,
        )

        fig.update_layout(
            margin=dict(t=30, b=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title=title_chart_config,
            yaxis_title=None,
            xaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    row3 = st.columns([0.4, 0.4, 0.3], gap="small")
    with row3[0]:
        fig = px.bar(
            positions_count.sort_index(),
            x="count",
            y="mapped_position",
            title="Number of Connections by job position",
            height=300,
            orientation="h",
        )

        fig.update_layout(
            margin=dict(t=30, b=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title=title_chart_config,
            yaxis_title=None,
            xaxis_title=None,
            yaxis={"categoryorder": "total ascending"},
        )
        st.container(border=True).plotly_chart(fig, use_container_width=True)

    with row3[1]:
        fig = px.bar(
            group_by_companies_count,
            x="count",
            y="company",
            title="Number of Connections by Company",
            height=300,
            orientation="h",
        )

        fig.update_layout(
            margin=dict(t=30, b=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title=title_chart_config,
            yaxis_title=None,
            xaxis_title=None,
            yaxis={"categoryorder": "total ascending"},
        )
        st.container(border=True).plotly_chart(fig, use_container_width=True)

    with row3[2]:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=proportion_recruiters_df["is_recruiter"],
                    values=proportion_recruiters_df["count"],
                    pull=[0.2, 0],
                    textfont_size=15,
                )
            ]
        )

        fig.update_layout(
            height=300,
            margin=dict(t=30, b=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title=title_chart_config | {"text": "Proportion of Recruiters (%)"},
            showlegend=False,
        )
        st.container(border=True).plotly_chart(fig, use_container_width=True)


def generate_weekly_count_connections_df(
    connections_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generates a dataframe that is a count of the connections grouped by week-year.
    Weeks without new connections will have 0 in the count column.

    args:
        connections_data (pd.DataFrame) : dataframe with the connections data

    returns:
        weekly_connections_count_df (pd.Dataframe): count of connections groupeb by week-year
            - week_year (str)
            - count (int)
    """
    first_date_con = connections_data.connected_on.min()
    last_date_con = connections_data.connected_on.max()

    connections_weekly_count_df = (
        connections_data.assign(
            week_year=connections_data["connected_on"].dt.strftime("%U-%Y"),
        )
        .groupby("week_year")
        .size()
        .reset_index(name="count")
    )

    generated_week_year = pd.DataFrame(
        {
            "week_year": (
                pd.date_range(start=first_date_con, end=last_date_con)
                .strftime("%U-%Y")
                .unique()
            )
        }
    )

    weekly_connections_count_df = generated_week_year.merge(
        connections_weekly_count_df, how="left", on="week_year"
    ).fillna(0)

    return weekly_connections_count_df


def generate_recruiter_proportion_df(
    connections_data: pd.DataFrame, recruiter_mapper: list
) -> pd.DataFrame:

    recruiters_percentage_df = (
        connections_data.assign(
            is_recruiter=connections_data["position"].str.contains(
                "|".join(recruiter_mapper), flags=re.IGNORECASE, regex=True
            )
        )
        .groupby("is_recruiter")
        .size()
        .reset_index(name="count")
    )
    return recruiters_percentage_df


def generate_positions_count_df(
    connections_data: pd.DataFrame, position_mapper: dict
) -> pd.DataFrame:
    def _get_job_position(text, keyword_dict):

        for job_title, keywords in keyword_dict.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    return job_title
        return "Other"

    connections_data["mapped_position"] = connections_data["position"].apply(
        lambda text: _get_job_position(text, position_mapper)
    )

    positions_count = (
        connections_data.groupby("mapped_position").size().reset_index(name="count")
    )

    connections_data.to_csv("analysis.csv")
    return positions_count


def generate_companies_count(connections_data: pd.DataFrame, top: int) -> pd.DataFrame:
    companies_count_df = (
        connections_data.groupby("company")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .iloc[:top]
    )
    return companies_count_df


main()
