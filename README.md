# impl-basic-toy
Implement a simple basic interpreter toy in Python.

## Run
`python3 run.py`

## Progress
- [x] Basic Lexer
- [x] Basic Parser
- [x] Basic Interpreter
- [x] Power Operator
- [x] Variables
- [x] Comparisons and logical operators
- [x] IF statement
- [x] FOR and WHILE statement
- [x] Functions
- [x] Strings
- [x] Lists
- [x] Built-in Functions
- [x] Multi-line statements
- [x] RETURN, CONTINUE, BREAK
- [x] RUN statement and comments

## Implement details
### 1. 设计目的及要求
**解释器的核心结构包括如下部分：**

- 词法分析器：能够将输入的程序单元分析产生Token。
- 语法分析器：将生成的 Token 转换为抽象语法树（AST）。
- 解释执行器：将抽象语法树进行翻译执行，产生结果值并返回。
- 符号表：将结果值保存到符号表中，实现上下文联系。

**解释器支持的程序语言特性包括如下部分：**

- 基本算数运算功能：加减乘除运算、幂运算
- 支持变量赋值： `VAR a = 3`
- 比较和逻辑运算符：比较运算符`>`, `>=`等，逻辑运算符`AND`, `OR`等
- 条件`IF`语句：`VAR a = IF 5 == 5 THEN 10`，多行 IF 如下：
```BASIC
VAR age = 19;
IF age > 20 THEN
  VAR ex = 20
ELSE
  VAR ex = 25
END
```
- `FOR`与`WHILE`循环语句：`FOR i = 1 TO 6 THEN VAR result = result * i`，多行循环语句如下：
```BASIC
// FOR
VAR a = 0
FOR i = 0 TO 10 THEN
  IF i == 4 THEN
    VAR a = a + i
  ELIF i == 8 THEN
    VAR a = a + 2 * i
  END
END
```
- 函数定义及调用功能：如定义两数相加`FUN add(a, b) -> a + b`，调用该函数即`add(1, 2)`

- 字符串功能：包括可赋值字符串变量、字符串拼接、转义符实现。

- 实现 List 列表：如下列表定义及相关操作
```BASIC
[]
[1, 2, 3, 4, 5]
[1, 2, 3] + 4 => [1, 2, 3, 4]
[1, 2, 3] * [3, 4, 5] => [1, 2, 3, 4, 5]
[1, 2, 3] - 1 => [1, 3]
[1, 2, 3] / 0 => 1
```
- 一些内置的函数库：如`PRINT`, `INPUT`等库函数。
- RETURN, CONTINUE, BREAK关键字
- 运行整个程序文件及注释功能
- 较为完备的错误提示

