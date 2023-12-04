grammar Expr;
   
prog: statementList EOF;

statementList: (statement NEWLINE* )+ ;

statement: variableDeclaration ';'
         | expr ';'
         ;

variableDeclaration: varType=IDENTIFIER varName=IDENTIFIER '=' expr;

expr: left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | IDENTIFIER                          #idExpr
    | BANDS                               #bandsExpr
    | ESSAY                               #essayExpr
    | PERCHANCE                           #perchanceExpr
    | '(' expr ')'                        #parensExpr
    | '[' argList ']'                     #squareBracketExpr
    | '{' pairs '}'         #curlyBracketExpr
    | functionName=IDENTIFIER '(' args=argList ')' #functionCallExpr
    ;

argList: expr (',' expr)*;

pair: key=IDENTIFIER ':' value=expr;

pairs: pair (',' pair)*;


OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';

NEWLINE : [\r\n]+ -> skip ;
BANDS: [0-9]+ ('.' [0-9]+)?;
ESSAY  : '"' ( ~["\\] | '\\' . )* '"';
PERCHANCE : ('onGod' | 'cap');
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
WS      : [ \t\r\n] -> channel(HIDDEN);
