from pysm import State, StateMachine, Event

foo = True


class CanonicalHsm(StateMachine):
    """ The classic example from Miro Samek's book """

    def __init__(self):
        super().__init__('top')
        s0 = StateMachine('s0')
        s1 = StateMachine('s1')
        s2 = StateMachine('s2')
        s11 = State('s11')
        s21 = StateMachine('s21')
        s211 = State('s211')
        s212 = State('s212')  # not part of Samek's original example

        self.add_state(s0, initial=True)
        s0.add_state(s1, initial=True)
        s0.add_state(s2)
        s1.add_state(s11, initial=True)
        s2.add_state(s21, initial=True)
        s21.add_state(s211, initial=True)
        s21.add_state(s212)

        # Internal transitions
        self.add_transition(s0, None, events='i', action=self.action_i)
        s0.add_transition(s1, None, events='j', action=self.action_j)
        s0.add_transition(s2, None, events='k', action=self.action_k)
        s1.add_transition(s11, None, events='h', condition=self.is_foo, action=self.unset_foo)
        s1.add_transition(s11, None, events='n', action=self.action_n)
        s21.add_transition(s211, None, events='m', action=self.action_m)
        s2.add_transition(s21, None, events='l', condition=self.is_foo, action=self.action_l)

        # External transition
        #self.add_transition(self, s211, events='e')
        self.add_transition(s0, s211, events='e')
        self.add_transition(s0, s212, events=['e2'])
        s0.add_transition(s1, s0, events='d')
        s0.add_transition(s1, s11, events='b')
        s0.add_transition(s1, s1, events='a')
        s0.add_transition(s1, s211, events='f')
        s0.add_transition(s1, s2, events='c')
        s0.add_transition(s2, s11, events='f')
        s0.add_transition(s2, s1, events='c')
        s1.add_transition(s11, s211, events='g')
        s21.add_transition(s211, s0, events='g')
        s21.add_transition(s211, s21, events='d')
        s2.add_transition(s21, s211, events='b')
        s2.add_transition(s21, s21, events='h', condition=self.is_not_foo, action=self.set_foo)

        # Attach enter/exit handlers
        states = [self, s0, s1, s11, s2, s21, s211, s212]
        for state in states:
            state.handlers = {'enter': self.on_enter, 'exit': self.on_exit}

        self.action_sequence = []
        self.print_to_console = True

        self.initialize()

    def log(self, msg):
        self.action_sequence.append(msg)
        if self.print_to_console:
            print(msg)

    def reset_action_sequence(self):
        self.action_sequence = []

    def on_enter(self, state, event):
        self.log(f'enter {state.name}')

    def on_exit(self, state, event):
        self.log(f'exit {state.name}')

    def set_foo(self, state, event):
        global foo
        self.log('set foo')
        foo = True

    def unset_foo(self, state, event):
        global foo
        self.log('unset foo')
        foo = False

    def action_i(self, state, event):
        self.log('action_i')

    def action_j(self, state, event):
        self.log('action_j')

    def action_k(self, state, event):
        self.log('action_k')

    def action_l(self, state, event):
        self.log('action_l')

    def action_m(self, state, event):
        self.log('action_m')

    def action_n(self, state, event):
        self.log('action_n')

    def is_foo(self, state, event):
        return foo is True

    def is_not_foo(self, state, event):
        return foo is False


def basic_test():
    hsm = CanonicalHsm()
    assert hsm.leaf_state.name == 's11'
    hsm.dispatch(Event('a'))
    assert hsm.leaf_state.name == 's11'
    # This transition toggles state between s11 and s211
    hsm.dispatch(Event('c'))
    assert hsm.leaf_state.name == 's211'
    hsm.dispatch(Event('b'))
    assert hsm.leaf_state.name == 's211'
    hsm.dispatch(Event('i'))
    assert hsm.leaf_state.name == 's211'
    hsm.dispatch(Event('c'))
    assert hsm.leaf_state.name == 's11'
    assert foo is True
    hsm.dispatch(Event('h'))
    assert foo is False
    assert hsm.leaf_state.name == 's11'
    # Do nothing if foo is False
    hsm.dispatch(Event('h'))
    assert hsm.leaf_state.name == 's11'
    # This transition toggles state between s11 and s211
    hsm.dispatch(Event('c'))
    assert hsm.leaf_state.name == 's211'
    assert foo is False
    hsm.dispatch(Event('h'))
    assert foo is True
    assert hsm.leaf_state.name == 's211'
    hsm.dispatch(Event('h'))
    assert hsm.leaf_state.name == 's211'


if __name__ == '__main__':
    basic_test()
