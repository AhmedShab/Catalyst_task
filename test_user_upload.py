import user_upload
import unittest
from mock import MagicMock

class TestUserUpload(unittest.TestCase):

    def test_surname_contains_quote__append_quote(self):
        expacted = "A''hmed"
        test = "A'hmed"
        self.assertTrue(user_upload.append_quote_to_names(test, "'"), expacted)

    def test_surname_contains_no_quote__return_false(self):
        expacted = False
        test = "Ahmed"

        self.assertFalse(user_upload.contains_single_quote(test, "'"), expacted)

    def test_invalid_email__return_true(self):
        expacted = True
        test = "ahmed&&&@gmail.com"

        self.assertTrue(user_upload.is_invalid_email(test), expacted)

    def test_valid_email__return_false(self):
        expacted = False
        test = "ahmed@gmail.com"

        self.assertFalse(user_upload.is_invalid_email(test), expacted)

    def test_remove_invalid_email__should_remove_email(self):
        expacted = None
        test = {"email": "ahmed&&&@gmail.com"}

        try:
            user_upload.remove_invalid_email(test)

        except KeyError as e:
            print "Eamil should be removed, thus, throw an error since the key does not exists"


    def test_remove_invalid_email__should_not_remove_email(self):
        expacted = "ahmed@gmail.com"
        test = {"email": "ahmed@gmail.com"}

        self.assertTrue(user_upload.remove_invalid_email(test), expacted)

    def test_fix_fullname_format__return_fixed_text(self):
        expacted = {"name": "Ahmed", "surname": "Shaaban"}
        test = {"name": "ahmed?", "surname": "shaaban***?"}

        user_upload.fix_fullname_format(test)

        self.assertTrue(test, expacted)

    def test_clean_whitespaces__should_remove_whitespaces(self):
        expacted = {"name": "ahmed", "surname": "shaaban", "email": "ahmed@gmail.com"}
        test = {"name": "ahmed   ", "surname": "   shaaban", "email": "      ahmed@gmail.com   "}

        user_upload.remove_whitespaces(test)

        self.assertTrue(test, expacted)


    def test_set_email_lower_case__return_lower_case_email(self):
        expacted = "ahmed@gmail.com"
        test = {"email": "AHMED@gmaIL.com"}

        self.assertTrue(user_upload.set_email_lower_case(test), expacted)    

if __name__ == "__main__":
    unittest.main()
