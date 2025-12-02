import reflex as rx
from app.states.admin_state import AdminState
from app.components.navbar import navbar
from app.models import User, Match, Payment, Prediction


def tab_button(name: str, label: str, icon: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-5 h-5 mr-2"),
        label,
        on_click=lambda: AdminState.set_tab(name),
        class_name=rx.cond(
            AdminState.active_tab == name,
            "flex items-center px-4 py-2 border-b-2 border-indigo-500 text-indigo-600 font-medium",
            "flex items-center px-4 py-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300",
        ),
    )


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            user.id, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            user.username,
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(user.is_admin, "Admin", "User"),
                class_name=rx.cond(
                    user.is_admin,
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            user.total_points,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.select(
                rx.el.option("Pending", value="pending"),
                rx.el.option("Paid", value="paid"),
                rx.el.option("Not Paid", value="not_paid"),
                default_value=user.payment_status,
                on_change=lambda val: AdminState.update_payment_status(user.id, val),
                class_name=rx.match(
                    user.payment_status,
                    (
                        "paid",
                        "block w-32 pl-3 pr-10 py-1 text-xs border-green-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-full bg-green-50 text-green-800",
                    ),
                    (
                        "not_paid",
                        "block w-32 pl-3 pr-10 py-1 text-xs border-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500 sm:text-sm rounded-full bg-red-50 text-red-800",
                    ),
                    "block w-32 pl-3 pr-10 py-1 text-xs border-yellow-300 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm rounded-full bg-yellow-50 text-yellow-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.cond(user.is_admin, "Demote", "Make Admin"),
                    on_click=lambda: AdminState.toggle_admin(user.id),
                    class_name="text-indigo-600 hover:text-indigo-900 mr-4 text-sm font-medium",
                ),
                rx.el.button(
                    "Delete",
                    on_click=lambda: AdminState.delete_user(user.id),
                    class_name="text-red-600 hover:text-red-900 text-sm font-medium",
                ),
                class_name="flex",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def match_row(match: Match) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            match.id, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            f"{match.team1} vs {match.team2}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            rx.moment(match.start_time, format="MMM D, HH:mm"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.span(
                match.status,
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 capitalize",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                match.status == "upcoming",
                "-",
                f"{match.team1_score} - {match.team2_score}",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Edit",
                    on_click=lambda: AdminState.open_match_modal(match.id),
                    class_name="text-indigo-600 hover:text-indigo-900 mr-4 text-sm font-medium",
                ),
                rx.el.button(
                    "Delete",
                    on_click=lambda: AdminState.delete_match(match.id),
                    class_name="text-red-600 hover:text-red-900 text-sm font-medium",
                ),
                class_name="flex",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def payment_row(payment: Payment) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            payment.id, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            AdminState.get_username_map[payment.user_id],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            f"${payment.amount}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
        ),
        rx.el.td(
            rx.moment(payment.date, format="MMM D, YYYY"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.span(
                payment.status,
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 capitalize",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def prediction_row(pred: Prediction) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            AdminState.get_match_map[pred.match_id],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            AdminState.get_username_map[pred.user_id],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"{pred.team1_prediction} - {pred.team2_prediction}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-bold text-indigo-600",
        ),
        rx.el.td(
            rx.cond(
                pred.boost_active,
                rx.el.span(
                    rx.icon("zap", class_name="w-4 h-4 mr-1"),
                    "Yes",
                    class_name="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800",
                ),
                rx.el.span("No", class_name="text-gray-500 text-xs"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            pred.points_earned,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium",
        ),
    )


def match_modal() -> rx.Component:
    return rx.cond(
        AdminState.is_match_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            rx.cond(
                                AdminState.editing_match_id == 0,
                                "Create Match",
                                "Edit Match",
                            ),
                            class_name="text-lg font-medium leading-6 text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=AdminState.close_match_modal,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Team 1",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    name="team1",
                                    default_value=AdminState.match_team1,
                                    required=True,
                                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Team 2",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    name="team2",
                                    default_value=AdminState.match_team2,
                                    required=True,
                                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            class_name="grid grid-cols-6 gap-6 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Start Time",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    name="start_time",
                                    type="text",
                                    default_value=AdminState.match_start_time,
                                    required=True,
                                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Status",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.select(
                                    rx.el.option("Upcoming", value="upcoming"),
                                    rx.el.option("Live", value="live"),
                                    rx.el.option("Finished", value="finished"),
                                    name="status",
                                    default_value=AdminState.match_status,
                                    class_name="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            class_name="grid grid-cols-6 gap-6 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Team 1 Score",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    name="score1",
                                    type="number",
                                    default_value=AdminState.match_score1.to_string(),
                                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Team 2 Score",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    name="score2",
                                    type="number",
                                    default_value=AdminState.match_score2.to_string(),
                                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                ),
                                class_name="col-span-6 sm:col-span-3",
                            ),
                            class_name="grid grid-cols-6 gap-6 mb-4",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                on_click=AdminState.close_match_modal,
                                class_name="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mr-3",
                            ),
                            rx.el.button(
                                "Save",
                                type="submit",
                                class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                            ),
                            class_name="flex justify-end",
                        ),
                        on_submit=AdminState.save_match,
                    ),
                    class_name="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0",
            ),
            class_name="fixed z-10 inset-0 overflow-y-auto bg-gray-500 bg-opacity-75",
        ),
        rx.fragment(),
    )


