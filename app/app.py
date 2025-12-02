import reflex as rx
from app.pages.index import index
from app.pages.auth import login_page, register_page
from app.pages.matches import matches_page
from app.pages.my_predictions import my_predictions_page
from app.pages.leaderboard import leaderboard_page
from app.pages.admin import admin_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
    ],
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(matches_page, route="/matches")
app.add_page(my_predictions_page, route="/my-predictions")
app.add_page(leaderboard_page, route="/leaderboard")
app.add_page(admin_page, route="/admin")