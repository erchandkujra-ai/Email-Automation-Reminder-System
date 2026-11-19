
from src.renderer import render_email


def test_email_personalization():

    subject, html = render_email(
        "Rahul",
        "Project Meeting"
    )

    assert subject == "Reminder: Project Meeting"
    assert "Rahul" in html
    assert "Project Meeting" in html
