import reflex as rx
from app.states.prediction_state import PredictionState
from app.components.navbar import navbar
from app.models import Match, Prediction


def match_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "upcoming",
            rx.el.span(
                "Upcoming",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
        ),
        (
            "live",
            rx.el.span(
                "LIVE",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 animate-pulse",
            ),
        ),
        (
            "finished",
            rx.el.span(
                "Finished",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
            ),
        ),
        rx.el.span(status),
    )


def prediction_form(match: Match) -> rx.Component:
    """Component to render the prediction form or current prediction."""
    return rx.cond(
        PredictionState.my_predictions.contains(match.id),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Your Prediction:",
                        class_name="text-xs text-gray-500 uppercase tracking-wide font-semibold",
                    ),
                    rx.cond(
                        PredictionState.my_predictions[match.id].boost_active,
                        rx.el.span(
                            rx.icon("zap", class_name="w-3 h-3 mr-1 inline"),
                            "2x Active",
                            class_name="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center justify-center gap-2",
                ),
                rx.el.div(
                    rx.el.span(
                        PredictionState.my_predictions[match.id].team1_prediction,
                        class_name="text-2xl font-bold text-indigo-600",
                    ),
                    rx.el.span(" - ", class_name="mx-2 text-gray-400"),
                    rx.el.span(
                        PredictionState.my_predictions[match.id].team2_prediction,
                        class_name="text-2xl font-bold text-indigo-600",
                    ),
                    class_name="flex items-center justify-center mt-1",
                ),
                class_name="text-center",
            ),
            rx.cond(
                match.status == "upcoming",
                rx.el.form(
                    rx.el.input(
                        type="hidden", name="match_id", value=match.id.to_string()
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Update Score",
                                class_name="block text-xs text-gray-500 mb-1",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="number",
                                    name="team1_score",
                                    default_value=PredictionState.my_predictions[
                                        match.id
                                    ].team1_prediction.to_string(),
                                    min="0",
                                    class_name="w-12 text-center border border-gray-300 rounded-md p-1 text-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                rx.el.span("-", class_name="mx-2 text-gray-400"),
                                rx.el.input(
                                    type="number",
                                    name="team2_score",
                                    default_value=PredictionState.my_predictions[
                                        match.id
                                    ].team2_prediction.to_string(),
                                    min="0",
                                    class_name="w-12 text-center border border-gray-300 rounded-md p-1 text-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                class_name="flex items-center justify-center",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    name="boost_active",
                                    default_checked=PredictionState.my_predictions[
                                        match.id
                                    ].boost_active,
                                    class_name="rounded border-gray-300 text-yellow-600 shadow-sm focus:border-yellow-300 focus:ring focus:ring-yellow-200 focus:ring-opacity-50 mr-2",
                                ),
                                rx.icon(
                                    "zap", class_name="w-4 h-4 text-yellow-500 mr-1"
                                ),
                                rx.el.span(
                                    "2x Boost",
                                    class_name="text-sm font-medium text-gray-700",
                                ),
                                class_name="flex items-center justify-center mt-3",
                            ),
                            class_name="flex justify-center w-full",
                        ),
                        rx.el.button(
                            "Update",
                            type="submit",
                            class_name="w-full mt-3 px-3 py-2 bg-white border border-gray-300 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-50 shadow-sm",
                        ),
                        class_name="flex flex-col items-center justify-center mt-3 pt-3 border-t border-gray-100",
                    ),
                    on_submit=PredictionState.submit_prediction,
                ),
                rx.cond(
                    match.status == "finished",
                    rx.el.div(
                        rx.el.span(
                            "Points Earned: ", class_name="text-sm text-gray-600"
                        ),
                        rx.el.span(
                            PredictionState.my_predictions[match.id].points_earned,
                            class_name="text-sm font-bold text-green-600",
                        ),
                        class_name="mt-2 text-center bg-green-50 rounded-md py-1",
                    ),
                    rx.fragment(),
                ),
            ),
            class_name="mt-4",
        ),
        rx.cond(
            match.status == "upcoming",
            rx.el.form(
                rx.el.input(type="hidden", name="match_id", value=match.id.to_string()),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Predict Score",
                            class_name="block text-xs text-gray-500 mb-2 text-center",
                        ),
                        rx.el.div(
                            rx.el.input(
                                type="number",
                                name="team1_score",
                                placeholder="0",
                                min="0",
                                class_name="w-16 text-center border border-gray-300 rounded-md p-2 shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                            ),
                            rx.el.span("-", class_name="mx-2 text-gray-400 font-bold"),
                            rx.el.input(
                                type="number",
                                name="team2_score",
                                placeholder="0",
                                min="0",
                                class_name="w-16 text-center border border-gray-300 rounded-md p-2 shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                            ),
                            class_name="flex items-center justify-center",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                name="boost_active",
                                class_name="rounded border-gray-300 text-yellow-600 shadow-sm focus:border-yellow-300 focus:ring focus:ring-yellow-200 focus:ring-opacity-50 mr-2",
                            ),
                            rx.icon("zap", class_name="w-4 h-4 text-yellow-500 mr-1"),
                            rx.el.span(
                                "Use 2x Boost",
                                class_name="text-sm font-medium text-gray-700",
                            ),
                            class_name="flex items-center justify-center mt-4 p-2 bg-yellow-50 rounded-md border border-yellow-100",
                        ),
                        class_name="flex justify-center w-full",
                    ),
                    class_name="mb-3",
                ),
                rx.el.button(
                    "Submit Prediction",
                    type="submit",
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mt-4",
                ),
                on_submit=PredictionState.submit_prediction,
                class_name="mt-4",
            ),
            rx.el.div(
                "Prediction Closed",
                class_name="mt-4 text-center text-sm text-gray-500 italic",
            ),
        ),
    )


