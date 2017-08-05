from user_upload import append_quote_to_names
from user_upload import contains_single_quote
from user_upload import remove_invalid_email
from user_upload import is_invalid_email


def test_surname_contains_quote__append_quote():
    expacted = "A''hmed"
    test = "A'hmed"
    assert append_quote_to_names(test, "'") == expacted

def test_surname_contains_no_quote__return_false():
    expacted = False
    test = "Ahmed"

    assert contains_single_quote(test, "'") == expacted

def test_invalid_email__return_true():
    expacted = True
    test = "ahmed&&&@gmail.com"

    assert is_invalid_email(test) == expacted

def test_valid_email__return_false():
    expacted = False
    test = "ahmed@gmail.com"

    assert is_invalid_email(test) == expacted

def test_remove_invalid_email__should_remove_email():
    expacted = None
    test = {"email": "ahmed&&&@gmail.com"}

    try:
        test = remove_invalid_email(test)

    except KeyError as e:
        print "Eamil should be removed, thus, key does not exists"
        test == expacted


def test_remove_invalid_email__should_not_remove_email():
    expacted = "ahmed@gmail.com"
    test = {"email": "ahmed@gmail.com"}

    assert remove_invalid_email(test) == expacted
