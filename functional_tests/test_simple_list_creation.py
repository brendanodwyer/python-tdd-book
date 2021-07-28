from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # Add first item to the list
        self.add_list_item("Buy peacock feathers")

        # Add second item to the list
        inputbox = self.get_item_input_box()
        self.add_list_item("Use peacock feathers to make a fly")

        # She see's that she has both of her items in her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith's Browser Session
        self.browser.get(self.live_server_url)
        self.add_list_item("Buy peacock feathers")
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Close Browser Session for Edith
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franscis's Browser Session
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list and add's a new item to his list
        self.add_list_item("Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Double check for trace's of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buying peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
