import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = "Your login link from Superlists"


class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(SUBJECT, email.subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ["EMAIL_RECEIVER_PASSWORD"])
            while (time.time() - start) < 60:
                # get 10 new messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("Getting message", i)
                    _, lines, _ = inbox.retr(i)
                    lines = [line.decode("utf-8") for line in lines]
                    print(lines)
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body

                print("Message not found, sleeping...")
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        if self.staging_server:
            test_email = "tddwithpythonbook@gmail.com"
        else:
            test_email = "edith@example.com"
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(
            lambda: self.assertIn(
                "Check your email", self.browser.find_element_by_tag_name("body").text
            )
        )

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # now she logs outx
        self.browser.find_element_by_link_text("Log out").click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)
