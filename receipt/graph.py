'''
Graph data structures for project. Adapted from personal code for Air Spares.
Written during Code for Good hackathon.

@author: grandpaa
'''
import copy

import numpy as np
import networkx as nx

class WordNode:

    # Coords should be in form (x, y, x_tol, y_tol)
    def __init__(self, word: str, coords: tuple, conf: int):
        self.word = word
        self.coords = coords
        self.conf = conf
        
    def distance_to(self, other: 'WordNode') -> float:
        my_x, my_y, _, _ = self.coords
        o_x, o_y, _, _ = other.coords
        
        dist = np.sqrt((my_x - o_x) ** 2 + (my_y - o_y) ** 2)        
        return dist
    
    def in_line(self, other: 'WordNode') -> tuple:
        my_x, my_y, my_xtol, my_ytol = self.coords
        o_x, o_y, o_xtol, o_ytol = other.coords    
                
        in_line_vert = my_x + my_xtol >= o_x - o_xtol \
                      and my_x - my_xtol <= o_x + o_xtol 
        in_line_horiz = my_y + my_ytol >= o_y - o_ytol \
                      and my_y - my_ytol <= o_y + o_ytol  
        
        return (in_line_horiz, in_line_vert)
        
    def set(self, target: 'WordNode') -> None:
        self.word = target.word
        self.coords = target.coords
        self.conf = target.conf
                
    def __eq__(self, other: 'WordNode') -> bool:
        is_eq = other.word == self.word and other.coords == self.coords
        
        return is_eq
        
    def __hash__(self) -> int:
        a, b, c, d = self.coords
        hash_float = 3 * hash(self.word) + 5 * a + 7 * b + 11 * c + 13 * d
        
        return int(hash_float)
    
    def __repr__(self) -> str:
        return('WordNode(word=%s, coords=%s, conf=%s)' 
               % (self.word, self.coords, self.conf))
    
    def __str__(self) -> str:
        return self.word
    
    @staticmethod
    def merge(*word_nodes) -> 'WordNode':
        empty_nodes = [node for node in word_nodes if node.word == '']
        for node in empty_nodes:
            word_nodes.remove(node)
        
        def merge_recurse(left: 'WordNode', stack: list) -> 'WordNode':            
            if (len(stack) == 1):
                return WordNode._merge_two(left, stack[0])
            else:
                new_left = WordNode._merge_two(left, stack[0])
                return merge_recurse(new_left, stack[1:]) 
        
        if len(word_nodes) > 1:
            return merge_recurse(word_nodes[0], word_nodes[1:])
        else:
            return word_nodes[0]
    
    @staticmethod   
    def _merge_two(left, right):
        lx, ly, lxtol, lytol = left.coords
        rx, ry, rxtol, rytol = right.coords
        
        # TODO: figure out correct coordinates of merged node
        assert(lx + lxtol <= rx - rxtol)
        new_word = left.word + right.word
        
        ul_corner = (lx - lxtol, ly - lytol)
        lr_corner = (rx + rxtol, ry + rytol)
        new_coords = WordNode._convert_coords_xyxy(ul_corner + lr_corner)
        
        new_conf = int(min(left.conf, right.conf) ** 2 / 100)
        
        return WordNode(new_word, new_coords, new_conf)
    
    
    @staticmethod
    def convert_coords(coords: tuple, scheme: str='xyxy') -> tuple:
        if scheme == 'xyxy':
            result = WordNode._convert_coords_xyxy(coords)
        elif scheme == 'xywh':
            result = WordNode._convert_coords_xywh(coords)
        else:
            raise RuntimeError('Scheme not recognized!')
            
        return result
    
    @staticmethod
    def _convert_coords_xyxy(coords: tuple) -> tuple:
        x0, y0, x1, y1 = coords
        mid = ((x0 + x1) / 2, (y0 + y1) / 2)            
        x_tol = x1 - mid[0]
        y_tol = y1 - mid[1]
        
        return (*mid, x_tol, y_tol)
    
    @staticmethod
    def _convert_coords_xywh(coords: tuple) -> tuple:        
        x, y, w, h = coords
        x_tol = w / 2
        y_tol = h / 2
        mid = (x + x_tol, y + y_tol)
        
        return (*mid, x_tol, y_tol)
        
