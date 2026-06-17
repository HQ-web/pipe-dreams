if __name__ == "__main__":
    letter_labels = ( 
        'a', 'b', 'c', 'd', 
        'e', 'f', 'g', 'h', 
        'i', 'j', 'k', 'l', 
        'u', 'v', 'w', 'x', 
        'y', 'z'
         )
    pipe_labels = [ (a+str(b), a + '_' + str(b)) for a in letter_labels for b in range(0,10) ]

    latex_base = """
\\documentclass{standalone}
\\begin{document}
   {\\LARGE$-LABEL-$}
\\end{document}
"""
    for pl in pipe_labels:
        filebase = pl[0]
        label = pl[1]
        stamp = latex_base.replace("-LABEL-", label)
        with open(filebase+'.tex','w') as fd:
            print(stamp, file=fd)


