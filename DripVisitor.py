from math import floor

import StdFuncs
from DripVariable import DripVariable
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor


class DripVisitor(ExprVisitor):
    
    def __init__(self):
        super(DripVisitor, self).__init__()
        self.indentifiers: dict[str, DripVariable] = {}   # Dictionary to store variables
            
    def visitArgList(self, ctx: ExprParser.ArgListContext):
        return (self.visit(expr) for expr in ctx.expr())

    def visitBandsExpr(self, ctx: ExprParser.BandsExprContext):
        num = float(str(ctx.BANDS()))
        if num == floor(num):
            num = int(num)
        return num
    
    def visitCurlyBracketExpr(self, ctx: ExprParser.CurlyBracketExprContext):
        return self.visit(ctx.pairs())
    
    def visitDictRetrievalExpr(self, ctx: ExprParser.DictRetrievalExprContext):
        d, key = [str(node) for node in ctx.IDENTIFIER()]
        if d not in self.indentifiers:
            raise Exception(f'Variable {d} not declared.')
        var = self.indentifiers[d]
        if var.type != 'dict':
            raise Exception(f'Variable {d} is not a dictionary.')
        if key not in var.value:
            raise Exception(f'Key {key} not found in dictionary {d}.')
        return var.value[key]
    
    def visitEssayExpr(self, ctx: ExprParser.EssayExprContext):
        return str(ctx.ESSAY()).split("\"")[1]
    
    def visitFr(self, ctx: ExprParser.FrContext):
        condition = self.visit(ctx.expr())
        if type(condition) != bool:
            raise Exception(f'Condition {condition} is not a boolean.')
        if not condition:
            if ctx.fr():
                self.visit(ctx.fr())
            if ctx.understandable():
                self.visit(ctx.understandable())
            return
        scoped_visitor = DripVisitor()
        scoped_visitor.indentifiers = self.indentifiers.copy()
        scoped_visitor.visit(ctx.statementList())

    def visitFunctionCallExpr(self, ctx: ExprParser.FunctionCallExprContext):
        func = str(ctx.IDENTIFIER())
        args_list = self.visit(ctx.args)
        if func in StdFuncs.std_funcs:
            StdFuncs.std_funcs[func](*args_list)
        else:
            print(f'Unidentified token {func}.')
            
    def visitIdExpr(self, ctx: ExprParser.IdExprContext):
        varName = str(ctx.IDENTIFIER())
        if varName in self.indentifiers:
            return self.indentifiers[varName].value
        else:
            raise Exception(f'Variable {varName} not declared.')

    def visitInfixExpr(self, ctx:ExprParser.InfixExprContext):
        a = self.visit(ctx.left)
        b = self.visit(ctx.right)
        if ctx.OP_ADD():
            return a + b
        if ctx.OP_SUB():
            return a - b
        if ctx.OP_MUL():
            return a * b
        if ctx.OP_DIV():
            return a / b
        if ctx.OP_POW():
            return a**b
        if ctx.OP_GT():
            return a > b
        if ctx.OP_LT():
            return a < b
        if ctx.OP_GTE():
            return a >= b
        if ctx.OP_LTE():
            return a <= b
        if ctx.OP_EQ():
            return a == b
    
    def visitListRetrievalExpr(self, ctx: ExprParser.ListRetrievalExprContext):
        var_name = str(ctx.IDENTIFIER())
        if var_name not in self.indentifiers:
            raise Exception(f'Variable {var_name} not declared.')
        var = self.indentifiers[var_name]
        if var.type != 'list':
            raise Exception(f'Variable {var_name} is not a list.')
        index = self.visit(ctx.expr())
        if type(index) != int:
            raise Exception(f'Index {index} is not an integer.')
        if index >= len(var.value):
            raise Exception(f'Index {index} out of range.')
        return var.value[index]
        
    def visitSquareBracketExpr(self, ctx: ExprParser.SquareBracketExprContext):
        args = self.visit(ctx.argList())
        return [*args]
    
    def visitPairs(self, ctx: ExprParser.PairsContext):
        return { key: value for key, value in (self.visit(pair) for pair in ctx.pair())}
            
    
    def visitPair(self, ctx: ExprParser.PairContext):
        key = str(ctx.IDENTIFIER())
        value = self.visit(ctx.value)
        return (key, value)

    def visitParensExpr(self, ctx:ExprParser.ParensExprContext):
        return self.visit(ctx.expr())
    
    def visitPerchanceExpr(self, ctx: ExprParser.PerchanceExprContext):
        perchance = str(ctx.PERCHANCE())
        if perchance == 'onGod':
            return True
        elif perchance == 'cap':
            return False
        raise Exception(f'Unidentified token {perchance}.')

    def visitProg(self, ctx:ExprParser.ProgContext):
        self.visit(ctx.statementList())
        
    def visitUnderstandable(self, ctx: ExprParser.UnderstandableContext):
        scoped_visitor = DripVisitor()
        scoped_visitor.indentifiers = self.indentifiers.copy()
        scoped_visitor.visit(ctx.statementList())        
            
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
    if (type(value) == bool) and varType == 'perchance':
        return True
    if (type(value) == list) and varType == 'list':
        return True
    if (type(value) == dict) and varType == 'dict':
        return True
    return False

def drip_type(value):
    if type(value) == str:
        return 'essay'
    return type(value)