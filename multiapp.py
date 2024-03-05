"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

from streamlit_option_menu import option_menu

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title(import streamlit as st
from langchain_helper import Reply
from streamlit_option_menu import option_menu"Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # app = st.sidebar.radio(
        # app = st.selectbox(
        #     'Navigation',
        #     self.apps,
        #     format_func=lambda app: app['title'])
        with st.sidebar:
            selected_app = option_menu(
                menu_title="Navigation",
                options=[app["title"] for app in self.apps],  # Extract titles from app dictionaries
                icons=["house", "database"] if len(self.apps) >= 2 else None,  # Add icons conditionally
                menu_icon="cast",
                default_index=0  # Set default selection to first app
            )

            # Find the selected app dictionary based on title
            selected_app_dict = next(app for app in self.apps if app["title"] == selected_app)

            # Run the selected app's function
        selected_app_dict["function"]()

            # app['function']()
