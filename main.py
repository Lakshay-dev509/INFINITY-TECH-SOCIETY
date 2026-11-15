
"""INFINITY - AI-Powered Interactive Web Platform.
NiceGUI application entry point.
Run with: python main.py
"""
import os
from nicegui import ui
from app.config import APP_TITLE, APP_PORT
from pages.home import render_home
from pages.contact import contact_page


@ui.page("/")
def home_page():
    render_home()


if __name__ in {"__main__", "__mp_main__"}:
        ui.run(
        title=APP_TITLE,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", APP_PORT)),
        reload=False,
        favicon="∞",
    )
