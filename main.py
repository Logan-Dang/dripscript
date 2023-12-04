import sys
from antlr4 import CommonTokenStream, InputStream
from ExprParser import ExprParser
from ExprLexer import ExprLexer
from DripVisitor import DripVisitor

def main(argv):
  if len(argv) < 2:
    print('Usage: python main.py <filename>')
    return
  
  with open(argv[1], 'r') as file:
    input_stream = InputStream(file.read())  
  lexer = ExprLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = ExprParser(stream)
  tree = parser.prog()
  
  visitor = DripVisitor()
  visitor.visitProg(tree)
  
if __name__ == '__main__':
  main(sys.argv)