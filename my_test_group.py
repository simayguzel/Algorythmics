# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#
#
# This file is just a stub of the particular module that every group should
# implement for making its project work. In fact, all these functions returns None,
# which is not compliant at all with the specifications that have been provided at
# https://comp-think.github.io/2018-2019/slides/14%20-%20Project.html

import csv
from typing import Dict, Any
from collections import deque

import networkx as nx
from networkx import Graph, DiGraph


def process_citation_data(file_path):
    dict_data = {}

    with open(file_path, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            refs = row['known refs'].split('; ')  # The second element of the tuple is transformed in a list of refs
            if len(refs) == 1 and refs[0] == '':  # If there are no actual refs, the only element of the list is ''
                refs = []  # In this case, refs should be only an empty list, without the ''
            dict_data[row['doi']] = (int(row['cited by']), refs)


    #for r in dict_data:
        #print(r + ": " + str(dict_data[r]))

    return dict_data


def do_citation_graph(data, sse):
    citation_graph = DiGraph()

    for doi in data:  # For each doi (the key of the dict data)

        if not data[doi][1] == []: # With this if we discard any article not involved in any citation

            result = sse.search(doi, 'doi', False)  # Get the info about the article searching with the doi on the 'doi' column.
            # False because the output must not be a number.

            node_u = str(sse.pretty_print(result))  # Make the result pretty and turn it into a string so we can create a node
            #if node_u not in citation_graph:
            citation_graph.add_node(node_u)  # Add the node. The particular identifier of each node in the graph
            # should be a string representing the article.

            for ref in data[doi][1]:  # for each ref in the list of refs, which is the second element of the tuple associated to the doi (hence the 1)
                result = sse.search(ref, 'doi', False)  # Do the same as before. Get the infos about the article identified by the ref
                node_v = str(sse.pretty_print(result)) # Make it pretty and a string
                #if node_v not in citation_graph:
                citation_graph.add_node(node_v)
                citation_graph.add_edge(node_u, node_v)  # Add the edge from the node representing the doi and the node representing the referenced doi

    #citation_graph.nodes()
    #citation_graph.edges()
    return citation_graph

def do_coupling(data, sse, doi_1, doi_2):
    strenght= 0
    for ref in data[doi_1][1]:
        if ref in data[doi_2][1]:
            strenght= strenght +1
    return strenght

def do_aut_coupling(data, sse, aut_1, aut_2):
    coupling_strength = 0
    refs = list()
#    #locate the two authors in sse
    retrieve_aut1 = sse.search(aut_1, 'authors', False)
    retrieve_aut2 = sse.search(aut_2, 'authors', False)
#    #once located, identify their doi
    for index1 in range(len(retrieve_aut1)):
        doi_aut1 = retrieve_aut1[index1]['doi']
    for index2 in range(len(retrieve_aut2)):
        doi_aut2 = retrieve_aut2[index2]['doi']
        if (doi_aut1) != (doi_aut2):
            for ref in data[doi_aut1][1]:
                if ref in data[doi_aut2][1] and (ref not in refs):
                    coupling_strength= coupling_strength +1
                    refs.append(ref)
    return coupling_strength


def do_aut_distance(data, sse, aut):
    coauthor_network = Graph()

    visited = []
    coauthors_to_be_visited = deque()
    coauthors_to_be_visited.append(aut)

    while len(coauthors_to_be_visited) > 0:
        current_author = coauthors_to_be_visited.pop()
        if current_author in visited:
            continue
        visited.append(current_author)
        if current_author not in coauthor_network:
            coauthor_network.add_node(current_author)

        articles = sse.search(current_author, 'authors', False)
        coauthor_dict = {}
        for article in articles:
            authors = article['authors'].split('; ')
            for author in authors:  # For each author in the list of authors
                if author != current_author:  # We take in account only the other authors
                    if author in coauthor_dict:
                        coauthor_dict[author] += 1
                    else:
                        coauthor_dict[author] = 1

                    if author not in coauthor_network:
                        coauthor_network.add_node(author)
                    if author not in visited:
                        coauthors_to_be_visited.append(author)

        for coauthor in coauthor_dict:
            coauthor_network.add_edge(current_author, coauthor, co_authored_papers=coauthor_dict[coauthor])

    distances = calculateAllDistances(coauthor_network, aut)
    nx.set_node_attributes(coauthor_network, distances, name="distance")
    return coauthor_network


def calculateAllDistances(coauthor_network, aut):
    distance_dict = {}
    visited = []
    dist = 0
    nodes_to_visit = [aut]

    while len(visited) != len(coauthor_network.nodes):  # til all the nodes are visited

        listAdj = []
        for node in nodes_to_visit:
            if node in visited:  # if node is already visited do nothing
                continue
            visited.append(node)  # mark the node as visited
            if node not in distance_dict:
                distance_dict[node] = dist  # if the distance is not set yet, set it

            dist += 1  # increase the distance for the adjacents
            for adjacent in coauthor_network[node]:
                if adjacent not in visited:
                    listAdj.append(
                        adjacent)  # if the adjacent is not visited add it in the list of adjs for the next iteration
                if adjacent not in distance_dict:
                    distance_dict[adjacent] = dist  # already set their distances just because

        nodes_to_visit = listAdj  # the next nodes to visit (in the next iteration) are the adjacents,
        # so they all have the same distance

    return distance_dict


def do_cit_count_year(data, sse, aut, year):
    citations_aut_list = list()
    sumcitations = list()
    for doi in data:
        if not (data[doi][0] == 0 and data[doi][1] == []):
            aut = sse.search(aut, 'authors', False)
            result = sse.search(doi, 'doi', False)
            for writer in aut:
                if writer in result: # HOW TO CONNECT THE AUTHORS WITH THEIR DOI ARTICLES? I meant how to do this part "citations received by the papers authored by aut"
                    citations_aut_list.append(result)

    for article in citations_aut_list:
        year = sse.search(year, 'year', False)
        if article in year:
            sumcitations = article + 1
        else:
            return sumcitations
    year_citations = dict()
    year_citations[int("year")] = sumcitations()
    return year_citations
