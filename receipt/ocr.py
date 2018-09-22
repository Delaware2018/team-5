'''
Wrapper for tesseract stuff. Adapted from personal code for Air Spares.
Written during Code for Good hackathon

@author: grandpaa
'''
import logging
logging.basicConfig(level='INFO')

from bs4 import BeautifulSoup
from tesserocr import PyTessBaseAPI

from .graph import WordNode, DocumentGraph

class OCREngine:
    
    def __init__(self, psm: int = 3, config: dict = {}):
        logging.info('Initializing OCR engine with PSM=%d and configs=%s' 
                    % (psm, config))
        self.api = PyTessBaseAPI(psm=psm)
        for key in config.keys():
            self.api.SetVariable(key, config[key])
        logging.debug('OCR engine initialized')
    
    def build_graph(self,
                    image_path: str,
                    scheme: str = None) -> DocumentGraph:
        
        hocr = self._get_hocr(image_path)
        words = self._get_words(hocr, scheme)
        dg = DocumentGraph(words)
        
        return dg
    
    def _get_hocr(self, image_path: str) -> str:   
        logging.info('Reading to hOCR from image: %s' % image_path)   
        self.api.SetImageFile(image_path)
        hocr_text = self.api.GetHOCRText(0)
        logging.debug('Image read')
        
        return hocr_text
    
    def _get_words(self, hocr: str, scheme: str = None):
        logging.info('Extracting words from hOCR.')
        if scheme is None:
            logging.warning('No scheme specified. Assuming xyxy')
            scheme = 'xyxy'
        
        soup = BeautifulSoup(hocr, 'html.parser')
        word_tags = soup.select('.ocrx_word')
        
        word_nodes = [self._make_node(tag, scheme=scheme) for tag in word_tags]
        word_nodes = list(filter(
            lambda node: node is not None, 
            word_nodes))
        
        return word_nodes
    
    def _make_node(self, tag: dict, scheme: str) -> WordNode:
        fields = tag['title'].split(';')
        if not len(fields) == 2:
            logging.warn('Malformed tag: %s. Skipping.' % tag)
            return None
        
        word = tag.text
        coordinates = tuple(map(int, fields[0].split()[1:]))
        conf = int(fields[1].split()[1])
        
        wn = WordNode(word, 
                      WordNode.convert_coords(coordinates, scheme), 
                      conf)
        logging.debug('Made word: %s' % wn.__repr__())
        
        return wn
    
    def close(self):
        self.api.End()
        logging.debug('OCR engine closed')
           
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("type: %s\nvalue: %s\ntrace: %s" 
                  % (exc_type, exc_value, traceback))
            
        self.close()
    
    
    
    
        
