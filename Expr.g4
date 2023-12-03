grammar Expr;

prog: statement* EOF;

statement: varDeclaration
         | expr
         ;

varDeclaration: 'essay' ID '=' STRING ';';

expr: left=expr op=('+'|'-') right=expr   #infixExpr
    | left=expr op=('*'|'/') right=expr   #infixExpr
    | INT                                 #numberExpr
    | '(' expr ')'                        #parensExpr
    | ID                                  #variableExpr
    ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';

NEWLINE : [\r\n]+ ;
INT     : [0-9]+ ;
ID      : [a-zA-Z_][a-zA-Z_0-9]* ;
STRING  : '\'' .*? '\'' ;
WS      : [ \t\r\n] -> channel(HIDDEN);
