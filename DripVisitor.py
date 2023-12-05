from math import floor

import StdFuncs
from DripVariable import DripVariable
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from antlr4.Token import CommonToken


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
    
    def visitDictPutExpr(self, ctx: ExprParser.DictPutExprContext):
        dictVar = self.visit(ctx.dictVar)
        key = self.visit(ctx.key)
        value = self.visit(ctx.value)
        new_dict = dictVar.copy()
        new_dict[key] = value
        return new_dict
    
    def visitEssayExpr(self, ctx: ExprParser.EssayExprContext):
        return str(ctx.ESSAY()).split("\"")[1]
    
    def visitForLoop(self, ctx: ExprParser.ForLoopContext):
        index: CommonToken = ctx.index
        varName: CommonToken = ctx.varName
        listName: CommonToken = ctx.listName
        if varName.text in self.indentifiers:
            raise Exception(f'Variable {varName.text} already declared.')
        if index.text in self.indentifiers:
            raise Exception(f'Variable {index.text} already declared.')
        if listName.text not in self.indentifiers:
            raise Exception(f'Variable {listName.text} not declared.')
        var = self.indentifiers[listName.text]
        if var.type != 'list':
            raise Exception(f'Variable {listName.text} is not a list.')
        scoped_visitor = DripVisitor()
        scoped_visitor.indentifiers = self.indentifiers.copy()
        for i, value in enumerate(var.value):
            scoped_visitor.indentifiers[varName.text] = DripVariable(varName.text, value, drip_type(value))
            scoped_visitor.indentifiers[index.text] = DripVariable(index.text, i, 'bands')
            scoped_visitor.visit(ctx.statementList())
    
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
        if ctx.OP_IN():
            return a in b
    
    def visitRetrievalExpr(self, ctx: ExprParser.RetrievalExprContext):
        var = self.visit(ctx.varName)
        key = self.visit(ctx.key)
        if type(var) == dict:
            if key not in var:
                raise Exception(f'Key {key} not found in dictionary {var}.')
            return var[key]
        if type(var) == list:
            if type(key) != int:
                raise Exception(f'Index {key} is not an integer.')
            if key >= len(var):
                raise Exception(f'Index {key} out of range.')
            return var[key]
        raise Exception(f'Variable {var} is not a dictionary or list.')
            
        
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
        
        var = DripVariable(varName, value, varType, mutable=ctx.mut != None)
        self.indentifiers[varName] = var
        
    def visitVariableReDec(self, ctx: ExprParser.VariableReDecContext):
        varName = str(ctx.IDENTIFIER())
        if varName not in self.indentifiers:
            raise Exception(f'Variable {varName} not declared.')
        var = self.indentifiers[varName]
        if not var.mutable:
            raise Exception(f'Variable {varName} is not mutable.')
        value = self.visit(ctx.expr())
        if not type_is_valid(value, var.type):
            raise Exception(f'Invalid type for variable {varName}. Expected {var.type}, got {drip_type(value)}.')
        var.set_value(value)
    
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
    val_type = type(value)
    if val_type == str:
        return 'essay'
    if val_type == int or val_type == float:
        return 'bands'
    return type(value)