import re
import streamlit as st
from src.domain.use_cases.get_all_connections.get_all_connections import (
    AllConnectionsGetter,
)
import pandas as pd
import altair as alt
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
    background-image: url("https://i.imgur.com/T5TympJ.png");
    background-size: cover;
    }
    </style>
    """
    # https://fakeimg.pl/600x400

    title_chart_config = {
        "fontSize": 20,
        "font": "Source Sans Pro",
        "anchor": "start",
        "color": "white",
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

    percentage_recruiters = round(
        int(
            proportion_recruiters_df.loc[
                proportion_recruiters_df["is_recruiter"].astype(bool) == (True,)
            ]["count"]
        )
        / connections_count
        * 100,
        1,
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

    st.altair_chart(
        alt.Chart(weekly_connections_count_df.sort_index())
        .mark_bar()
        .encode(
            x=alt.X("week_year", sort=None, title=""),
            y=alt.Y("count", title=""),
            tooltip=["week_year", "count"],
        )
        .properties(height=300, title="Number of new Connections by week-year")
        .configure_title(**title_chart_config)
        .configure_scale(continuousPadding=10),
        use_container_width=True,
    )

    row3 = st.columns([0.4, 0.4, 0.3], gap="medium")
    with row3[0]:
        st.altair_chart(
            alt.Chart(positions_count.sort_index())
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title=""),
                y=alt.Y("mapped_position:N", sort="-x", title=""),
                tooltip=["mapped_position", "count"],
            )
            .properties(height=300, title="Number of Connections by job position")
            .configure_title(**title_chart_config),
            use_container_width=True,
        )

    with row3[1]:
        st.altair_chart(
            alt.Chart(group_by_companies_count)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title=""),
                y=alt.Y("company:N", sort=None, title=""),
            )
            .properties(height=300, title="Number of Connections by company")
            .configure_title(**title_chart_config),
            use_container_width=True,
        )

    with row3[2]:
        # st.write("#### Proportion of Recruiters (%)")
        proportion_rec_donut = (
            alt.Chart(proportion_recruiters_df)
            .mark_arc(innerRadius=110)
            .encode(
                theta="count",
                color=alt.Color("is_recruiter:N"),
                tooltip=["is_recruiter", "count"],
            )
            .properties(height=300, title="Proportion of Recruiters (%)")
        )

        text_inside_donut = proportion_rec_donut.mark_text(
            align="center",
            baseline="middle",
            fontSize=60,
            fontWeight="bold",
            color="white",
        ).encode(text=alt.value(f"{percentage_recruiters} %"))

        st.altair_chart(
            alt.layer(proportion_rec_donut, text_inside_donut).configure_title(
                **title_chart_config
            ),
            use_container_width=True,
        )


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
