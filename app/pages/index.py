import reflex as rx
from app.components.navbar import navbar
from app.states.base_state import BaseState


def feature_card(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-white"),
            class_name="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white mb-4",
        ),
        rx.el.h3(title, class_name="text-lg leading-6 font-medium text-gray-900 mb-2"),
        rx.el.p(description, class_name="text-base text-gray-500"),
        class_name="p-6 bg-white rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow",
    )


def top_player_card() -> rx.Component:
    return rx.cond(
        BaseState.top_player,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("crown", class_name="h-8 w-8 text-yellow-500"),
                    class_name="p-3 bg-yellow-100 rounded-full mr-4",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Current Leader",
                        class_name="text-sm font-medium text-gray-500 uppercase tracking-wide",
                    ),
                    rx.el.div(
                        rx.el.span(
                            BaseState.top_player.username,
                            class_name="text-xl font-bold text-gray-900 mr-2",
                        ),
                        rx.el.span(
                            f"{BaseState.top_player.total_points} pts",
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="mt-8 bg-white p-4 rounded-lg shadow-sm border-l-4 border-yellow-400",
        ),
        rx.fragment(),
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        rx.el.span("Predict Scores.", class_name="block xl:inline"),
                        rx.el.span(
                            " Win Glory.", class_name="block text-indigo-600 xl:inline"
                        ),
                        class_name="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl",
                    ),
                    rx.el.p(
                        "Join the ultimate sports prediction community. Compete with friends, climb the leaderboard, and prove your sports knowledge.",
                        class_name="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0",
                    ),
                    top_player_card(),
                    rx.el.div(
                        rx.cond(
                            BaseState.is_authenticated,
                            rx.el.a(
                                rx.el.button(
                                    "View Upcoming Matches",
                                    class_name="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10",
                                ),
                                href="/matches",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Join Now",
                                    class_name="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10",
                                ),
                                href="/register",
                            ),
                        ),
                        class_name="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start",
                    ),
                    class_name="text-center lg:text-left lg:w-1/2",
                ),
                rx.el.div(
                    rx.image(
                        src="/placeholder.svg",
                        class_name="w-full h-full object-cover rounded-3xl shadow-xl",
                    ),
                    class_name="mt-10 lg:mt-0 lg:w-1/2 lg:pl-12",
                ),
                class_name="flex flex-col lg:flex-row items-center justify-between py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "How it works",
                        class_name="text-base text-indigo-600 font-semibold tracking-wide uppercase",
                    ),
                    rx.el.p(
                        "Everything you need to compete",
                        class_name="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl",
                    ),
                    class_name="text-center mb-12",
                ),
                rx.el.div(
                    feature_card(
                        "Predict Scores",
                        "Guess the exact score of upcoming matches before they start.",
                        "crosshair",
                    ),
                    feature_card(
                        "Earn Points",
                        "Get points for correct outcomes and bonus points for exact scores.",
                        "star",
                    ),
                    feature_card(
                        "Climb Ranks",
                        "Compete on the global leaderboard and show off your expertise.",
                        "trending-up",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                ),
                class_name="bg-gray-50 py-16",
            ),
            class_name="flex-grow",
        ),
        class_name="min-h-screen bg-white font-['Inter'] flex flex-col",
    )