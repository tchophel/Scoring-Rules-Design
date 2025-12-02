import reflex as rx
from app.states.prediction_state import PredictionState
from app.components.navbar import navbar
from app.models import Match, Prediction


def prediction_stat_card(label: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
                class_name=f"flex items-center justify-center h-12 w-12 rounded-md bg-{color}-100 mb-4",
            ),
            rx.el.div(
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            ),
            class_name="flex flex-col",
        ),
        class_name="p-6 bg-white rounded-lg shadow-sm border border-gray-100",
    )


def prediction_history_row(match: Match) -> rx.Component:
    """Row for a match where the user has made a prediction."""
    pred = PredictionState.my_predictions[match.id]
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(match.team1, class_name="font-medium text-gray-900"),
                rx.el.div("vs", class_name="text-xs text-gray-400 my-1"),
                rx.el.div(match.team2, class_name="font-medium text-gray-900"),
                class_name="text-sm",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.moment(match.start_time, format="MMM D, YYYY HH:mm"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    pred.team1_prediction, class_name="font-bold text-indigo-600"
                ),
                rx.el.span(" - ", class_name="mx-1 text-gray-400"),
                rx.el.span(
                    pred.team2_prediction, class_name="font-bold text-indigo-600"
                ),
                rx.cond(
                    pred.boost_active,
                    rx.el.span(
                        rx.icon("zap", class_name="w-3 h-3 text-yellow-600"),
                        class_name="ml-2 p-1 bg-yellow-100 rounded-full inline-flex items-center justify-center",
                        title="2x Boost Active",
                    ),
                    rx.fragment(),
                ),
                class_name="text-sm flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                match.status == "finished",
                rx.el.div(
                    rx.el.span(match.team1_score, class_name="font-medium"),
                    rx.el.span(" - "),
                    rx.el.span(match.team2_score, class_name="font-medium"),
                    class_name="text-sm text-gray-900",
                ),
                rx.el.span("TBD", class_name="text-sm text-gray-400 italic"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                match.status == "finished",
                rx.el.span(
                    f"+{pred.points_earned}",
                    class_name=rx.cond(
                        pred.points_earned > 0,
                        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
                    ),
                ),
                rx.el.span("-", class_name="text-gray-300"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def prediction_mobile_card(match: Match) -> rx.Component:
    """Mobile friendly card for a prediction."""
    pred = PredictionState.my_predictions[match.id]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        rx.moment(match.start_time, format="MMM D, HH:mm"),
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    rx.cond(
                        match.status == "finished",
                        rx.el.span(
                            f"+{pred.points_earned}",
                            class_name=rx.cond(
                                pred.points_earned > 0,
                                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
                            ),
                        ),
                        rx.el.span(
                            "Upcoming",
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
                        ),
                    ),
                    class_name="flex justify-between items-center mb-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(match.team1, class_name="font-medium text-gray-900"),
                        rx.el.span(
                            match.team2,
                            class_name="font-medium text-gray-900 text-right",
                        ),
                        class_name="flex justify-between items-center mb-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Your Pick:", class_name="text-xs text-gray-500 mr-2"
                            ),
                            rx.el.span(
                                f"{pred.team1_prediction} - {pred.team2_prediction}",
                                class_name="text-sm font-bold text-indigo-600",
                            ),
                            rx.cond(
                                pred.boost_active,
                                rx.el.span(
                                    rx.icon(
                                        "zap", class_name="w-3 h-3 text-yellow-600"
                                    ),
                                    class_name="ml-2 p-1 bg-yellow-100 rounded-full inline-flex items-center justify-center",
                                ),
                                rx.fragment(),
                            ),
                            class_name="flex items-center",
                        ),
                        rx.cond(
                            match.status == "finished",
                            rx.el.div(
                                rx.el.span(
                                    "Result:", class_name="text-xs text-gray-500 mr-2"
                                ),
                                rx.el.span(
                                    f"{match.team1_score} - {match.team2_score}",
                                    class_name="text-sm font-bold text-gray-900",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex justify-between items-center bg-gray-50 p-2 rounded-md",
                    ),
                    class_name="flex flex-col",
                ),
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-lg shadow-sm border border-gray-200",
    )


def my_predictions_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "My Predictions", class_name="text-3xl font-bold text-gray-900 mb-8"
                ),
                rx.el.div(
                    prediction_stat_card(
                        "Total Points",
                        PredictionState.current_user.total_points.to_string(),
                        "trophy",
                        "indigo",
                    ),
                    prediction_stat_card(
                        "Matches Predicted",
                        PredictionState.my_prediction_list.length().to_string(),
                        "target",
                        "blue",
                    ),
                    prediction_stat_card("Accuracy", "56%", "percent", "green"),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Match",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Date",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Your Pick",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Result",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Points",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                ),
                                class_name="bg-gray-50",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    PredictionState.matches,
                                    lambda m: rx.cond(
                                        PredictionState.my_predictions.contains(m.id),
                                        prediction_history_row(m),
                                        rx.fragment(),
                                    ),
                                ),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="hidden md:block overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                    ),
                    rx.el.div(
                        rx.foreach(
                            PredictionState.matches,
                            lambda m: rx.cond(
                                PredictionState.my_predictions.contains(m.id),
                                prediction_mobile_card(m),
                                rx.fragment(),
                            ),
                        ),
                        class_name="md:hidden space-y-4",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-10 bg-gray-50 min-h-screen",
        ),
        on_mount=PredictionState.load_data,
        class_name="font-['Inter']",
    )