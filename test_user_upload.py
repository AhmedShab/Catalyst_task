import user_upload


def test_surname_contains_quote__append_quote():
    expacted = "A''hmed"
    test = "A'hmed"
    assert user_upload.append_quote_to_names(test, "'") == expacted

def test_surname_contains_no_quote__return_false():
    expacted = False
    test = "Ahmed"

    assert user_upload.contains_single_quote(test, "'") == expacted

def test_invalid_email__return_true():
    expacted = True
    test = "ahmed&&&@gmail.com"

    assert user_upload.is_invalid_email(test) == expacted

def test_valid_email__return_false():
    expacted = False
    test = "ahmed@gmail.com"

    assert user_upload.is_invalid_email(test) == expacted

def test_remove_invalid_email__should_remove_email():
    expacted = None
    test = {"email": "ahmed&&&@gmail.com"}

    try:
        test = user_upload.remove_invalid_email(test)

    except KeyError as e:
        print "Eamil should be removed, thus, key does not exists"
        test == expacted


def test_remove_invalid_email__should_not_remove_email():
    expacted = "ahmed@gmail.com"
    test = {"email": "ahmed@gmail.com"}

    assert user_upload.remove_invalid_email(test) == expacted

def test_fix_fullname_format__should_return_fixed_text():
    expacted = {"name": "Ahmed", "surname": "Shaaban"}
    test = {"name": "ahmed?", "surname": "shaaban***?"}

    user_upload.fix_fullname_format(test)

    assert test == expacted

def test_clean_whitespaces__should_remove_whitespaces():
    expacted = {"name": "ahmed", "surname": "shaaban", "email": "ahmed@gmail.com"}
    test = {"name": "ahmed   ", "surname": "   shaaban", "email": "      ahmed@gmail.com   "}

    user_upload.remove_whitespaces(test)

    assert test == expacted


def test_set_email_lower_case__return_lower_case_email():
    expacted = "ahmed@gmail.com"
    test = {"email": "AHMED@gmaIL.com"}

    assert user_upload.set_email_lower_case(test) == expacted
