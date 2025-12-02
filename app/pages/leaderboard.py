import reflex as rx
from app.components.navbar import navbar
from app.states.leaderboard_state import LeaderboardState
from app.models import User


def leaderboard_row(item: tuple[int, User]) -> rx.Component:
    index = item[0]
    user = item[1]
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.cond(
                    index == 0,
                    rx.icon("trophy", class_name="h-5 w-5 text-yellow-500 mr-2"),
                    rx.cond(
                        index == 1,
                        rx.icon("medal", class_name="h-5 w-5 text-gray-400 mr-2"),
                        rx.cond(
                            index == 2,
                            rx.icon("medal", class_name="h-5 w-5 text-orange-400 mr-2"),
                            rx.el.span(
                                f"#{index + 1}", class_name="w-5 mr-2 text-gray-500"
                            ),
                        ),
                    ),
                ),
                class_name="flex items-center justify-center font-bold text-gray-700",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-center",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "user",
                        class_name="h-8 w-8 text-gray-400 bg-gray-100 rounded-full p-1 mr-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            user.username,
                            class_name="text-sm font-medium text-gray-900",
                        ),
                        rx.el.div(
                            rx.cond(user.is_admin, "Pro Member", "Member"),
                            class_name="text-xs text-gray-500",
                        ),
                    ),
                    class_name="flex items-center",
                )
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    user.total_points,
                    class_name="text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full",
                ),
                class_name="flex justify-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-center",
        ),
    )


def leaderboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Global Leaderboard",
                        class_name="text-3xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Top players competing for glory",
                        class_name="mt-2 text-gray-600",
                    ),
                    class_name="text-center mb-10",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Rank",
                                        class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-24",
                                    ),
                                    rx.el.th(
                                        "Player",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Total Points",
                                        class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-32",
                                    ),
                                ),
                                class_name="bg-gray-50",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    LeaderboardState.ranked_users, leaderboard_row
                                ),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="overflow-x-auto shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                    ),
                    class_name="max-w-4xl mx-auto",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-10 bg-gray-50 min-h-screen",
        ),
        on_mount=LeaderboardState.load_leaderboard,
        class_name="font-['Inter']",
    )