grammar Expr;
   
prog: statementList EOF;

statementList: (statement NEWLINE* )*;

statement
    : variableDeclaration ';'
    | variableReDec ';'
    | fr
    | expr ';'
    | forLoop
    ;

variableDeclaration: mut='mut'? varType=IDENTIFIER varName=IDENTIFIER '=' expr;
variableReDec: varName=IDENTIFIER '=' expr;
fr: 'fr?' '(' expr ')' '{' NEWLINE* statementList NEWLINE* '}' ('no but' fr)? understandable?;
understandable: 'understandable' '{' statementList '}';
forLoop: 'for every' index=IDENTIFIER ',' varName=IDENTIFIER 'in the' listName=IDENTIFIER '{' NEWLINE* statementList NEWLINE* '}';

expr
    : left=expr op='^' right=expr #infixExpr
    | left=expr op=('*'|'/') right=expr   #infixExpr
    | left=expr op=('+'|'-') right=expr   #infixExpr
    | left=expr op=('<'|'>'|'=='|'<='|'>=') right=expr #infixExpr
    | left=expr op='in' right=expr #infixExpr
    | IDENTIFIER #idExpr
    | BANDS #bandsExpr
    | ESSAY #essayExpr
    | PERCHANCE #perchanceExpr
    | '(' expr ')' #parensExpr
    | '[' argList ']' #squareBracketExpr
    | '{' pairs '}' #curlyBracketExpr
    | functionName=IDENTIFIER '(' args=argList ')' #functionCallExpr
    | varName=expr '[' key=expr ']' #retrievalExpr
    | dictVar=expr '<-' '(' key=expr ',' value=expr ')' #dictPutExpr
    ;

argList: expr (',' expr)*;

pair: key=IDENTIFIER ':' value=expr;

pairs: pair? (',' pair)*;

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
OP_IN: 'in';

NEWLINE : [\r\n]+ -> skip ;
COMMENT : '//' .*? ('\n' | EOF) -> skip;
BANDS: [0-9]+ ('.' [0-9]+)?;
ESSAY  : '"' ( ~["\\] | '\\' . )* '"';
PERCHANCE : ('onGod' | 'cap');
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;
WS      : [ \t\r\n] -> channel(HIDDEN);
