"""Weekly subscriber digest (business logic hidden behind run())."""
import csv
import io
from datetime import date


class WeeklyDigest:
    def __init__(self, repository, mailer, recipient: str):
        self.__repo = repository
        self.__mailer = mailer
        self.__to = recipient

    def __build_csv(self, rows) -> bytes:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["email", "subscribed_at"])
        writer.writerows(rows)
        return buf.getvalue().encode("utf-8")

    def run(self) -> int:
        if not self.__to:
            raise RuntimeError("DIGEST_RECIPIENT is not configured")
        rows = self.__repo.all()
        self.__mailer.send_attachment(
            self.__to,
            f"Weekly subscriber list: {date.today():%Y-%m-%d}",
            f"{len(rows)} subscriber(s) attached.",
            "subscribers.csv",
            self.__build_csv(rows),
        )
        return len(rows)
