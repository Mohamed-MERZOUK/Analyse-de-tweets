
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
                                            "width": progress+"%"},
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


def cardMultiProgress(title1="Hommes", title2="Femmes", value1="120", value2="120", progress1="80", progress2="30", color1="text-c-red", bg_color1="bg-c-red", color2="text-c-green", bg_color2="bg-c-green"):
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
                                            html.Div(
                                                [

                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.H6(
                                                                        title1),
                                                                    html.H5(
                                                                        [
                                                                            value1,
                                                                            html.Span(
                                                                                "-10%",
                                                                                className=color1 + " m-l-10"
                                                                            )
                                                                        ],
                                                                        className="m-b-30 f-w-700"
                                                                    ),
                                                                    html.Div(
                                                                        html.Div(
                                                                            className="newprogress-bar " + bg_color1,
                                                                            style={
                                                                                "width": progress1 + "%"}
                                                                        ),
                                                                        className="newprogress"
                                                                    ),
                                                                ]

                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.H6(
                                                                        title2),
                                                                    html.H5(
                                                                        [
                                                                            value2,
                                                                            html.Span(
                                                                                "+10%",
                                                                                className=color2 + " m-l-10"
                                                                            )
                                                                        ],
                                                                        className="m-b-30 f-w-700"
                                                                    ),
                                                                    html.Div(
                                                                        html.Div(
                                                                            className="newprogress-bar " + bg_color2,
                                                                            style={
                                                                                "width": progress2 + "%"}
                                                                        ),
                                                                        className="newprogress"
                                                                    ),
                                                                ]

                                                            )
                                                        ]

                                                    )

                                                ],
                                                className="card-body",
                                            )

                                        ],
                                        className="card proj-progress-card"

                                    ),

                                ], className="col-xl-12"
                            ),


                        ], className="row d-flex justify-content-center",

                    )
                ]
            )

        ], className='page-content page-container', id="page-content"
    )