### 2. 设计内容、主要算法描述
#### 2.1 语言文法定义
参考 [BASIC-JS-Interpreter](https://githubmemory.com/repo/sathishrazor/BASIC-JS-Interpreter)的 Basic 文法描述，所实现的类 Baisc 解释器文法定义如下
```
statements: NEWLINE* statement (NEWLINE* statement)*  NEWLINE*

statement : KEYWORD:RETURN expr?
          : KEYWORD:CONTINUE
          : KEYWORD:BREAK
          : expr

expr    : KEYWORD:VAR IDENTIFIER EQ expr
        : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*

comp-expr  : NOT comp-expr
           : arith-expr ((EE|NE|LT|GT|LTE|GTE) arith-expr)*

arith-expr : term ((PLUS|MINUS) term)*

term    : factor ((MUL|DIV) factor)*

factor  : (PLUS|MINUS) factor
        : power

power   : call (POW factor)*

call    : atom (LPAREN (expr (COMMA expr)*)? RPAREN)?

atom    : INT|FLOAT|STRING|IDENTIFIER
        : LPAREN expr RPAREN
        : list-expr
        : if-expr
        : for-expr
        : while-expr
        : func-def

list-expr: LSQUARE (expr (COMMA expr*)*)? RASQURE

if-expr : KEYWORD:IF expr KEYWORD:THEN
          (statement if-expr-b|if-expr-c?)
        | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)

if-expr-b : KEYWORD:ELIF expr KEYWORD:THEN
          (statement if-expr-b|if-expr-c?)
        | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)

if-expr-c : KEYWORD:ELSE expr
          statement
        | (NEWLINE statements KEYWORD:END)

for-expr: KEYWORD:FOR IDENTIFIER EQ expr KEYWORD:TO expr
          (KEYWORD:STEP expr)? KEYWORD:THEN
          statement
        | (NEWLINE statements KEYWORD:END)

while-expr: KEYWORD:WHILE expr KEYWORD:THEN
          statement
        | (NEWLINE statements KEYWORD:END)

func-def : KEYWORD:FUN IDENTIFIER?
           LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN
           (ARROW expr)
        |  (NEWLINE statements KEYWORD:END)
```

#### 2.2 词法分析器 Lexer
词法分析器 Lexer 的功能是输入源程序，按照构词规则分解成一系列单词符号。

单词具有独立意义的最小单位，包括关键字、标识符、运算符、界符等.

以标识符`IDENTIFIER`为例，算法实现的状态转换图功能描述为下：

<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/state.png" alt="1" style="zoom:50%;" />

其中 0 为初态，2 为终态。这个转换图识别（接受）标识符的过程是：从初态0开始，若在状态0之下输入字符是一个字母，则读进它，并转入状态1。在状态1之下，若下一个输入字符为字母或数字或下划线，则读进它，并重新进入状态1。一直重复这个过程直到状态1发现输入字符不再是字母或数字时就结束进入状态 2 终态，即开始识别其他类型 Token。

`Lexer`的`IDENTIFIER`标识符识别核心实现代码细节如下：
```Python
class Lexer:
    def make_tokens(self):
        while self.current_char is not None:
            ...
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            ...
        return tokens, None

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while (
            self.current_char is not None and self.current_char in LETTERS_DIGITS + "_"
        ):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
```

#### 2.3 语法分析器 Parser

语法分析器 Parser 基于词法分析器 Lexer，对识别出来的单词的形式通过定义的文法进行分析。

上述定义的 类 Basic 语言文法不含左递归产生式，可以直接实现自顶向下/递归向下的语法分析器 Paser。

其接受输入是词法分析器生成的 `tokens`，输出是一颗抽象语法树 `ast`。

以`statements: NEWLINE* statement (NEWLINE* statement)*  NEWLINE*`这条产生式为例，其递归分析过程如下：
```Python
    def statements(self):
        ...
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        statement = res.register(self.statement())
        ...

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            ...
            statement = res.try_register(self.statement())

        return ...
```

#### 2.4 解释执行器 Interpreter

解释器执行器 Interpreter 基于语法分析器 Parser，对抽象语法树 AST 进行解释执行，并将结果返回。

由语法分析器 Parser 所获取的树节点类名，以赋值运算表达式为例，赋值运算表达式节点类名为`VarAccessNode`

在 Interpreter 中调用`visit`方法进行访问，`visit`方法调用`visit_VarAccessNode`解释赋值运算表达式。

核心实现代码细节如下：
```Python
class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    ...
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{var_name}' is not defined",
                    context,
                )
            )

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
```

#### 2.5 错误类型提示
作为一个完备的解释器，也应当具有错误类型提示功能，在程序解释执行时，每一个分析阶段遇到错误时，应返回相应的类型错误。

- 词法分析阶段
  - 非法字符错误(`IllegalCharError`)：除定义的合法字符外，程序输入有非法字符。
  - 缺少/期待字符错误(`ExpectedCharError`)：如不等于逻辑运算`!=`只输入`!`，缺少`=`。
- 语法分析阶段
  - 非法语法错误(`InvalidSyntaxError`)：程序存在语法错误，如缺少关键字、缺少标识符等语法错误。
- 解释执行阶段
  - 运行时错误(`RTError`)：程序在解释执行时出现的错误，如访问未定义变量、除 0 错误等。

实现细节是定义一个 `Error` 基类，各种错误类型类如`IllegalCharError`, `ExpectedCharError`, `InvalidSyntaxError`, `RTError`都继承这个类，分别在分析器的各阶段分析时，若出现错误则创建相应的错误类方法，同时返回。

`Error` 基类的成员及方法如下：
|  成员变量或方法   | 功能  |
|  :--:  | :--:  |
| pos_start | 错误开始位置 |
| pos_end | 错误结束位置 |
| error_name | 错误类型名称 |
| details | 错误描述 |
| as_string() | 格式化输出字符串 |

代码实现细节如下：

```Python
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return result
```

各类型的子类实现细节在附件源码中可以查看。

#### 2.6 符号表 SymbolTable

符号表用与保存每条语句执行结果，例如保存标识符内容，其核心成员变量是一个字典，数据结构定义如下：
```Python
class SymbolTable:
    def __init__(self, parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
```

值的一提的是，对于函数调用，其函数内部所定义的变量都是临时变量，这些变量与主程序不共享，故在解释执行函数时，需要新建一个符号表，保存部分上下文。

```Python
# interpreter/function BaseFunction class
def generate_new_context(self):
	new_context = Context(self.name, self.context, self.pos_start)
	new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
	return new_context
```

### 3. 输入输出形式
类似一个解释器的两种方法，程序输入方式可以是命令行单条输入，也可以是通过实现的内置函数库`RUN`方法输入文件批量处理。

输出是依次词法分析（TOEKN）、语法分析（语法树）、解释执行（运算结果）阶段返回的结果。

以`VAR a = 3 + 4`为例，输出格式形式如下。

- 词法分析输出格式：返回识别单词Token类型。上述表达式 Token 输出形式为：`[KEYWORD:VAR, IDENTIFIER:a, EQ, INT:3, PLUS, INT:4, EOF]`，`VAR`为关键字，`a`是标识符，`=`是`EQ`赋值运算符，3 和 4 识别为 `INT`，+识别为`PLUS`运算符，EOF代表结束。
- 语法分析输出格式：返回表达式的语法树，上述表达式的语法树输出形式为：`[IDENTIFIER:a, EQ, (INT:3, PLUS, INT:4)]`，表示如下内容

<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/ast.png" alt="1" style="zoom:50%;" />
- 解释执行输出格式：直接返回运算结果，这里是`7`

程序执行如下图：

<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/program1.png" alt="1" style="zoom:50%;" />

### 4. 程序运行结果

更多程序运行示例在附件`demo/xxx.demo`中，`doc/grammar_example.txt`也有该类Basic语言的语句使用方式描述。

这里给出部分例子。

#### 4.1 IF 分支条件
如下这里将中间过程Token、AST、结果均输出了出来，FOR、WHILE 等循环程序表达式过长导致语法树较长，观察不直观

后续运行结果展示中，将直接展示解释器执行结果。

<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/if1.png" alt="1" style="zoom:50%;" />

#### 4.2. FOR 循环
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/for1.png" alt="1" style="zoom:50%;" />

上述程序，第二条 FOR 语句输出的`[1, 2, 6, 24]`，是循环过程中每次的结果值，`result`结果值是24，`PRINT(result)`输出`result`并返回函数调用结果值，0表示成功返回。

while 循环类似，这里不再给出。

#### 4.3 求最小值程序
`demo/min.demo`是一个求最小值程序，内容如下
```Basic
VAR a = [5, 4, 3, 7, 2]

FUN MIN(array)
  VAR RES = array/0;

  FOR i = 0 TO LEN(a) THEN
    IF a/i < RES THEN
      VAR RES = a/i
    END
  END

  RETURN RES
END

PRINT(MIN(a))
```

该程序定义了一个数组`a`，`a/i`语法表示获取数组`a`下标为 `i` 的元素值，求得最小值并打印输出。

该程序解释执行结果如下图，运行结果为2，程序返回值为 0，表示成功运行。

<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/min.png" alt="1" style="zoom:50%;" />

#### 4.4 错误分析提示
##### 4.4.1 词法分析阶段错误
非法字符提示如下
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error1.png" alt="1" style="zoom:50%;" />

不完整字符提示如下
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error2.png" alt="1" style="zoom:50%;" />

##### 4.4.2 语法分析阶段错误
缺少关键字
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error3.png" alt="1" style="zoom:50%;" />

缺少标识符
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error4.png" alt="1" style="zoom:50%;" />

##### 4.4.3 解释执行阶段错误
未定义变量
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error5.png" alt="1" style="zoom:50%;" />

除 0 错误
<img src="https://github.com/ZonePG/impl-basic-toy/tree/main/doc/img/error6.png" alt="1" style="zoom:50%;" />
