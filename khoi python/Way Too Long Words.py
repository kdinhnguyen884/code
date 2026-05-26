a = int(input())
ket_qua = []
for _ in range(a) :
  b = input()
  if len(b) < 11:
    ket_qua.append(b)
  else :
    ket_qua.append(f"{b[0]}{len(b) -2}{b[-1]}")
for tu in ket_qua :
  print(tu)
