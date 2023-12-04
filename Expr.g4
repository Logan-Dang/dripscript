grammar Expr;
   
prog: statementList EOF;

statementList: (statement NEWLINE* )+ ;

statement: variableDeclaration ';'
         | expr ';'
         ;

variableDeclaration: varType=IDENTIFIER varName=IDENTIFIER '=' expr;

expr: left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | BANDS                               #bandsExpr
    | ESSAY                               #essayExpr
    | '(' expr ')'                        #parensExpr
    | functionName=IDENTIFIER '(' args=argList ')' #functionCallExpr
    ;

argList
    : exprOrId (',' exprOrId)*
    ;

exprOrId
    : expr   #exprAlt
    | IDENTIFIER #idAlt
    ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';

NEWLINE : [\r\n]+ -> skip ;
BANDS: [0-9]+ ('.' [0-9]+)?;
ESSAY  : '"' ( ~["\\] | '\\' . )* '"';
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
WS      : [ \t\r\n] -> channel(HIDDEN);
