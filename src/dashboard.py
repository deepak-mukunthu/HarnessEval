"""Interactive dashboard for visualizing harness evaluation results."""

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
from dash import Dash, dcc, html, Input, Output
import dash


def load_latest_results(results_dir: Path = Path("data/results")):
    """Load the most recent experiment results."""
    results_dir = Path(results_dir)

    session_files = sorted(results_dir.glob("*_sessions.json"))
    interaction_files = sorted(results_dir.glob("*_interactions.json"))

    if not session_files or not interaction_files:
        print("No results found. Run run_experiment.py first.")
        return None, None

    latest_sessions = session_files[-1]
    latest_interactions = interaction_files[-1]

    with open(latest_sessions) as f:
        sessions = json.load(f)

    with open(latest_interactions) as f:
        interactions = json.load(f)

    return pd.DataFrame(sessions), pd.DataFrame(interactions)


def create_comparison_chart(df_sessions):
    """Create a comparison chart of harness performance."""
    metrics = [
        "avg_response_length",
        "total_hints",
        "total_questions",
        "total_concepts",
        "estimated_understanding",
    ]

    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=[
            "Avg Response Length",
            "Total Hints Given",
            "Questions Asked",
            "Concepts Explained",
            "Estimated Understanding",
            "Success Rate",
        ],
    )

    harness_groups = df_sessions.groupby("harness_name")

    row_col_positions = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]

    for idx, (metric, (row, col)) in enumerate(
        zip(metrics, row_col_positions[:-1])
    ):
        avg_by_harness = harness_groups[metric].mean().sort_values()

        fig.add_trace(
            go.Bar(
                x=avg_by_harness.index,
                y=avg_by_harness.values,
                name=metric,
                showlegend=False,
            ),
            row=row,
            col=col,
        )

    success_rate = (
        harness_groups["student_reached_answer"].mean().sort_values()
    )
    fig.add_trace(
        go.Bar(
            x=success_rate.index,
            y=success_rate.values * 100,
            name="Success Rate",
            showlegend=False,
        ),
        row=2,
        col=3,
    )

    fig.update_layout(
        height=800,
        title_text="Harness Performance Comparison",
        showlegend=False,
    )

    return fig


def create_radar_chart(df_sessions):
    """Create a radar chart comparing harnesses across dimensions."""
    harness_groups = df_sessions.groupby("harness_name")

    metrics = {
        "Understanding": "estimated_understanding",
        "Hints": "total_hints",
        "Questions": "total_questions",
        "Concepts": "total_concepts",
        "Efficiency": "total_interactions",
    }

    fig = go.Figure()

    for harness_name, group in harness_groups:
        values = []
        for metric_name, col in metrics.items():
            if col == "total_interactions":
                val = 1 / (group[col].mean() + 1)
            else:
                val = group[col].mean()

            max_val = df_sessions[col].max()
            if col == "total_interactions":
                max_val = 1
            values.append(val / max_val if max_val > 0 else 0)

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=list(metrics.keys()),
                fill="toself",
                name=harness_name,
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Harness Performance Radar",
        height=600,
    )

    return fig


def create_interaction_timeline(df_interactions):
    """Create timeline visualization of interactions."""
    df_interactions["timestamp"] = pd.to_datetime(
        df_interactions["timestamp"], unit="s"
    )

    fig = px.scatter(
        df_interactions,
        x="timestamp",
        y="harness_name",
        color="harness_name",
        size="response_length",
        hover_data=["problem_id", "hints_given", "questions_asked"],
        title="Interaction Timeline (bubble size = response length)",
        height=500,
    )

    return fig


def create_problem_difficulty_chart(df_sessions):
    """Create chart showing performance by problem."""
    problem_performance = (
        df_sessions.groupby(["harness_name", "problem_id"])
        .agg(
            {
                "estimated_understanding": "mean",
                "total_interactions": "mean",
                "student_reached_answer": "mean",
            }
        )
        .reset_index()
    )

    fig = px.bar(
        problem_performance,
        x="problem_id",
        y="estimated_understanding",
        color="harness_name",
        barmode="group",
        title="Understanding Level by Problem and Harness",
        labels={
            "problem_id": "Problem ID",
            "estimated_understanding": "Understanding",
        },
        height=500,
    )

    return fig


def create_dashboard():
    """Create and run the Dash dashboard."""
    df_sessions, df_interactions = load_latest_results()

    if df_sessions is None:
        print("No data available. Please run the experiment first.")
        return

    app = Dash(__name__)

    app.layout = html.Div(
        [
            html.H1(
                "MathTutor Harness Evaluation Dashboard",
                style={"textAlign": "center", "padding": "20px"},
            ),
            html.Div(
                [
                    html.H3("Overview Statistics"),
                    html.Div(id="summary-stats"),
                ],
                style={"padding": "20px"},
            ),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Performance Comparison",
                        children=[
                            dcc.Graph(
                                figure=create_comparison_chart(df_sessions)
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Radar View",
                        children=[
                            dcc.Graph(figure=create_radar_chart(df_sessions))
                        ],
                    ),
                    dcc.Tab(
                        label="Problem Analysis",
                        children=[
                            dcc.Graph(
                                figure=create_problem_difficulty_chart(
                                    df_sessions
                                )
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Interaction Timeline",
                        children=[
                            dcc.Graph(
                                figure=create_interaction_timeline(
                                    df_interactions
                                )
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Raw Data",
                        children=[
                            html.H3("Session Data"),
                            html.Div(
                                dash.dash_table.DataTable(
                                    data=df_sessions.to_dict("records"),
                                    columns=[
                                        {"name": i, "id": i}
                                        for i in df_sessions.columns
                                    ],
                                    page_size=15,
                                    style_table={
                                        "overflowX": "auto",
                                        "padding": "20px",
                                    },
                                )
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )

    @app.callback(
        Output("summary-stats", "children"), Input("summary-stats", "id")
    )
    def update_summary(_):
        harness_stats = df_sessions.groupby("harness_name").agg(
            {
                "estimated_understanding": "mean",
                "total_interactions": "mean",
                "total_hints": "sum",
                "student_reached_answer": "mean",
            }
        )

        summary_cards = []
        for harness, row in harness_stats.iterrows():
            card = html.Div(
                [
                    html.H4(harness),
                    html.P(
                        f"Avg Understanding: {row['estimated_understanding']:.2f}"
                    ),
                    html.P(
                        f"Avg Interactions: {row['total_interactions']:.1f}"
                    ),
                    html.P(f"Total Hints: {row['total_hints']:.0f}"),
                    html.P(
                        f"Success Rate: {row['student_reached_answer']:.1%}"
                    ),
                ],
                style={
                    "border": "1px solid #ddd",
                    "padding": "15px",
                    "margin": "10px",
                    "borderRadius": "5px",
                    "display": "inline-block",
                    "width": "18%",
                },
            )
            summary_cards.append(card)

        return summary_cards

    print("\n" + "=" * 60)
    print("Starting Dashboard...")
    print("=" * 60)
    print("Dashboard will open at: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    app.run_server(debug=True, port=8050)


if __name__ == "__main__":
    create_dashboard()
