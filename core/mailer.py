"""Flask-Mail wrapper: the only place that builds or sends messages."""
from flask_mail import Mail, Message


class Mailer:
    def __init__(self, app=None):
        self.__mail = Mail()
        self.__artist = ""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.__mail.init_app(app)
        self.__artist = app.config["ARTIST_NAME"]

    def send_welcome(self, email: str) -> None:
        msg = Message(f"Welcome to the studio of {self.__artist}", recipients=[email])
        msg.body = (f"Thank you for subscribing.\n\nYou will hear about new "
                    f"paintings, exhibitions and studio news.\n\n- {self.__artist}")
        self.__mail.send(msg)

    def send_attachment(self, to: str, subject: str, body: str,
                        filename: str, data: bytes) -> None:
        msg = Message(subject, recipients=[to], body=body)
        msg.attach(filename, "text/csv", data)
        self.__mail.send(msg)
