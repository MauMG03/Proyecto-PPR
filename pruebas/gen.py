# write on file
import os
import random
from itertools import combinations

def generate_test1(file_path, n, m):
    with open(file_path, 'w') as file:
        
        actores = []
        file.write("ACTORES = {")
        for i in range(n): 
            actores.append(f"Actor{i}")
            
            if i < n - 1:
                file.write(f"Actor{i}, ")
            else:
                file.write(f"Actor{i}")

        file.write("};\n")
        

        escenas = []
        file.write(f'Escenas =[')
        for i in range(n):
            escenas.append([])
            file.write('|')

            costo = (int(round(random.uniform(1, 20), 0)))

            for j in range(m):

                aux = random.choice([0,1])
                

                escenas[i].append(aux)
                file.write(f'{aux}')

                if j < m-1:
                    file.write(',')
                else:
                    file.write(f',{costo}\n\t\t  ')
                
        file.write('|];\n')


        duracion = []
        for i in range(m):
            duracion.append(int(round(random.uniform(1, 5), 0)))

        file.write(f"Duracion={duracion};")

def generate_test2(file_path, n, m):
    with open(file_path, 'w') as file:
        
        actores = []
        file.write("ACTORES = {")
        for i in range(n): 
            actores.append(f"Actor{i}")
            
            if i < n - 1:
                file.write(f"Actor{i}, ")
            else:
                file.write(f"Actor{i}")

        file.write("};\n")
        

        escenas = []
        file.write(f'Escenas =[')
        for i in range(n):
            escenas.append([])
            file.write('|')

            costo = (int(round(random.uniform(1, 20), 0)))

            for j in range(m):

                aux = random.choice([0,1])
                

                escenas[i].append(aux)
                file.write(f'{aux}')

                if j < m-1:
                    file.write(',')
                else:
                    file.write(f',{costo}\n\t\t  ')
                
        file.write('|];\n')


        duracion = []
        for i in range(m):
            duracion.append(int(round(random.uniform(1, 5), 0)))

        file.write(f"Duracion={duracion};\n")

        file.write("Disponibilidad = [")
        for i in range(n): 
            aux = (int(round(random.uniform(0, 50), 0)))

            if i < n - 1:
                file.write(f"|Actor{i}, {aux}\n\t\t\t\t  ")
            else:
                file.write(f"|Actor{i}, {aux}|];\n")

        parejas = []
        for i in range(len(actores)):
            for j in range(i + 1, len(actores)):
                parejas.append((actores[i], actores[j]))

        k = random.randint(1, len(parejas))

        file.write("Evitar = [")
        for i in range(k):
            pareja = random.choice(parejas)
            parejas.remove(pareja)
            
            if i < k - 1:
                file.write(f"|{pareja[0]}, {pareja[1]}\n\t\t  ")
            else:
                file.write(f"|{pareja[0]}, {pareja[1]}|];\n")
            
generate_test2("./pruebas/parte2/Prueba20.dzn", 3, 20)
