from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from math import floor
from DripVariable import DripVariable
import StdFuncs

class MyExprVisitor(ExprVisitor):
    
    def __init__(self):
        super(MyExprVisitor, self).__init__()
        self.stack = []  # Stack to evaluate the expression
        self.indentifiers = {}   # Dictionary to store variables

    # Visit a parse tree produced by ExprParser#prog.
    def visitProg(self, ctx:ExprParser.ProgContext):
        return self.visit(ctx.statementList())

    # Visit a parse tree produced by ExprParser#infixExpr.
    def visitInfixExpr(self, ctx:ExprParser.InfixExprContext):
        self.visit(ctx.left)  # Evaluate the left  expression and push to stack
        self.visit(ctx.right) # Evaluate the right expression and push to stack

        b = self.stack.pop()  # Why is ‘b’ the first popped item?
        a = self.stack.pop()
        c = None

        if ctx.OP_ADD():
            c = a + b
        elif ctx.OP_SUB():
            c = a - b
        elif ctx.OP_MUL():
            c = a * b
        elif ctx.OP_DIV():
            c = a / b

        self.stack.append(c)
        return c
    
    def visitBandsExpr(self, ctx: ExprParser.BandsExprContext):
        c = float(str(ctx.BANDS()))
        if c == floor(c):
            c = int(c)
        self.stack.append(c)
        return c

    # Visit a parse tree produced by ExprParser#parensExpr.
    def visitParensExpr(self, ctx:ExprParser.ParensExprContext):
        return self.visit(ctx.expr())  # Since enclosed by parents, just visit expr
    
    def visitEssayExpr(self, ctx: ExprParser.EssayExprContext):
        c = str(ctx.ESSAY()).split("\"")[1]
        self.stack.append(c)
        return c
    
    def visitFunctionCallExpr(self, ctx: ExprParser.FunctionCallExprContext):
        func = str(ctx.IDENTIFIER())
        args = self.visit(ctx.argList())
        if func in StdFuncs.std_funcs:
            StdFuncs.std_funcs[func](*args)
        else:
            print(f'Unidentified token {func}.')
            
    def visitArgList(self, ctx: ExprParser.ArgListContext):
        for exprOrId in ctx.exprOrId():
            if isinstance(exprOrId, ExprParser.ExprAltContext):
                yield self.visit(exprOrId)
            elif isinstance(exprOrId, ExprParser.IdAltContext):
                yield self.indentifiers[str(exprOrId.IDENTIFIER())]
            
    def visitVariableDeclaration(self, ctx: ExprParser.VariableDeclarationContext):
        varType, varName = [str(node) for node in ctx.IDENTIFIER()]
        value = self.visit(ctx.expr())
        if not type_is_valid(value, varType):
            raise Exception(f'Invalid type for variable {varName}. Expected {varType}, got {drip_type(value)}.')
        
        var = DripVariable(varName, value, varType)
        self.indentifiers[varName] = var
        
def type_is_valid(value, varType):
    if type(value) == str and varType == 'essay':
        return True
    if (type(value) == int or type(value) == float) and varType == 'bands':
        return True
    return False

def drip_type(value):
    if type(value) == str:
        return 'essay'
    return type(value)