class DocumentGraph:
    # TODO: more elegant solution?
    NONE_FIELD = {'dist': float('Inf'), 'inline': (False, False)}
    
    def __init__(self, word_nodes: list = []):
        self.graph = nx.Graph()
        self._connect(word_nodes)
    
    def _connect(self, word_nodes: list):
        for node in word_nodes:
            self.add_node(node)            
    
    def add_node(self, target: WordNode) -> None:
        if self.graph.number_of_nodes() == 0:
            self.graph.add_node(target)
        else:
            nodes = copy.deepcopy(self.graph.nodes)
            for node in nodes:
                self.graph.add_edge(
                    target, node,
                    dist=target.distance_to(node),
                    inline=target.in_line(node))
    
    def remove_node(self, target: WordNode) -> None:
        if target in self.graph.nodes():
            self.graph.remove_node(target)
        else:
            raise RuntimeWarning('Node not found: ', target.__repr__())
    
    def find_nodes(self, mark) -> list:
        if type(mark) is str:
            nodes = self._find_by_word(mark)
        elif type(mark) is tuple:
            nodes = self._find_by_coord(mark)
        else:
            raise RuntimeError('Input %s not identified' % mark)
        
        return nodes
    
    def _find_by_word(self, word: str) -> list:
        nodes = [node for node in self.graph.nodes if node.word == word]        
        return nodes
    
    # coord in form (x, y)
    def _find_by_coord(self, coord: tuple) -> list:
        x, y, = coord
        
        def _get_distance(node: WordNode):
            o_x, o_y, o_xtol, o_ytol = node.coords
            
            dx = max(abs(x - o_x) - o_xtol, 0)
            dy = max(abs(y - o_y) - o_ytol, 0)        
            dist = np.sqrt(dx ** 2 + dy ** 2)
            
            return (dist, node)
        
        distances = sorted([_get_distance(node) for node in self.graph.nodes],
                           key=lambda node: node[0])
        nodes = [pair[1] for pair in distances]                   
        return nodes
    
    def get_field(self, start: WordNode, stop: WordNode, field: str):
        if stop not in self.graph.adj[start]:
            info = DocumentGraph.NONE_FIELD[field] # TODO more natural solution
        else:
            info = self.graph.adj[start][stop][field]
        return info
            
    def get_row(self, node: WordNode, bounds: tuple = None):
        return self._get_line(node, 0, bounds)
    
    def get_col(self, node: WordNode, bounds: tuple = None):
        return self._get_line(node, 1, bounds)
    
    def _get_line(self, node: WordNode, axis: int, 
                  bounds: tuple = None) -> list:
        adj = self.graph.adj
              
        def _accept(other: WordNode) -> bool:
            do_accept = self.get_field(node, other, 'inline')[axis]
            if bounds is not None:
                do_accept &= other.coords[axis] >= bounds[0] \
                          and other.coords[axis] <= bounds[1]
            
            return do_accept
            
        line = [neighbor for neighbor in adj[node] if _accept(neighbor)]
        line.append(node)
                
        line.sort(key=lambda wn: wn.coords[axis])        
        return line
    
    # TODO: distinguish spaces and adjacents
    def merge_k(self, row: list, k: int) -> list:
        gaps = self.compute_gaps(row)
        gap_vals = [gap[0] for gap in gaps]
        
        lowest_idxs = np.argsort(gap_vals)[:k]
        lowest_idxs.sort()
        for i in lowest_idxs:
            _, left, right = gaps[i]
            merged_node = self.merge_nodes(left, right)
            row.remove(left)
            right.set(merged_node)           
    
    def compute_gaps(self, row: list) -> list:
        
        def _get_gap(left: WordNode, right: WordNode) \
                -> tuple:
            lx, _, lx_tol, _ = left.coords
            rx, _, rx_tol, _ = right.coords
            
            gap = (rx - rx_tol) - (lx + lx_tol)
            return (gap, left, right)
        
        gaps = [_get_gap(row[i], row[i+1]) for i in range(len(row) - 1)]
        return gaps
    
    # It's a BEAST!!! (with gutteral intonations)
    # TODO: make beast testable
    def clean(self, threshold: int = 25) -> None:

        def compute_adj_distance(me: WordNode, other: WordNode) -> float:
            mx, _, mx_tol, _ = me.coords
            ox, _, ox_tol, _ = other.coords
            
            dist = (ox - ox_tol) - (mx + mx_tol)
            return dist
        
        def inline_and_right(me: WordNode, other: WordNode) -> bool:
            is_inline = self.get_field(me, other, 'inline')[0]
            
            dist = compute_adj_distance(me, other)
            to_right = 0 < dist < threshold      
                  
            return is_inline and to_right
        
        def find_neighbor(node: WordNode) -> WordNode:
            candidates = [neighbor for neighbor in self.graph.adj[node]
                            if inline_and_right(node, neighbor)]
            target = None
            if len(candidates) > 0:
                target = min(candidates, key=lambda node: node.coords[0])
            
            return target
        
        node_stack = list(copy.deepcopy(self.graph.nodes()))
        while not len(node_stack) == 0:
            node = node_stack.pop()
            do_cont = True
                    
            while do_cont:
                target = find_neighbor(node)
                if target is not None:
                    merged_node = self.merge_nodes(node, target)
                    if target in node_stack:
                        node_stack.remove(target)
                        
                    node = merged_node
                else:
                    do_cont = False
                  
    def merge_nodes(self, left: WordNode, right: WordNode) -> WordNode:
        merged_node = WordNode.merge(left, right)
            
        self.remove_node(left)
        self.remove_node(right)
        self.add_node(merged_node)
        
        return merged_node
    
    
    
    
    
    
    