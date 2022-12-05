import sys

def removeSymbols(file):
  symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+", "|", "\\", "`", "~", "'", '"', "/", "?", ".", ",", ">", "<", ";", ":", "{", "}", "[", "]"]

  for symbol in symbols:
    file = file.replace(symbol, "")

  return file

def tokenize(file):
  file = file.lower()
  return file.split()

def removeStopwords(tokens):
  stopWords = ["a", "about", "actually", "almost", "also", "although", "always", "am", "an", "and", "any", "are", "as", "at", "became", "can", "each", "had", "has", "have", "may", "maybe", "whereas", "be", "become", "does", "either", "else", "hence", "me", "mine", "mine", "neither", "when", "where", "wherever", "whenever", "whether", "while", "whoever", "whose", "yes", "yet", "did", "i", "if", "in", "is", "it", "its", "might", "which", "will", "with", "within", "without", "could", "do", "for", "from", "how", "nor", "not", "of", "oh", "ok", "who", "whom", "would", "you", "your", "but", "by", "just", "must", "my", "must", "my", "why", "to", "were", "on" ,"our", "the"]
  return [x for x in tokens if x not in stopWords]

def removeCodeStopwords(tokens):
  stopWords = ["for", "while", "if", "else", "int", "float", "char", "main", "public", "static", "void", "def", "str", "import", "include", "<<", ">>", "\n", "\t", "switch", "case", "return", "bool", "=", "+", "-", "*", "/", "//", "#", "++", "--", "==", ";", "::"]
  return [x for x in tokens if x not in stopWords]

def preprocessing(file, mode):
  file = removeSymbols(file)
  tokens = tokenize(file)

  if mode == "code":
    tokens = removeCodeStopwords(tokens)
  else:
    tokens = removeStopwords(tokens)
  return tokens

def checkPlagiarism(originalFile, testFile):
  threshold = 40
  mode = "eng"

  # determine if given text is code
  codePhrases = ["#include", "String[] args", "import java.", 'if __name__=="__main__"', "input(", "elif"]
  for phrase in codePhrases:
    if phrase in testFile:
      threshold = 18
      mode = "code"
      break

  if len(originalFile) == 0 or len(testFile) == 0:
    return 0
  else:
    testFileTokens = list(set(preprocessing(testFile, mode)))
    
    if len(testFileTokens) > 150: threshold += 10

    if len(testFileTokens) > 1000: threshold += 10
    
    matchCount = 0
    matches = []
    for token in testFileTokens:
      if token in originalFile:
        matchCount += 1
        matches.append(token)

    result = round(matchCount/len(testFileTokens)*100, 2) > threshold
    return int(result)

if __name__ == "__main__":
  # "../data/plagiarism01/1.txt"
  try:
    originalFile = sys.argv[1]
    testFile = sys.argv[2]
  except IndexError: 
    print("Enter file path")
    exit()

  originalFile = open(originalFile, "r").read()
  testFile = open(testFile, "r").read()

  print(checkPlagiarism(originalFile, testFile))
