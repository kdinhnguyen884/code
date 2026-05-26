# calculator_ply.py

import ply.lex as lex
import ply.yacc as yacc

# =================================================================
# PHẦN 1: LEXER (Phân Tích Từ Vựng)
# =================================================================

# 1. Định nghĩa các tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'LPAREN',  # Dấu ngoặc mở (
    'RPAREN',  # Dấu ngoặc đóng )
)

# 2. Các luật đơn giản (dùng Biểu thức chính quy)
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# 3. Luật phức tạp hơn cho NUMBER (Chuyển đổi thành số nguyên)
def t_NUMBER(t):
    r'\d+'
    # Chuyển chuỗi số thành kiểu số nguyên (int)
    t.value = int(t.value)
    return t

# 4. Bỏ qua (ignore) các ký tự không quan trọng
t_ignore = ' \t'

# 5. Xử lý lỗi Lexer (Ký tự bất hợp lệ)
def t_error(t):
    print(f"Lỗi Lexer: Ký tự bất hợp lệ '{t.value[0]}' tại vị trí {t.lexpos}")
    t.lexer.skip(1)

# Xây dựng Lexer
lexer = lex.lex()

# =================================================================
# PHẦN 2: PARSER (Phân Tích Cú Pháp)
# =================================================================

# Sử dụng danh sách tokens đã định nghĩa ở trên

# 1. Thiết lập độ ưu tiên toán tử (Độ ưu tiên Left-Associative)
precedence = (
    # PLUS và MINUS có cùng độ ưu tiên, thực hiện từ trái sang phải ('left')
    ('left', 'PLUS', 'MINUS'),
)

# 2. Quy tắc Ngữ pháp (Grammar Rules)
# p[0] là giá trị trả về của quy tắc, p[1], p[2], p[3] là các thành phần bên phải

# Quy tắc 1: Biểu thức cộng hoặc trừ
def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
    '''
    # p[2] là toán tử (+ hoặc -)
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

# Quy tắc 2: Biểu thức có dấu ngoặc
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    # p[0] bằng giá trị của biểu thức bên trong ngoặc (p[2])
    p[0] = p[2]

# Quy tắc 3: Biểu thức là một số (Điểm dừng)
def p_expression_number(p):
    'expression : NUMBER'
    # p[0] bằng giá trị số nguyên đã được Lexer xử lý
    p[0] = p[1]

# 3. Xử lý lỗi Parser (Lỗi cú pháp)
def p_error(p):
    if p:
        print(f"Lỗi cú pháp: Không khớp tại '{p.value}'")
    else:
        print("Lỗi cú pháp: Kết thúc file (EOF) không hợp lệ")

# Xây dựng Parser
parser = yacc.yacc()

# =================================================================
# PHẦN 3: Vòng lặp chính (Main Loop)
# =================================================================

if __name__ == '__main__':
    print("--- Máy tính đơn giản (PLY) ---")
    print("Nhập biểu thức (vd: 5 + (10 - 2)). Nhập 'quit' để thoát.")

    while True:
        try:
            s = input('>>> ')
            if s.lower() == 'quit':
                break
        except EOFError:
            break
        
        if not s:
            continue

        try:
            # Gọi Parser để phân tích và thực thi biểu thức
            result = parser.parse(s)
            print(f"Kết quả: {result}")
        except Exception as e:
            # Xử lý các lỗi xảy ra trong quá trình Parse (nếu cần)
            pass
