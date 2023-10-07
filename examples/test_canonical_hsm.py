import pytest
import canonical_hsm
import pysm


@pytest.fixture
def hsm():
    hsm = canonical_hsm.CanonicalHsm()
    hsm.print_to_console = False
    return hsm


def test_initial_state(hsm):
    assert hsm.leaf_state.name == 's11'


@pytest.mark.skip  # we know this currently fails
def test_initial_entry_actions(hsm):
    # my understanding of the UML spec is that entry actions should be executed for initial states, even at start
    assert hsm.action_sequence == ['enter s0', 'enter s1', 'enter s11']


def test_entry_exit_sequence(hsm):
    assert hsm.leaf_state.name == 's11'

    hsm.reset_action_sequence()
    hsm.dispatch(pysm.Event('e'))
    assert hsm.leaf_state.name == 's211'
    assert hsm.action_sequence == ['exit s11', 'exit s1', 'enter s2', 'enter s21', 'enter s211']

    hsm.reset_action_sequence()
    hsm.dispatch(pysm.Event('e2'))
    assert hsm.leaf_state.name == 's212'
    assert hsm.action_sequence == ['exit s211', 'enter s212']