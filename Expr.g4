grammar Expr;
   
prog: expr EOF;

expr: left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | INT                                 #numberExpr
    | STRING                              #stringExpr
    | '(' expr ')'                        #parensExpr
    ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';

NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;
STRING  : '"' ( ~["\\] | '\\' . )* '"';
WS      : [ \t\r\n] -> channel(HIDDEN);