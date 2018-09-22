'''
Reads receipts from image. For Code for Good hackathon

@author: grandpaa
'''

from .data import Item
from .ocr import OCREngine
from .graph import DocumentGraph, WordNode

# TODO: implement specific configs for tesseract
def read_receipt(im: str) -> list:
    graph = _get_graph(im)
    items = _get_items(graph)
    return items
    
def _get_graph(im: str) -> str:
    with OCREngine() as engine:
        hocr = engine.build_graph(im)
    
    return hocr

def _get_items(graph: DocumentGraph) -> list:
    date = _get_date(graph)
    
    item = graph.find_nodes('Item')[0]
    item_col = graph.get_col(item)
    
    start_pos = item_col.index(item)
    item_nodes = item_col[start_pos + 1 : start_pos + 4]
    
    def _extract_item(col_node: WordNode) -> Item:
        item_row = graph.get_row(col_node)
        description = item_row[0].word
        value = int(item_row[2].word)
        
        entry_dict = {
            'date_added': date,
            'description': description,
            'value': value
        }
        
        item = Item(entry_dict)
        return item
    
    items = [_extract_item(node) for node in item_nodes]
    return items
    
def _get_date(graph: DocumentGraph) -> str:
    date_name = graph.find_nodes('Date:')[0]
    date_node = graph.get_row(date_name)[1]
    
    return date_node.word

def main():
    receipt_path = 'receipt.png'
    print(read_receipt(receipt_path))

if __name__ == '__main__':
    main()
    
    
    
    
