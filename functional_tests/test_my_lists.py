from django.conf import settings

from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(name=settings.SESSION_COOKIE_NAME, value=session_key, path="/")
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in_user
        self.create_pre_authenticated_session("edith@example.com")

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticlate Splines")
        self.add_list_item("Immanetize eschaton")
        first_list_url = self.browser.current_url

        # She notices a "My Lists" link, for the first time
        self.browser.find_element_by_link_text("My Lists").click()

        # She sees that her list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Reticlate Splines")
        )
        self.browser.find_element_by_link_text("Reticlate Splines")
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item("Click Cows")
        second_list_url = self.browser.current_url

        # under "my lists", her new list appears
        self.browser.find_element_by_link_text("My Lists").click()
        self.wait_for(lambda: self.browser.find_element_by_link_text("Click Cows"))
        self.browser.find_element_by_link_text("Click Cows")
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The "My Lists" option disappears
        self.browser.find_element_by_link_text("Log out").click()

    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")
