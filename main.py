import networkx as nx

def get_graph(n_nodes, init, initial_data, capacities, t_max):

    G = nx.DiGraph()

    G.add_node('s') # sursa

    for n in range(n_nodes):
        for t in range(t_max+1):
            G.add_node('{}_{}'.format(n, t))

            if t != 0:
                if n == 0:
                    G.add_edge('{}_{}'.format(n, t-1),
                               '{}_{}'.format(n, t))
                else:
                    G.add_edge('{}_{}'.format(n, t-1),
                               '{}_{}'.format(n, t),
                               capacity=capacities)

        if n != 0:
            G.add_edge('s', '{}_0'.format(n), capacity=initial_data)

    for node in init:

        for t in range(node[2], t_max+1, node[3]):
            src = '{}_{}'.format(node[0], t)
            dest = '{}_{}'.format(node[1], t)

            G.add_edge(src, dest, capacity=capacities)
            if node[1] != 0:
                G.add_edge(dest, src, capacity=capacities)

    return G

def add_dyn_nodes(G, n_nodes, t_max, cycle_lengths, initial_data):

    for i in range(1, n_nodes):

        #G.add_node('{}_ENDOFLINE'.format(i))
        #G.add_edge('{}_{}'.format(i, t_max), '{}_ENDOFLINE'.format(i))
        #G.add_edge('{}_ENDOFLINE'.format(i), '0_{}'.format(t_max))


        G.add_node('dummy_{}_0'.format(i))
        G.add_edge('s', 'dummy_{}_0'.format(i))  

        for t in range(1, t_max+1):
            G.add_node('dummy_{}_{}'.format(i, t))
            G.add_edge('dummy_{}_{}'.format(i, t-1), 'dummy_{}_{}'.format(i, t))  

            if t % cycle_lengths[i] == 0:
                G.add_edge('dummy_{}_{}'.format(i, t), '{}_{}'.format(i, t), capacity=initial_data)
        

def get_flow(G, t_max):

    return nx.maximum_flow(G, 's', '0_{}'.format(t_max))

def get_min_needed_time(n_nodes, init, initial_data, capacities):

    needed_flow = (n_nodes - 1) * initial_data
    current_flow = 0
    detailed_flow = None

    t_current = 1
    while current_flow != needed_flow:

        G = get_graph(n_nodes, init, initial_data, capacities, t_current)
        detailed_flow = get_flow(G, t_current)
        current_flow = detailed_flow[0]

        t_current += 1

    t_current -= 1
    return t_current, detailed_flow

def dynamic_data(n_nodes, init, initial_data, capacities, cycle_lengths, t_max):

    G = get_graph(n_nodes, init, initial_data, capacities, t_max)
    add_dyn_nodes(G, n_nodes, t_max, cycle_lengths, initial_data)

    detailed_flow = get_flow(G, t_max)
        
    return detailed_flow
    
        
n_nodes = 3
#init = [(1, 3, 1, 4), # arc_x, arc_y, first meeting time, periodicity of meetings
#        (3, 2, 2, 6),
#        (2, 1, 3, 6),
#        (2, 0, 0, 6)]
init = [(1, 2, 3, 6),
        (1, 0, 0, 3)]
cycle_lengths = {1: 3, 2: 2}

while True:
    
    initial_data = int(input('Give initial data: '))
    capacities = int(input('Give capacity: '))
    t_max = int(input('Give t_max: '))

    with_dyn = dynamic_data(n_nodes, init, initial_data, capacities, cycle_lengths, t_max)
    print(with_dyn)
    print()
    print()

#min_time = get_min_needed_time(n_nodes, init, initial_data, capacities)
#print('Timp minim:', min_time)
