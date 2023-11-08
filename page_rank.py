# creators: Raivis Lickrastins, Julia Bijak and Renata Sapeta
import networkx as nx
import collections
import random


def load_file(filename):
    with open(filename, 'rb') as infile:
        return nx.read_adjlist(infile, create_using=nx.DiGraph())


def branching_function(G):
    for_dict = [edge[0] for edge in G.edges()]
    branching_dict = collections.Counter(for_dict)
    return branching_dict


def dangling_nodes_function(G):
    dangling_nodes = []
    for node in G.nodes():
        if [neighbor for neighbor in G.neighbors(node)] == []:
            dangling_nodes.append(node)
    return dangling_nodes


def surfer(G, n):
    """
    Function performing a random walk on a nx.DiGraph object G
    with n iterations.

    Parameters:
        n - int(number of iterations to surf)
        G - nx.DiGraph

    Return:
        List of 10 most important pages.
    """
    dangling_nodes = dangling_nodes_function(G)
    m = 0.15
    visited_nodes = []
    nodes_list = [node for node in G.nodes()]

    random_node = random.choice(nodes_list)

    for _ in range(n):
        visited_nodes.append(random_node)
        probability = random.random()
        if random_node in dangling_nodes or probability < m:
            random_node = random.choice(nodes_list)
        else:
            neighbors = [neighbor for neighbor in G.neighbors(random_node)]
            random_node = random.choice(neighbors)

    visited_nodes_dict = collections.Counter(visited_nodes)
    return [i[0] for i in visited_nodes_dict.most_common(10)]


def page_rank(G, k):
    """
    Function computing the pageRank vector using linear algebra.

    Parameters:
        k - int (number of iterations to run to approximate)
        G - nx.DiGraph

    Return:
        List of 10 most important pages and their scores.
    """
    m = 0.15
    G_size = len(G)
    G_reversed = nx.reverse(G)
    branching = branching_function(G)
    dangling_nodes = dangling_nodes_function(G)

    x_0 = {}
    for node in G.nodes():
        x_0[node] = 1 / G_size  # starting vector has the same entries everywhere

    x_next = x_0
    S = sum((1 / G_size) * x_next[node] for node in
            x_next.keys())  # as S has all entries the same it's ok to sum only 1st row
    for _ in range(k):
        D = sum(x_next[node] / G_size for node in
                dangling_nodes)  # all rows are the same so it's sufficient to sum up just 1st
        for node in range(G_size):
            backlinks = [backlink for backlink in G_reversed.neighbors(str(node))]
            A = sum((1 / (branching[backlink])) * x_next[backlink] for backlink in
                    backlinks)  # sum for row corresponding to given node
            x_next[str(node)] = (1 - m) * A + (1 - m) * D + m * S
    node_list_ordered = sorted(x_next.items(), key=lambda x: x[1], reverse=True)

    return node_list_ordered[:10]


def approximation(G, decimal_points):
    """
    Function computing approximation of number of iterations of the PageRank algorithm
    needed for the top 10 to stabilise.

    Parameters:
        G - nx.DiGraph
        decimal_points - to how many decimal point we are comparing the output of PageRank function

    Return:
        Number of how many iterations are required for PageRank function to stabilise the results.
    """
    perfect_output = [x[0] for x in page_rank(G, 10**2)]
    for i in range(10**2):
        to_compare = [x[0] for x in page_rank(G, i)]
        if to_compare == perfect_output:
            break
    return i


def main():
    G = load_file("PageRankExampleData/p2p-Gnutella08-mod.txt")

    print(surfer(G, n=10 ** 6))
    print(page_rank(G, 10 ** 2))
    print(f"The (approximate) number of iterations of the PageRank algorithm needed for the top 10 to stabilise: {approximation(G, 6)}")


if __name__ == "__main__":
    main()