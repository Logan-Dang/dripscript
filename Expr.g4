grammar Expr;
   
prog: statementList EOF;

statementList: (statement NEWLINE* )+ ;

statement: expr ';';

expr: left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | BANDS                               #bandsExpr
    | ESSAY                               #essayExpr
    | '(' expr ')'                        #parensExpr
    | functionName=IDENTIFIER '(' args=exprList ')' #functionCallExpr
    ;

exprList
    : expr (',' expr)*
    ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';

NEWLINE : [\r\n]+ -> skip ;
BANDS: [0-9]+ ('.' [0-9]+)?;
ESSAY  : '"' ( ~["\\] | '\\' . )* '"';
WS      : [ \t\r\n] -> channel(HIDDEN);
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
