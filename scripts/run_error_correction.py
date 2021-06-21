import configparser
from corrector import Corrector
    
def main():
    path_to_file = './dictionary/corpus.txt'
    f = open(path_to_file, encoding = 'utf-8', mode = "r")

    corrector = Corrector()

    while True:
        line = f.readline()
    
        if not line:
            break

        line = line.split(",")
        entry = {}
        entry['doc'] = line[0]
        entry['page'] = int(line[1])
        entry['content'] = ','.join(line[2:])

        corrector.correct(entry)
    
    f.close()
    
if __name__ == '__main__':
    main()
