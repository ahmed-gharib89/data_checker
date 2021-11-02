import glob
import filecmp
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender


class EmailOnChange(object):
    def __init__(self, destination, mailer):
        self.destination = destination
        self.mailer = mailer

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("EMAIL_ON_CHANGE_ENABLED"):
            raise NotConfigured
        destination = crawler.settings.get("EMAIL_ON_CHANGE_DESTINATION")
        if not destination:
            raise NotConfigured("EMAIL_ON_CHANGE_DESTINATION must be provided")
        mailer = MailSender.from_settings(crawler.settings)
        # Create an instance of our extension
        extension = cls(destination, mailer)
        crawler.signals.connect(extension.engine_stopped, signal=signals.engine_stopped)
        return extension

    def engine_stopped(self):
        runs = sorted(
            glob.glob("/tmp/[0-9]*-[0-9]*-[0-9]*T[0-9]*-[0-9]*-[0-9]*.json"),
            reverse=True,
        )
        if len(runs) < 2:
            # We can't compare if there's only 1 run
            return
        current_file, previous_file = runs[0:2]
        print(current_file, previous_file)
        if not filecmp.cmp(current_file, previous_file):
            print("\n\nTHE FILES ARE DIFFERENT\n\n")
            with open(current_file) as f:
                self.mailer.send(
                    to=[self.destination],
                    subject="Datasets Changed",
                    body="Changes in datasets detected, see attachment for current datasets",
                    attachs=[(current_file.split("/")[-1], "application/json", f)],
                )
        else:
            print("\n\nNO CHANGE\n\n")
