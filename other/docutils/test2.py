from docutils import core
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser

class NoHeaderHTMLTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []

class Publisher(core.Publisher):
    def publish(self, data):
        help(self)
        #self.set_options()
        self.options.stylesheet = ''
        self.options._destination = ''

        parser = Parser()
        reader = Reader(parser, None)
        writer = Writer()
        writer.translator_class = NoHeaderHTMLTranslator
        iodata = core.io.StringIO(self.options, source=data)
        xmldata = reader.read(iodata, parser, None)
        xmldata.options = self.options
        return writer.write(xmldata, iodata)

def reSTify(s):
    return Publisher().publish(s)

if __name__ == '__main__':
    test = """
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print reSTify(test)

