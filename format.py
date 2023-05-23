import os

def main():
    try:
        files = os.listdir('raw/')
        for fileName in files:
            rawFile = open('raw/'+fileName, 'r')
            title = ' '.join((map(lambda word: word.capitalize(), fileName.split('-'))))
            formattedFile = open('formatted/'+fileName+".tex", 'w')

            # Initialize formatted file with title.
            formattedFile.write("\\section{{{0}}}\n".format(title))

            prevLine = False
            for line in rawFile:
                if(line == "\n"):
                    # Cuts gaps to at most 1 linebreak
                    if(prevLine):
                        formattedFile.write("\n\n")
                    prevLine = False
                else:
                    if(prevLine):
                        formattedFile.write("\\\\\n")
                    formattedFile.write(line.strip())
                    prevLine = True

            rawFile.close()
            formattedFile.close()

    except FileNotFoundError as e:
        print(e.strerror)

if __name__ == "__main__":
    main()