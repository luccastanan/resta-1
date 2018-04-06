import os

class Game(object):

    base = 7
    dots = 32
    matrix = 0

    #Início
    def __init__(self):
        self.setup()
    
    #Inicializa matriz 
    def setup(self):
        #♦◊
        self.matrix = [[(-1 if ((i < 2 or i > 4) and (j < 2 or j > 4)) else 1 if not (
            i == 3 and j == 3) else 0) for j in range(self.base)] for i in range(self.base)]
        self.start()
    
    #Loop
    def start(self):
        while True:
            self.clear()
            self.adjust()
            if(self.won()):
                print("***GANHOU***")
                return
            elif(self.isFinished()):
                print("---PERDEU---\nRestaram {}".format(self.dots))
                return
                
            self.isFinished()
            init, end = 0, 0
            options = []
            while True:
                init = input("Mover a posição (i;j): ")
                options = self.optionsToMove(self.inpToPos(init))
                if(len(options) > 0):
                    break
                else:
                    print("POSIÇÃO INVÁLIDA")
            
            while True:
                end = input("Para a posição (i;j): ")
                if(init != end and (self.inpToPos(end) in options)):
                    self.move(init, end)
                    break
                else:
                    print("POSIÇÃO INVÁLIDA")
    
    #Verifica se ainda existe possíveis jogadas
    def isFinished(self):
        for i in range(len(self.matrix)):
            for j, val in enumerate(self.matrix[i]):
                if val == 1 and self.optionsToMove([i, j]):
                    return False
        return True

    #Verifica se venceu
    def won(self):
        return self.dots == 1

    #Obtêm posição possíveis para o movimento
    def optionsToMove(self, initPos):
        options = []
        #Se a posição é válida
        if (self.matrix[initPos[0]][initPos[1]] == 1):
            if(initPos[0] - 2 >= 0 and self.matrix[initPos[0]-2][initPos[1]] == 0):
                p = [initPos[0]-2, initPos[1]]
                eatPos = self.optionsToEat(initPos,p)
                if(self.matrix[eatPos[0]][eatPos[1]] == 1):
                    options.append(p)
            if(initPos[0] + 2 < len(self.matrix) and self.matrix[initPos[0]+2][initPos[1]] == 0):
                p = [initPos[0]+2, initPos[1]]
                eatPos = self.optionsToEat(initPos,p)
                if(self.matrix[eatPos[0]][eatPos[1]] == 1):
                    options.append(p)
            if(initPos[1] - 2 >= 0 and self.matrix[initPos[0]][initPos[1]-2] == 0):
                p = [initPos[0],initPos[1]-2]
                eatPos = self.optionsToEat(initPos,p)
                if(self.matrix[eatPos[0]][eatPos[1]] == 1):
                    options.append(p)
            if(initPos[1] + 2 < len(self.matrix[0]) and self.matrix[initPos[0]][initPos[1]+2] == 0):
                p = [initPos[0],initPos[1]+2]
                eatPos = self.optionsToEat(initPos,p)
                if(self.matrix[eatPos[0]][eatPos[1]] == 1):
                    options.append(p)
            return options

        return []

    #Cria matriz visual
    def adjust(self):
        result = [[x if x != 0 else ' ' for x in range(self.base + 1)]]
        #custom = [[' ' if x == -1 else '◊' if x == 0 else '♦' for x in i] for i in self.matrix]
        custom = [[' ' if x == -1 else '-' if x == 0 else 'O' for x in i] for i in self.matrix]
        i = 0
        while i < len(self.matrix):
            row = custom[i]
            result.append([chr(97 + i)] + row)
            i += 1
        self.show(result)
    
    #Printa matriz
    def show(self, matrixEnd):
        print("\n".join(' '.join([str(x) for x in i]) for i in matrixEnd))
    
    #Move
    def move(self, init, end):
        initPos = self.inpToPos(init)
        endPos = self.inpToPos(end)

        self.matrix[initPos[0]][initPos[1]] = 0
        self.matrix[endPos[0]][endPos[1]] = 1
        self.eat(initPos, endPos)
    
    #Come a peça
    def eat(self, initPos, endPos):
        pos = self.optionsToEat(initPos, endPos)
        self.matrix[pos[0]][pos[1]] = 0
        self.dots-=1

    #Obtêm a posição da peça a ser comida
    def optionsToEat(self, initPos, endPos):
        return [endPos[0], round((initPos[1] + endPos[1])/2)] if initPos[0] == endPos[0] else [round((initPos[0] + endPos[0])/2), endPos[1]]
    
    #Converte input para posição
    def inpToPos(self, inp):
        pos = inp.split(';')
        return [ord(pos[0]) - 97, int(pos[1]) - 1]  

    #Limpa terminal
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

g = Game()

