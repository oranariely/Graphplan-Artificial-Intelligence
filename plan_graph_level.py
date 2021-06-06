from action_layer import ActionLayer
from util import Pair
from proposition import Proposition
from proposition_layer import PropositionLayer


class PlanGraphLevel(object):
    """
    A class for representing a level in the plan graph.
    For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
    """
    independent_actions = set()  # updated to the independent_actions of the problem (graph_plan.py line 32)
    actions = []  # updated to the actions of the problem (graph_plan.py line 33 and planning_problem.py line 36)
    props = []  # updated to the propositions of the problem (graph_plan.py line 34 and planning_problem.py line 36)

    @staticmethod
    def set_independent_actions(independent_actions):
        PlanGraphLevel.independent_actions = independent_actions

    @staticmethod
    def set_actions(actions):
        PlanGraphLevel.actions = actions

    @staticmethod
    def set_props(props):
        PlanGraphLevel.props = props

    def __init__(self):
        """
        Constructor
        """
        self.action_layer = ActionLayer()  # see action_layer.py
        self.proposition_layer = PropositionLayer()  # see proposition_layer.py

    def get_proposition_layer(self):  # returns the proposition layer
        return self.proposition_layer

    def set_proposition_layer(self, prop_layer):  # sets the proposition layer
        self.proposition_layer = prop_layer

    def get_action_layer(self):  # returns the action layer
        return self.action_layer

    def set_action_layer(self, action_layer):  # sets the action layer
        self.action_layer = action_layer

    def update_action_layer(self, previous_proposition_layer):
        """
        Updates the action layer given the previous proposition layer (see proposition_layer.py)
        """
        all_actions = PlanGraphLevel.actions
        # next_action_layer = ActionLayer()
        for action in all_actions:
            if previous_proposition_layer.all_preconds_in_layer(action):
                self.action_layer.add_action(action)

    def update_mutex_actions(self, previous_layer_mutex_proposition):
        """
        Updates the mutex set in self.action_layer,
        given the mutex proposition from the previous layer.
        """
        current_layer_actions = list(self.action_layer.get_actions())

        for i in range(len(current_layer_actions)):
            a1 = current_layer_actions[i]
            for j in range(i + 1, len(current_layer_actions)):
                a2 = current_layer_actions[j]
                if mutex_actions(a1, a2, previous_layer_mutex_proposition):
                    self.action_layer.add_mutex_actions(a1, a2)

    def update_proposition_layer(self):
        """
        Updates the propositions in the current proposition layer,
        given the current action layer.
        """
        current_layer_actions = self.action_layer.get_actions()
        propositions_to_add = dict()
        for action in current_layer_actions:
            added_propositions = action.get_add()
            for proposition in added_propositions:
                if proposition not in propositions_to_add:
                    propositions_to_add[proposition] = Proposition(proposition.get_name())
                propositions_to_add[proposition].add_producer(action)
        for prop in propositions_to_add.keys():
            self.proposition_layer.add_proposition(propositions_to_add[prop])

    def update_mutex_proposition(self):
        """
        updates the mutex propositions in the current proposition layer
        """
        current_layer_propositions = list(self.proposition_layer.get_propositions())
        current_layer_mutex_actions = self.action_layer.get_mutex_actions()
        for i in range(len(current_layer_propositions)):
            for j in range(i + 1, len(current_layer_propositions)):
                prop1 = current_layer_propositions[i]
                prop2 = current_layer_propositions[j]
                if mutex_propositions(prop1, prop2, current_layer_mutex_actions):
                    self.proposition_layer.add_mutex_prop(prop1, prop2)

    def expand(self, previous_layer):
        """
        given the propositions and the list of mutex propositions from the previous layer,
        set the actions in the action layer.
        Then, set the mutex action in the action layer.
        Finally, given all the actions in the current layer,
        set the propositions and their mutex relations in the proposition layer.
        """
        previous_proposition_layer = previous_layer.get_proposition_layer()
        previous_layer_mutex_proposition = previous_proposition_layer.get_mutex_props()

        self.update_action_layer(previous_proposition_layer)
        self.update_mutex_actions(previous_layer_mutex_proposition)
        self.update_proposition_layer()
        self.update_mutex_proposition()

    def expand_without_mutex(self, previous_layer):
        """
        Questions 11 and 12
        You don't have to use this function
        """
        previous_proposition_layer = previous_layer.get_proposition_layer()
        self.update_action_layer(previous_proposition_layer)
        self.update_proposition_layer()


def mutex_actions(a1, a2, mutex_props):
    """
    This function returns true if a1 and a2 are mutex actions.
    """
    if Pair(a1, a2) not in PlanGraphLevel.independent_actions:
        return True
    return have_competing_needs(a1, a2, mutex_props)


def have_competing_needs(a1, a2, mutex_props):
    """
    Complete code for deciding whether actions a1 and a2 have competing needs,
    given the mutex proposition from previous level (list of pairs of propositions).
    """
    for pre1 in a1.get_pre():
        for pre2 in a2.get_pre():
            if Pair(pre1, pre2) in mutex_props:  # check every pair in precondition if they mutex
                return True
    return False


def mutex_propositions(prop1, prop2, mutex_actions_list):
    """
    complete code for deciding whether two propositions are mutex,
    given the mutex action from the current level (set of pairs of actions).
    """
    for a1 in prop1.get_producers():
        for a2 in prop2.get_producers():
            if Pair(a1, a2) not in mutex_actions_list:
                return False
    return True
