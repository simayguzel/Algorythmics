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
from anytree import Node, RenderTree, NodeMixin


def process_citation_data(file_path):
    dict_data = {}
    with open(file_path, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            refs = row['known refs'].split('; ')
            if len(refs) == 1 and refs[0] == '':
                refs = []
            dict_data[row['doi']] = (int(row['cited by']), refs)


    return dict_data



def do_get_coauthor(author, sse):

    get_aut = list(set(sse.coauthor_network(author).nodes()))
    get_aut.remove(author)
    
    return get_aut
    # coauthors = set()
    # author_search = sse.search(author, 'authors', False)  # it returns a list.
    # for each in author_search:
    #     coauthors.update(each['authors'].split('; '))
    # coauthors.remove(author)
    # return coauthors

def do_coauthor_hierarchy(data, sse, aut):
    added_coaut = deque()
    root_node = Node(aut, parent=None)
    coaut_dict = dict()
    list_of_coauthors = list(set(sse.coauthor_network(aut).nodes()))
    list_of_coauthors.remove(aut)
    coaut_dict[aut] = list_of_coauthors
    visited =list()
    visited.append(aut)
    for item in list_of_coauthors:
        added_coaut.append(item)
    first_level = Node(list_of_coauthors, parent=root_node)
    renderer = RenderTree(root_node)
    #print(first_level)
    #print(list_of_coauthors)
    while added_coaut:
        node_to_visit = added_coaut.popleft()
        #print(node_to_visit)
        visited.append(node_to_visit)
        newsearch = do_get_coauthor(node_to_visit, sse)
        print(list_of_coauthors)
        for item in newsearch:
            if item != aut and item not in visited:
                added_coaut.append(item)
                coaut_dict[node_to_visit] = newsearch
    print(coaut_dict)
    #print(coaut_dict)
    #print(renderer)
    #     for cocuk in coaut_dict.keys():
    #         print(cocuk)
    #         if cocuk not in visited:
    #             added_coaut.append(cocuk)
    #             visited.append(cocuk)
    # coaut_dict[cocuk] = coaut_dict[newsearch]+1
    #print(coaut_dict)
    #     #print(node_to_visit)
    # #if node_to_visit not in a:
    #     coauthop = set(sse.coauthor_network(node_to_visit).nodes())
    #     for key, value in coaut_dict:
    #         coaut_dict[node_to_visit] = coauthop
    #         print(coaut_dict)

        # a.update(coauthors)
        # a.remove(aut)
        #
        # #print(coauthors)
        # if node_to_visit not in coaut_dict:
        #     for key in a:
        #         print(key)
                # if key not in coaut_dict[node_to_visit][0]:
                #     newlevel = coaut_dict[key]
                #     for node_to_visit in newlevel:
                #         coaut_dict.update({(do_get_coauthor(sse, node_to_visit))})

        #coaut_dict[node_to_visit] = coauthors
    #print(node_to_visit)
    #print(coauthors)
    #renderer = RenderTree(root_node)
    #print(renderer)
    #print(coaut_dict)


