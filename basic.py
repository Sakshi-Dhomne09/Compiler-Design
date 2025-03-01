#from strings_with_arrows import *

DIGITS = '0123456789'

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start=pos_start
        self.pos_end=pos_end
        self.error_name=error_name
        self.details = details

    def as_string(self):
        result=f'{self.error_name}:{self.details}'
        result+=f'File{self.pos_start.filename},line{self.pos_start.line+1}'
        result += '\n\n' + (self.pos_start.filetext, self.pos_start, self.pos_end)

        return result
    
class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,"Illegal Character",details)

class InvalidSyntaxError():
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,"Invalid Syntax",details)
  
class Position:
    def __init__(self,index,line,col,filename,filetext):
        self.index=index
        self.line=line
        self.col=col
        self.filename=filename
        self.filetext=filetext

    def advance(self,current_char=None):
        self.index+=1
        self.col+=1

        if current_char=='\n':
            self.line+=1
            self.col=0

        return self
    
    def copy(self):
        return Position(self.index,self.line,self.col,self.filename,self.filetext)
    
class Token:
    def __init__(self,type,value=None,pos_start=None,pos_end=None) :
        self.type=type
        self.value=value
        if pos_start:
            self.pos_start=pos_start.copy()
            self.pos_end=pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end=pos_end

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self,filename,text):
        self.text=text
        self.filename=filename
        self.pos=Position(-1,0,-1,filename,text)
        self.current_char=None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char=self.text[self.pos.index] if self.pos.index<len(self.text) else None

    def make_tokens(self):
        tokens=[]
        while self.current_char !=None:
            if self.current_char in '\t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char=='+':
                tokens.append(Token(TT_PLUS,pos_start=self.pos))
                self.advance()
            elif self.current_char=='-':
                tokens.append(Token(TT_MINUS,pos_start=self.pos))
                self.advance()
            elif self.current_char=='*':
                tokens.append(Token(TT_MUL,pos_start=self.pos))
                self.advance()
            elif self.current_char=='/':
                tokens.append(Token(TT_DIV,pos_start=self.pos))
                self.advance()
            elif self.current_char=='(':
                tokens.append(Token(TT_LPAREN,pos_start=self.pos))
                self.advance()
            elif self.current_char==')':
                tokens.append(Token(TT_RPAREN,pos_start=self.pos))
                self.advance()
            else:
                pos_start=self.pos.copy()
                char=self.current_char
                self.advance()
                return [],IllegalCharError(pos_start,self.pos,"'"+ char + "'")
        tokens.append(Token(TT_EOF,pos_start=self.pos))
        return tokens,None
    def make_number(self):
        num_str=''
        dot_count =0
        pos_start=self.pos.copy()
        while self.current_char!=None and self.current_char in DIGITS + '.':
            if self.current_char =='.':
                if dot_count ==1:
                    break
                dot_count+=1
                num_str+='.'
            else:
                num_str+=self.current_char
            self.advance()  
        if dot_count==0:
            return Token(TT_INT,int(num_str),pos_start,self.pos)
        else:
            return Token(TT_FLOAT,float(num_str),pos_start,self.pos)


##Nodes
        
class NumberNodes:
    def __init__(self,tok):
        self.tok=tok
    def __repr__(self):
        return f'{self.tok}'
    def evaluate(self):
        return self.tok.value

# class BinOpNode:
#     def __init__(self,left_node,op_tok,right_node):
#         self.left_node=left_node
#         self.op_tok=op_tok
#         self.right_node=right_node
#     def __repr__(self):
#         return f'({self.left_node},{self.op_tok},{self.right_node})'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    def __repr__(self):
        return f'({self.left_node},{self.op_tok},{self.right_node})'
    def evaluate(self):
        if self.op_tok.type == TT_PLUS:
            return self.left_node.evaluate() + self.right_node.evaluate()
        elif self.op_tok.type == TT_MINUS:
            return self.left_node.evaluate() - self.right_node.evaluate()
        elif self.op_tok.type == TT_MUL:
            return self.left_node.evaluate() * self.right_node.evaluate()
        elif self.op_tok.type == TT_DIV:
            return self.left_node.evaluate() / self.right_node.evaluate()


# class UnnaryOpNode:
#     def __init__(self,op_tok,node):
#         self.op_tok=op_tok
#         self.node=node
#     def __repr__(self):
#         return f'({self.op_tok},{self.node})'
        
class UnnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    def __repr__(self):
        return f'({self.op_tok},{self.node})'
    def evaluate(self):
        if self.op_tok.type == TT_PLUS:
            return +self.node.evaluate()
        elif self.op_tok.type == TT_MINUS:
            return -self.node.evaluate()
		
class ParseResult:
    def __init__(self):
        self.error=None
        self.node=None 
    def register(self,res):
        if isinstance(res,ParseResult):
            if res.error:
                self.error=res.error
            return res.node

        return res
    def success(self,node):
        self.node=node
        return self
    def failure(self,error):
        self.error=error
        return self

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.tok_idx=-1
        self.advance()

    def advance(self):
        self.tok_idx+=1
        if self.tok_idx<len(self.tokens):
            self.current_tok=self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res=self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
           return res.failure(InvalidSyntaxError(
               self.current_tok.pos_start,self.current_tok.pos_end,
               "Expected '+','-','*' or '/'"
           ))
        return res

    def factor(self):
        res=ParseResult()
        tok=self.current_tok

        if tok.type in (TT_PLUS,TT_MINUS):
            res.register(self.advance())
            factor=res.register(self.factor())
            if res.error:
                return res
            return  res.success(UnnaryOpNode(tok,factor))
  
        elif tok.type in (TT_INT,TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNodes(tok))
        elif tok.type==TT_LPAREN:
            res.register(self.advance())
            expr=res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type==TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected int or float"))
        return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end,"Expected int or float"))
        
    def term(self):
        return self.bin_op(self.factor,(TT_MUL,TT_DIV))
    
    def expr(self):
        return self.bin_op(self.term,(TT_PLUS,TT_MINUS))
    
    def bin_op(self,func,ops):
        res=ParseResult()
        left=res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok=self.current_tok
            res.register(self.advance())
            right=res.register(func())
            if res.error:
                return res
            left=BinOpNode(left,op_tok,right)
        return res.success(left)
        
def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    # Generate abstract syntax tree
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    return ast.node,ast.node.evaluate(), None

