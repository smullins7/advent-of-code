
def find_counterpart(total, inputs):
  for n in inputs:
    target = total - n
    if target in inputs:
      return n, target

  return None, None

if __name__=="__main__":
  inputs = set([int(line.strip()) for line in open("./input.txt")])
  for n in inputs:
    target = 2020 - n
    a, b = find_counterpart(target, inputs)
    if a and b:
      print(f"{n} * {a} * {b} = {n*a*b}")
      break
