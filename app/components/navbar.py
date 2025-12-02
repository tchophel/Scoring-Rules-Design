import reflex as rx
from app.states.base_state import BaseState


def navbar_link(text: str, url: str, icon_tag: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_tag, class_name="w-4 h-4 mr-2"),
            rx.el.span(text),
            class_name="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50 transition-colors",
        ),
        href=url,
    )


def mobile_navbar_link(text: str, url: str, icon_tag: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_tag, class_name="w-5 h-5 mr-3"),
            rx.el.span(text),
            class_name="flex items-center px-3 py-3 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50 transition-colors",
        ),
        href=url,
        on_click=BaseState.close_mobile_menu,
        class_name="block w-full",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.a(
                            rx.icon(
                                "trophy", class_name="h-8 w-8 text-indigo-600 mr-2"
                            ),
                            rx.el.span(
                                "ScorePredictor",
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            href="/",
                            class_name="flex items-center flex-shrink-0 mr-10",
                        ),
                        rx.el.div(
                            navbar_link("Home", "/", "home"),
                            navbar_link("Leaderboard", "/leaderboard", "bar-chart-2"),
                            rx.cond(
                                BaseState.is_authenticated,
                                navbar_link(
                                    "My Predictions", "/my-predictions", "list"
                                ),
                                rx.fragment(),
                            ),
                            rx.cond(
                                BaseState.is_admin,
                                navbar_link("Admin Panel", "/admin", "shield"),
                                rx.fragment(),
                            ),
                            class_name="hidden md:flex items-center space-x-4",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.cond(
                        BaseState.is_authenticated,
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "user", class_name="h-4 w-4 mr-2 text-gray-500"
                                ),
                                rx.el.span(
                                    BaseState.current_user.username,
                                    class_name="text-sm font-medium text-gray-700",
                                ),
                                class_name="flex items-center mr-4 bg-gray-100 px-3 py-1 rounded-full",
                            ),
                            rx.el.button(
                                "Logout",
                                on_click=BaseState.logout,
                                class_name="text-sm font-medium text-red-600 hover:text-red-800 transition-colors",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.el.a(
                                rx.el.button(
                                    "Sign In",
                                    class_name="text-gray-600 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors mr-2",
                                ),
                                href="/login",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Get Started",
                                    class_name="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm hover:shadow-md",
                                ),
                                href="/register",
                            ),
                            class_name="flex items-center",
                        ),
                    ),
                    class_name="hidden md:flex items-center",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            BaseState.is_mobile_menu_open,
                            rx.icon("x", class_name="block h-6 w-6"),
                            rx.icon("menu", class_name="block h-6 w-6"),
                        ),
                        on_click=BaseState.toggle_mobile_menu,
                        class_name="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500",
                    ),
                    class_name="flex md:hidden",
                ),
                class_name="flex items-center justify-between h-16",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        rx.cond(
            BaseState.is_mobile_menu_open,
            rx.el.div(
                rx.el.div(
                    mobile_navbar_link("Home", "/", "home"),
                    mobile_navbar_link("Leaderboard", "/leaderboard", "bar-chart-2"),
                    rx.cond(
                        BaseState.is_authenticated,
                        mobile_navbar_link("My Predictions", "/my-predictions", "list"),
                        rx.fragment(),
                    ),
                    rx.cond(
                        BaseState.is_admin,
                        mobile_navbar_link("Admin Panel", "/admin", "shield"),
                        rx.fragment(),
                    ),
                    class_name="px-2 pt-2 pb-3 space-y-1",
                ),
                rx.el.div(
                    rx.cond(
                        BaseState.is_authenticated,
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "user",
                                        class_name="h-8 w-8 rounded-full text-gray-500 bg-gray-100 p-1",
                                    ),
                                    class_name="flex-shrink-0",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        BaseState.current_user.username,
                                        class_name="text-base font-medium text-gray-800",
                                    ),
                                    rx.el.div(
                                        rx.cond(
                                            BaseState.current_user.is_admin,
                                            "Administrator",
                                            "Member",
                                        ),
                                        class_name="text-sm font-medium text-gray-500",
                                    ),
                                    class_name="ml-3",
                                ),
                                class_name="flex items-center px-5",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.el.div(
                                        rx.icon("log-out", class_name="w-5 h-5 mr-3"),
                                        rx.el.span("Sign out"),
                                        class_name="flex items-center",
                                    ),
                                    on_click=BaseState.logout,
                                    class_name="mt-3 block w-full text-left px-3 py-3 rounded-md text-base font-medium text-red-600 hover:text-red-800 hover:bg-gray-50",
                                ),
                                class_name="mt-3 px-2 space-y-1",
                            ),
                            class_name="pt-4 pb-4 border-t border-gray-200",
                        ),
                        rx.el.div(
                            rx.el.a(
                                rx.el.button(
                                    "Sign In",
                                    class_name="block w-full text-center px-4 py-3 rounded-md text-base font-medium text-indigo-600 bg-gray-50 hover:bg-gray-100",
                                ),
                                href="/login",
                                class_name="block px-5 py-2",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Get Started",
                                    class_name="block w-full text-center px-4 py-3 rounded-md text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm",
                                ),
                                href="/register",
                                class_name="block px-5 py-2",
                            ),
                            class_name="pt-4 pb-4 border-t border-gray-200",
                        ),
                    )
                ),
                class_name="md:hidden bg-white border-b border-gray-200 shadow-lg",
            ),
            rx.fragment(),
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-50",
    )