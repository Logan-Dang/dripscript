from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from math import floor

class MyExprVisitor(ExprVisitor):
    std_funcs = {'yap': print}
    
    def __init__(self):
        super(MyExprVisitor, self).__init__()
        self.stack = []  # Stack to evaluate the expression

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
        args = self.visit(ctx.exprList())
        if func in MyExprVisitor.std_funcs:
            MyExprVisitor.std_funcs[func](*args)
        else:
            print(f'Unidentified token {func}.')
        
    def visitExprList(self, ctx: ExprParser.ExprListContext):
        for expr in ctx.expr():
            yield self.visit(expr)