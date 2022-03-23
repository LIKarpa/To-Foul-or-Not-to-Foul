
# Returns name of opponent
def otherTeam(team):
    return 'A' if team == 'B' else 'B'

# Gets index of node with given state
def getIndex(tree_list, state):
    for node in tree_list:
        if str(state) in node:
            return tree_list.index(node)

# Generates the list representation of the game tree given
# an event diagram, an initial state, and an end condition
def toTree(event_diagram, initial_state, end_condition):
    toTreeHelper(event_diagram, initial_state, end_condition, [], [], "1", 0, 0)


# Does the recursive work to process the event diagram and compute successive states.
# 'event_diagram' is the event diagram. 'current_state' is the current state being processed.
# 'end_condition' is the end condition. 'visited' marks which states have already been processed.
# 'tree' stores the list representation of the game. 'tree' stores states with information
# about their index in the list, the states level in the tree, and the states probability
# of occurring given the parent occurred. 'prob' is the probability of the current state
# occurring given the parent state occurred or is 'c' denoting the event of the current state
# is a choice. 'level' is the level of the tree that the current state is at.
def toTreeHelper(event_diagram, current_state, end_condition, visited, tree, prob, level, parent):
    index = len(tree)
    # Gets the current_state's values
    score_dif = current_state[0]
    team = current_state[1]
    fouls = current_state[2]
    event = current_state[3]

    # Checks if we have already processed the current state previously
    if current_state in visited:
        # If we have processed the current state previously,
        # we reference the index at which it was already processed
        # to condense the size of the tree. The repeat reference
        # is added to the tree and is printed for visualization.
        tree.append(str(index) + "-" + str(parent)
                    + "  " + prob + ", REPEAT " + str(getIndex(tree, current_state)))
        print(tree[-1])
    else:
        # If we have not processed the current state previously,
        # we mark the state as having been processed and add it
        # to the tree, with the corresponding probability and level
        # information.
        visited.append(current_state)
        tree.append(str(index) + "-" + str(parent)
                    + " " + prob + ", " + str(current_state))
        print(tree[-1])
        # If the current state is not in the end condition, we
        # construct the child (new) state and recurse on that new state.
        if not(current_state in end_condition):
            for child in event_diagram[event]:
                new_event = child[0]
                new_prob = child[1]
                point_change = child[2]
                flip_possession = child[3]

                new_state = (score_dif + point_change if team == 'A' else score_dif - point_change,
                             team if flip_possession == 0 else otherTeam(team),
                             fouls + 1 if new_event == "Foul" else fouls,
                             new_event)

                toTreeHelper(event_diagram, new_state, end_condition, visited, tree, new_prob, level + 1, index)







graph = dict()
# Weighted edges are represented by a tuple extension of the event name
graph["Start"] = [("No Turnover", "1-tB", 0, 0), ("Turnover", "tB", 0, 1)]
graph["No Turnover"] = [("2pter", "c", 0, 0), ("3pter", "c", 0, 0)]
graph["Turnover"] = [("Start", "1", 0, 0)]
graph["2pter"] = [("Missed Shot", "1-fgi2", 0, 1), ("Made Shot", "fgi2", 2, 1)]
graph["3pter"] = [("Missed Shot", "1-fgi3", 0, 1), ("Made Shot", "fgi3", 3, 1)]
graph["Missed Shot"] = []
graph["Made Shot"] = []



toTree(graph, (0, 'B', 0, "Start"), [])


# Function to print a BFS of graph
def toBFSTree(event_diagram, initial_state, end_states):
    # Stores list representation of tree
    tree = []
    # Mark all states unvisited
    visited = []
    # Creates queue of states with initial state included
    queue = [initial_state]
    # Mark the initial state as visited
    visited.append(initial_state)

    # Print and add root to tree
    tree.append("1, " + str(initial_state))
    print("0  1, " + str(initial_state))

    while queue:
        # Dequeue a vertex from queue
        current_state = queue.pop(0)

        # Gets the current_state's values
        score_dif = current_state[0]
        team = current_state[1]
        event = current_state[2]

        # -- > if current_state does not satisfy end condition

        # Get all adjacent vertices of the
        # dequeued vertex. If an adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for child in event_diagram[event]:
            new_state = (score_dif + child[2] if team == 'A' else score_dif + child[2],
                         team if child[3] == 0 else otherTeam(team),
                         child[0])

            if new_state in visited:
                tree.append("REPEAT " + str(getIndex(tree, new_state)))
                print("" + str(len(tree)-1) + "  REPEAT " + str(getIndex(tree, new_state)))
            else:
                visited.append(new_state)
                tree.append("" + child[1] + ", " + str(new_state))
                print("" + str(len(tree)-1) + "  " + tree[len(tree)-1])
                queue.append(new_state)