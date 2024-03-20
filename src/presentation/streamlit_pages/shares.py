from numpy import log
import streamlit as st
from src.domain.use_cases.get_all_shares.get_all_shares import AllSharesGetter
import pandas as pd
import plotly.express as px
from src.presentation import styles


class SharesPage:
    def __init__(self, all_shares_getter=AllSharesGetter) -> None:
        self.__all_shares_getter = all_shares_getter

    def main(self):
        st.set_page_config(
            page_title="Shares Analysis",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.markdown(styles.css_styles, unsafe_allow_html=True)

        shares_data = (
            self.__all_shares_getter()
            .get_all()
            .sort_values(by="shared_date", ascending=True)
            .reset_index(drop=True)
        )
        shares_data["id"] = shares_data.index + 1
        shares_data["log_reactions"] = log(shares_data.num_of_reactions)
        shares_data["log_comments"] = [
            log(n_comments) if n_comments > 0 else 0
            for n_comments in shares_data.num_of_comments
        ]

        total_shares = len(shares_data)
        avg_likes_per_share = round(shares_data["num_of_reactions"].mean(), 1)
        avg_comments_per_share = round(shares_data["num_of_comments"].mean(), 1)

        st.write("## Shares Analysis")

        row1 = st.columns([0.2, 0.4, 0.4])
        with row1[0]:
            st.metric(
                "Number of Shares",
                total_shares,
            )
            st.metric("Average Likes per Share", avg_likes_per_share)
            st.metric("Average Comments per Share", avg_comments_per_share)

        with row1[1]:
            fig = px.line(
                shares_data.loc[shares_data.num_of_reactions.notna()],
                x="id",
                y="num_of_reactions",
                title="Number of Reactions by Share ID",
                height=267,
                markers=True,
                log_y=True,
            )
            fig.update_layout(
                margin=dict(t=30, b=0),
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                title=styles.title_chart_config,
                yaxis_title=None,
                xaxis_title=None,
            )

            fig.update_traces(line_color="#BE5CFF", line_width=2)

            st.container(border=True).plotly_chart(fig, use_container_width=True)

        with row1[2]:
            fig = px.line(
                shares_data.loc[shares_data.num_of_comments.notna()],
                x="id",
                y="num_of_comments",
                title="Number of comments by Share ID",
                height=267,
                markers=True,
                log_y=True,
            )
            fig.update_layout(
                margin=dict(t=30, b=0),
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                title=styles.title_chart_config,
                yaxis_title=None,
                xaxis_title=None,
            )
            fig.update_traces(line_color="#FEFF8D", line_width=2)

            st.container(border=True).plotly_chart(fig, use_container_width=True)

        row2 = st.columns([0.7, 0.3])
        with row2[0]:
            shares_by_month_year = self.__generate_shares_by_month_year_df(shares_data)
            fig = px.bar(
                shares_by_month_year,
                x="month_year",
                y="count",
                title="Number of Shares by Month-Year",
            )
            fig.update_layout(
                margin=dict(t=30, b=0),
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                title=styles.title_chart_config,
                yaxis_title=None,
                xaxis_title=None,
            )
            st.container(border=True).plotly_chart(fig, use_container_width=True)

        with row2[1]:
            total_reactions = shares_data["num_of_reactions"].sum()
            total_comments = shares_data["num_of_comments"].sum() + len(shares_data)

            ratio = total_reactions / (total_comments if total_comments > 0 else 1)

            labels = ["Reactions", "Comments"]
            fig = px.pie(
                values=[total_reactions, total_comments],
                names=labels,
                title="Ratio of Reactions to Comments",
                hole=0.8,
                color_discrete_sequence=["#BE5CFF", "#FEFF8D"],
            )

            fig.update_layout(
                margin=dict(t=30, b=0),
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                title=styles.title_chart_config,
                annotations=[
                    dict(text=ratio, x=0.5, y=0.5, font_size=40, showarrow=False)
                ],
            )
            fig.update_traces(textinfo="none")

            st.container(border=True).plotly_chart(fig, use_container_width=True)

    @staticmethod
    def __generate_shares_by_month_year_df(shares_data: pd.DataFrame) -> pd.DataFrame:
        shares_data["month_year"] = shares_data["shared_date"].dt.strftime("%b-%Y")
        shares_by_month_year = (
            shares_data.groupby("month_year").size().reset_index(name="count")
        )

        all_months = pd.date_range(
            start=shares_data["shared_date"].min(),
            end=shares_data["shared_date"].max(),
            freq="M",
        ).strftime("%b-%Y")
        all_months_df = pd.DataFrame(all_months, columns=["month_year"])
        shares_by_month_year = all_months_df.merge(
            shares_by_month_year, on="month_year", how="left"
        ).fillna(0)
        shares_by_month_year["count"] = shares_by_month_year["count"].astype(int)

        return shares_by_month_year


SharesPage().main()
