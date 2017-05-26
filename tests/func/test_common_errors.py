import pytest  # noqa
from parglare import Grammar, Parser
from parglare.exceptions import NoActionsForStartRule, GrammarError


def test_no_actions_root_rule():
    """
    If root rule have no recursion termination alternative as for example:

    Elements = Elements Element;

    instead of:
    Elements = Elements Element | Element;

    Action set for the first state will have no elements so parsing can't even
    begin as no SHIFT actions can occur.
    """

    grammar = """
    Elements = Elements Element;
    Element = "a" | "b";
    """

    g = Grammar.from_string(grammar)

    with pytest.raises(NoActionsForStartRule):
        Parser(g)


def test_terminals_with_different_names():
    """Test that all terminals with same string match have the same name.
    """

    # In this grammar we have 'd' terminal in S production and B terminal with
    # the same 'd' recognizer.
    grammar = """
    S = 'a' A 'd' | 'b' A B;
    A = 'c' A | 'c';
    B = 'd';
    """

    with pytest.raises(GrammarError) as e:
        Grammar.from_string(grammar)

    assert 'B' in str(e)
    assert 'd' in str(e)
    assert 'already exists' in str(e)
