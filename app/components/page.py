from typing import Callable
import reflex as rx

from app.components.navbar import navbar


def page_layout(
    *children,
    title: str,
    description: str,
    on_mount: Callable | None = None,
) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(title, class_name="text-3xl font-bold text-gray-900 mb-2"),
                rx.el.p(description, class_name="text-gray-600 mb-8"),
                *children,
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-10 bg-gray-50 min-h-screen",
        ),
        on_mount=on_mount,
        class_name="font-['Inter']",
    )
