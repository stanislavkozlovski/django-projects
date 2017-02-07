from functional_tests.base import FunctionalTest


class LayoutAndStylingTests(FunctionalTest):
    def test_layout_and_styling(self):
        # The Aesthetic Goat visits our page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        # It notices that the input box is nicely centered
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=6
        )

        # It starts a new list and sees that the input box is nicely centered there too
        input_box.send_keys('IsItCentered?\n')
        other_input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            other_input_box.location['x'] + other_input_box.size['width'] / 2,
            512,
            delta=6
        )

    def test_error_messages_are_cleared_on_input(self):
        # The Artistic Goat visits our page
        self.browser.get(self.server_url)
        self.js_remove_input_box_required_attr()
        self.get_item_input_box().send_keys('\n')
        # it gets an error message
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        # it starts typing and the error message disappears
        self.get_item_input_box().send_keys('a')
        # it is pleased that the error message is no more
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

