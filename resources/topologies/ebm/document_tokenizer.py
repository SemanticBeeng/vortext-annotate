import logging, re
log = logging.getLogger(__name__)

from document_handler import DocumentHandler
from nltk.tokenize.punkt import PunktSentenceTokenizer

class Handler(DocumentHandler):
    title = "Tokenizer"

    def __init__(self):
        log.info("constructing %s" % (self.title))

        self.word_token_pattern = re.compile(r"(?u)\b\w\w+\b")
        self.sentence_tokenizer = PunktSentenceTokenizer()

    def add_mapping(self, mapping, nodes, span):
        last = len(nodes) - 1
        for i, node in enumerate(nodes):
            element = mapping.elements.add()
            element.node_index = node["index"]
            element.range.lower = node["range"][0] if i != 0 else span[0]
            element.range.upper = node["range"][1] if i != last else span[1]

    def handle_document(self, document):
        """
        Adds sentence and word mappings to the document by tokenizing the full text,
        this allows the client-side to figure out where to position the sentence and word annotations.
        """
        text = document.text
        nodes = document.nodes
        node_intervals = [(n.interval.lower, n.interval.upper) for n in nodes]
        pages = document.pages

        sentence_spans = self.sentence_tokenizer.span_tokenize(text)

        def _is_overlapping(i1, i2):
            return i2[0] < i1[1] and i1[0] < i2[1]

        curr = 0
        for sentence_span in sentence_spans:
            sentence_nodes = []
            if _is_overlapping(sentence_span, node_intervals[max(curr - 1, 0)]):
                curr = max(curr - 1, 0)
            while not _is_overlapping(sentence_span, node_intervals[curr]):
                curr += 1
            while curr < len(nodes) and _is_overlapping(sentence_span, node_intervals[curr]):
                sentence_nodes += [{"index": curr,
                                    "range": (nodes[curr].interval.lower,
                                              nodes[curr].interval.upper)}]
                curr += 1

            if sentence_nodes:
                sentence_mapping = document.sentences.add()
                self.add_mapping(sentence_mapping, sentence_nodes, sentence_span)
           #sentence = text[sentence_span[0]:sentence_span[1]]

            # Add word mappings
            # for m in self.word_token_pattern.finditer(sentence):
            #     word_span = m.span()
            #     # Add sentence offset
            #     word_nodes = overlap.overlap_indices([x+sentence_span[0] for x in word_span])

            #     word_mapping = document.words.add()
            #     self.add_mapping(word_mapping, word_nodes, word_span)

        return document
