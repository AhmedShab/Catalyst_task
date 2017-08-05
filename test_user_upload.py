from user_upload import append_quote_to_names
from user_upload import contains_single_quote
from user_upload import remove_invalid_email


def test_surname_contains_quote__append_quote():
    expacted = "A''hmed"
    test = "A'hmed"
    assert append_quote_to_names(test, "'") == expacted

def test_surname_contains_no_quote__return_false():
    expacted = False
    test = "Ahmed"

    assert contains_single_quote(test, "'") == expacted
