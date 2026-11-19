
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from src.config import BASE_DIR

environment = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=True,
    undefined=StrictUndefined
)


def render_email(name, title):

    template = environment.get_template("reminder.html")

    html = template.render(
        name=name,
        title=title
    )

    subject = f"Reminder: {title}"

    return subject, html