def payment_modal() -> rx.Component:
    return rx.cond(
        AdminState.is_payment_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Add Payment",
                            class_name="text-lg font-medium leading-6 text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=AdminState.close_payment_modal,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "User",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    AdminState.users,
                                    lambda u: rx.el.option(u.username, value=u.id),
                                ),
                                name="user_id",
                                class_name="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Amount ($)",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                name="amount",
                                type="number",
                                step="0.01",
                                required=True,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Status",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option("Completed", value="completed"),
                                rx.el.option("Pending", value="pending"),
                                rx.el.option("Failed", value="failed"),
                                name="status",
                                class_name="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                on_click=AdminState.close_payment_modal,
                                class_name="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mr-3",
                            ),
                            rx.el.button(
                                "Save",
                                type="submit",
                                class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                            ),
                            class_name="flex justify-end",
                        ),
                        on_submit=AdminState.save_payment,
                    ),
                    class_name="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0",
            ),
            class_name="fixed z-10 inset-0 overflow-y-auto bg-gray-500 bg-opacity-75",
        ),
        rx.fragment(),
    )


def admin_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Admin Dashboard", class_name="text-3xl font-bold text-gray-900"
                    ),
                    rx.el.div(
                        tab_button("users", "Users", "users"),
                        tab_button("matches", "Matches", "calendar"),
                        tab_button("payments", "Payments", "credit-card"),
                        tab_button("predictions", "Predictions", "crosshair"),
                        class_name="flex space-x-4 border-b border-gray-200 mt-6 overflow-x-auto pb-2",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    rx.cond(
                        AdminState.active_tab == "users",
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "User Management",
                                    class_name="text-xl font-semibold mb-4",
                                ),
                                rx.el.div(
                                    rx.el.table(
                                        rx.el.thead(
                                            rx.el.tr(
                                                rx.el.th(
                                                    "ID",
                                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                                rx.el.th(
                                                    "Username",
                                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                                rx.el.th(
                                                    "Role",
                                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                                rx.el.th(
                                                    "Points",
                                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                                rx.el.th(
                                                    "Payment Status",
                                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                                rx.el.th(
                                                    "Actions",
                                                    class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                                ),
                                            ),
                                            class_name="bg-gray-50",
                                        ),
                                        rx.el.tbody(
                                            rx.foreach(AdminState.users, user_row),
                                            class_name="bg-white divide-y divide-gray-200",
                                        ),
                                        class_name="min-w-full divide-y divide-gray-200",
                                    ),
                                    class_name="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                                ),
                            )
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AdminState.active_tab == "matches",
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Match Management",
                                    class_name="text-xl font-semibold",
                                ),
                                rx.el.button(
                                    "Add Match",
                                    on_click=lambda: AdminState.open_match_modal(0),
                                    class_name="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700",
                                ),
                                class_name="flex justify-between items-center mb-4",
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "ID",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Teams",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Time",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Status",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Score",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Actions",
                                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                        ),
                                        class_name="bg-gray-50",
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(AdminState.matches, match_row),
                                        class_name="bg-white divide-y divide-gray-200",
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                            ),
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AdminState.active_tab == "payments",
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Payment History",
                                    class_name="text-xl font-semibold",
                                ),
                                rx.el.button(
                                    "Record Payment",
                                    on_click=AdminState.open_payment_modal,
                                    class_name="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700",
                                ),
                                class_name="flex justify-between items-center mb-4",
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "ID",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "User",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Amount",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Date",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Status",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                        ),
                                        class_name="bg-gray-50",
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(AdminState.payments, payment_row),
                                        class_name="bg-white divide-y divide-gray-200",
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                            ),
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AdminState.active_tab == "predictions",
                        rx.el.div(
                            rx.el.h2(
                                "All Predictions",
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Match",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "User",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Prediction",
                                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                            ),
                                            rx.el.th(
                                                "Boost",
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
                                            AdminState.predictions, prediction_row
                                        ),
                                        class_name="bg-white divide-y divide-gray-200",
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200",
                                ),
                                class_name="overflow-x-auto shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg",
                            ),
                        ),
                        rx.fragment(),
                    ),
                    class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
            ),
            class_name="py-10 bg-gray-50 min-h-screen",
        ),
        match_modal(),
        payment_modal(),
        on_mount=AdminState.on_mount,
        class_name="font-['Inter']",
    )