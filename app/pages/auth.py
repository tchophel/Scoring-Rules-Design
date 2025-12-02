import reflex as rx
from app.states.auth_state import AuthState
from app.components.navbar import navbar


def auth_layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("trophy", class_name="mx-auto h-12 w-12 text-indigo-600"),
                    rx.el.h2(
                        title,
                        class_name="mt-6 text-center text-3xl font-extrabold text-gray-900",
                    ),
                    class_name="sm:mx-auto sm:w-full sm:max-w-md",
                ),
                rx.el.div(content, class_name="mt-8 sm:mx-auto sm:w-full sm:max-w-md"),
                class_name="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8",
            ),
            class_name="min-h-[calc(100vh-4rem)] bg-gray-50",
        ),
        class_name="font-['Inter']",
    )


def login_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Username", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="text",
                            required=True,
                            name="username",
                            class_name="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        ),
                        class_name="mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="password",
                            required=True,
                            name="password",
                            class_name="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        ),
                        class_name="mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-4 w-4 text-red-400 mr-2"
                            ),
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-sm text-red-700",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="bg-red-50 border-l-4 border-red-400 p-4 mb-6",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Sign in",
                        type="submit",
                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                    )
                ),
                on_submit=AuthState.handle_login,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="w-full border-t border-gray-300"),
                    class_name="absolute inset-0 flex items-center",
                ),
                rx.el.div(
                    rx.el.span("Or", class_name="px-2 bg-white text-sm text-gray-500"),
                    class_name="relative flex justify-center text-sm",
                ),
                class_name="relative my-6",
            ),
            rx.el.div(
                rx.el.a(
                    "Don't have an account? Register",
                    href="/register",
                    class_name="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50",
                )
            ),
            class_name="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10",
        ),
        "Sign in to your account",
    )


def register_page() -> rx.Component:
    return auth_layout(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Username", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="text",
                            required=True,
                            name="username",
                            class_name="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        ),
                        class_name="mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="password",
                            required=True,
                            name="password",
                            class_name="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        ),
                        class_name="mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Confirm Password",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.div(
                        rx.el.input(
                            type="password",
                            required=True,
                            name="confirm_password",
                            class_name="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        ),
                        class_name="mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-4 w-4 text-red-400 mr-2"
                            ),
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-sm text-red-700",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="bg-red-50 border-l-4 border-red-400 p-4 mb-6",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Register",
                        type="submit",
                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                    )
                ),
                on_submit=AuthState.handle_register,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="w-full border-t border-gray-300"),
                    class_name="absolute inset-0 flex items-center",
                ),
                rx.el.div(
                    rx.el.span("Or", class_name="px-2 bg-white text-sm text-gray-500"),
                    class_name="relative flex justify-center text-sm",
                ),
                class_name="relative my-6",
            ),
            rx.el.div(
                rx.el.a(
                    "Already have an account? Sign in",
                    href="/login",
                    class_name="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50",
                )
            ),
            class_name="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10",
        ),
        "Create your account",
    )