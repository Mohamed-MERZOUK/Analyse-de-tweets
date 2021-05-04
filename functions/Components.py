
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def card(title="card", value="120", progress="80", icon="icon-book-open", color="#138496", bg_color="bg-info"):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H3(
                                                value, className="primary"
                                            ),
                                            html.Span(
                                                title
                                            ),

                                        ],
                                        className="media-body text-left",
                                        style={
                                            "color": color}

                                    ),
                                    html.Div(
                                        [
                                            html.I(
                                                className=icon+" primary font-large-2 float-right")

                                        ], className="align-self-center",
                                        style={
                                            "color": color}
                                    ),
                                ], className="media d-flex"
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        className="progress-bar "+bg_color,
                                        style={
                                            "width": "80%"},
                                        **{"aria-valuenow": progress, "aria-valuemin": "0", "aria-valuemax": "100"}
                                    )

                                ], className="progress mt-1 mb-0", style={"height": "7px"}
                            )


                        ], className="card-body",

                    )
                ], className="card-content"
            )
        ], className='card'
    )
