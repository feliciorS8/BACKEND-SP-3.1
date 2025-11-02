def read_data(path):
     with open (path, 'rt') as file:
         for line in file:
                print(line.replace("\n",""))
                
                
                #fungsi read data  untuk baca pada artikel.txt