def match_card(match: Match) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                match_status_badge(match.status),
                rx.el.span(
                    rx.moment(match.start_time, from_now=True),
                    class_name="text-xs text-gray-500 ml-2",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        match.team1,
                        class_name="text-lg font-bold text-gray-900 truncate",
                    ),
                    class_name="flex-1 text-right pr-4",
                ),
                rx.el.div(
                    rx.cond(
                        match.status != "upcoming",
                        rx.el.div(
                            rx.el.span(
                                match.team1_score,
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                            rx.el.span("-", class_name="mx-2 text-gray-400"),
                            rx.el.span(
                                match.team2_score,
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                            class_name="flex items-center justify-center bg-gray-100 rounded-lg px-3 py-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "VS",
                                class_name="text-sm font-medium text-gray-400 bg-gray-50 rounded-full px-2 py-1",
                            ),
                            class_name="flex items-center justify-center",
                        ),
                    ),
                    class_name="w-24 flex justify-center",
                ),
                rx.el.div(
                    rx.el.h3(
                        match.team2,
                        class_name="text-lg font-bold text-gray-900 truncate",
                    ),
                    class_name="flex-1 text-left pl-4",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.cond(
                PredictionState.is_authenticated,
                rx.el.div(
                    prediction_form(match), class_name="border-t border-gray-100 pt-4"
                ),
                rx.el.div(
                    rx.el.a(
                        "Login to predict",
                        href="/login",
                        class_name="block w-full text-center text-indigo-600 hover:text-indigo-800 text-sm font-medium mt-4",
                    )
                ),
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def matches_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Match Center", class_name="text-3xl font-bold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Predict scores for upcoming matches and track live games.",
                    class_name="text-gray-600 mb-8",
                ),
                rx.el.div(
                    rx.el.nav(
                        rx.el.button(
                            "Upcoming",
                            on_click=PredictionState.set_active_tab("upcoming"),
                            class_name=rx.cond(
                                PredictionState.active_tab == "upcoming",
                                "border-indigo-500 text-indigo-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm",
                                "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm",
                            ),
                        ),
                        rx.el.button(
                            "Live",
                            on_click=PredictionState.set_active_tab("live"),
                            class_name=rx.cond(
                                PredictionState.active_tab == "live",
                                "border-indigo-500 text-indigo-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ml-8",
                                "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ml-8",
                            ),
                        ),
                        rx.el.button(
                            "Finished",
                            on_click=PredictionState.set_active_tab("finished"),
                            class_name=rx.cond(
                                PredictionState.active_tab == "finished",
                                "border-indigo-500 text-indigo-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ml-8",
                                "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ml-8",
                            ),
                        ),
                        class_name="-mb-px flex space-x-8",
                    ),
                    class_name="border-b border-gray-200 mb-8 overflow-x-auto",
                ),
                rx.cond(
                    PredictionState.active_tab == "upcoming",
                    rx.el.div(
                        rx.foreach(PredictionState.upcoming_matches, match_card),
                        class_name="grid gap-6 md:grid-cols-2 xl:grid-cols-3",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    PredictionState.active_tab == "live",
                    rx.cond(
                        PredictionState.live_matches.length() > 0,
                        rx.el.div(
                            rx.foreach(PredictionState.live_matches, match_card),
                            class_name="grid gap-6 md:grid-cols-2 xl:grid-cols-3",
                        ),
                        rx.el.div(
                            rx.icon("radio", class_name="h-12 w-12 text-gray-300 mb-3"),
                            rx.el.p(
                                "No live matches at the moment.",
                                class_name="text-gray-500",
                            ),
                            class_name="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200",
                        ),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    PredictionState.active_tab == "finished",
                    rx.el.div(
                        rx.foreach(PredictionState.finished_matches, match_card),
                        class_name="grid gap-6 md:grid-cols-2 xl:grid-cols-3",
                    ),
                    rx.fragment(),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-10 bg-gray-50 min-h-screen",
        ),
        on_mount=PredictionState.load_data,
        class_name="font-['Inter']",
    )