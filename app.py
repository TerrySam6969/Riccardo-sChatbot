from multiapp import MultiApp
from apps import database, home, review

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("Database", database.app)
app.add_app("Review", review.app)

app.run()