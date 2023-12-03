import sys
from antlr4 import CommonTokenStream, InputStream
from ExprParser import ExprParser
from ExprLexer import ExprLexer
from MyExprVisitor import MyExprVisitor

def main(argv):
  lexer = ExprLexer(InputStream('2 + 3 * 4'))
  stream = CommonTokenStream(lexer)
  parser = ExprParser(stream)
  tree = parser.prog()
  
  visitor = MyExprVisitor()
  res = visitor.visitProg(tree)
  print(res)
  
if __name__ == '__main__':
  main(sys.argv)