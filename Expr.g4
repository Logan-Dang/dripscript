grammar Expr;
   
prog: statementList EOF;

statementList: (statement NEWLINE* )*;

statement
    : variableDeclaration ';'
    | fr
    | expr ';'
    ;

variableDeclaration: varType=IDENTIFIER varName=IDENTIFIER '=' expr;
fr: 'fr?' '(' expr ')' '{' NEWLINE* statementList NEWLINE* '}' ('no but' fr)? understandable?;
understandable: 'understandable' '{' statementList '}';

expr
    : left=expr op='^' right=expr #infixExpr
    | left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | left=expr op=('<'|'>'|'=='|'<='|'>=') right=expr #infixExpr
    | IDENTIFIER #idExpr
    | BANDS #bandsExpr
    | ESSAY #essayExpr
    | PERCHANCE #perchanceExpr
    | '(' expr ')' #parensExpr
    | '[' argList ']' #squareBracketExpr
    | '{' pairs '}' #curlyBracketExpr
    | functionName=IDENTIFIER '(' args=argList ')' #functionCallExpr
    | IDENTIFIER '[' expr ']' #listRetrievalExpr
    | IDENTIFIER '.' IDENTIFIER #dictRetrievalExpr
    ;

argList: expr (',' expr)*;

pair: key=IDENTIFIER ':' value=expr;

pairs: pair (',' pair)*;


OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_POW: '^';
OP_EQ: '==';
OP_LT: '<';
OP_GT: '>';
OP_LTE: '<=';
OP_GTE: '>=';

NEWLINE : [\r\n]+ -> skip ;
BANDS: [0-9]+ ('.' [0-9]+)?;
ESSAY  : '"' ( ~["\\] | '\\' . )* '"';
PERCHANCE : ('onGod' | 'cap');
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
WS      : [ \t\r\n] -> channel(HIDDEN);
