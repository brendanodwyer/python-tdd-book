from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValitationTest(FunctionalTest):
    
    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box

        # The browser intercepts the request, and does not load the
        # list page

        # She starts typing some text for the new item and the error disappears

        # And she can submit it successfully

        # Perversely, she now decides to submit a second blank list item

        # Again, the browser will not comply

        # And she can correct it by filling some text in
        self.fail("Write Me!")
