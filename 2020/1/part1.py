
if __name__=="__main__":
  inputs = set([int(line.strip()) for line in open("./input.txt")])
  for n in inputs:
    target = 2020 - n
    if target in inputs:
      print(target * n)
      break
  
