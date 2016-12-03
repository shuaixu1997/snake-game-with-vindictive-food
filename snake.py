import sys, time
import _thread
from random import randrange
from PyQt4 import QtGui, QtCore

class Snake(QtGui.QWidget):
        def __init__(self):
                super(Snake, self).__init__()
                self.initUI()

        def initUI(self):
                self.highscore2 = 0
                self.newGame()
                #self.setStyleSheet("QWidget { background: #B19F5D0}") 
                self.setFixedSize(300*3, 350*3)
                self.setWindowTitle('Snake')
                self.show()

        def paintEvent(self, event):
                qp = QtGui.QPainter()
                qp.begin(self)
                self.scoreBoard(qp)
                self.placeFood(qp)
                self.fakeFood(qp)
                self.drawSnake(qp)
                self.scoreText(event, qp)
                if self.isOver:
                        self.gameOver(event, qp)
                qp.end()

        def keyPressEvent(self, e):
                if not self.isPaused:
                        #print "inflection point: ", self.x, " ", self.y
                        if e.key() == QtCore.Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                                self.direction("UP")
                                self.lastKeyPress = 'UP'
                        elif e.key() == QtCore.Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
                                self.direction("DOWN")
                                self.lastKeyPress = 'DOWN'
                        elif e.key() == QtCore.Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
                                self.direction("LEFT")
                                self.lastKeyPress = 'LEFT'
                        elif e.key() == QtCore.Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
                                self.direction("RIGHT")
                                self.lastKeyPress = 'RIGHT'
                        elif e.key() == QtCore.Qt.Key_P:
                                self.pause()
                elif e.key() == QtCore.Qt.Key_P:
                        self.start()
                elif e.key() == QtCore.Qt.Key_Space:
                        self.newGame()
                elif e.key() == QtCore.Qt.Key_Escape:
                        self.close()

        def newGame(self):
                self.score = 0
                self.x = 12*3;
                self.y = 180*3;
                self.lastKeyPress = 'RIGHT'
                self.timer = QtCore.QBasicTimer()
                self.snakeArray = [[self.x, self.y], [self.x-12*3, self.y], [self.x-24*3, self.y]]
                self.foodx = 0
                self.foody = 0
                self.fakex =[0 for n in range(50)]
                self.fakey =[0 for n in range(50)]
                self.isPaused = False
                self.isOver = False
                self.FoodPlaced = False
                self.fakeflag = False
                self.tempflag = False
                self.speed = 85
                self.fakenumber = 0
                self.start()

        def pause(self):
                self.isPaused = True
                self.timer.stop()
                self.update()

        def start(self):
                self.isPaused = False
                self.timer.start(self.speed, self)
                self.update()

        def direction(self, dir):
                if (dir == "DOWN" and self.checkStatus(self.x, self.y+12*3)):
                        self.y += 12*3
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "UP" and self.checkStatus(self.x, self.y-12*3)):
                        self.y -= 12*3
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "RIGHT" and self.checkStatus(self.x+12*3, self.y)):
                        self.x += 12*3
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "LEFT" and self.checkStatus(self.x-12*3, self.y)):
                        self.x -= 12*3
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])

                #checkfakestatus        
                if (dir == "DOWN" and self.checkfake(self.x, self.y-12*3)):
                        self.y += 12*3
                        self.score -= 1
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "UP" and self.checkfake(self.x, self.y+12*3)):
                        self.y -= 12*3
                        self.score -= 1
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "RIGHT" and self.checkfake(self.x-12*3, self.y)):
                        self.x += 12*3
                        self.score -= 1
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                elif (dir == "LEFT" and self.checkfake(self.x+12*3, self.y)):
                        self.x -= 12*3
                        self.score -= 1
                        self.repaint()
                        self.snakeArray.insert(0 ,[self.x, self.y])
                        
        def scoreBoard(self, qp):
                qp.setPen(QtCore.Qt.NoPen)
                qp.setBrush(QtGui.QColor(245, 80, 0, 150))
                qp.drawRect(0, 0, 300*3, 72*3)

        def scoreText(self, event, qp):
                qp.setPen(QtGui.QColor(245, 245, 245))
                qp.setFont(QtGui.QFont('Decorative', 10*2))
                qp.drawText(8*3, 17*3, "SCORE: " + str(self.score))  
                qp.drawText(8*3, 54*3, "HIGHSCORE: " + str(self.highscore2))  

        def gameOver(self, event, qp):
                self.highscore2 = max(self.highscore2, self.score)
                qp.setPen(QtGui.QColor(0, 34, 3))
                qp.setFont(QtGui.QFont('Decorative', 10*2))
                qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER"+"\n"+"PRESS SPACE TO PLAY AGIAN")  
                      
        def checkStatus(self, x, y):
                
                if y > 338*3 or x > 288*3 or x < 0 or y < 64*3:
                        self.pause()
                        self.isPaused = True
                        self.isOver = True
                        return False
                elif self.score < 0:
                        self.pause()
                        self.isPaused = True
                        self.isOver = True
                        return False
                elif self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
                        self.pause()
                        self.isPaused = True
                        self.isOver = True
                        return False
                
                elif self.y == self.foody and self.x == self.foodx:
                        self.FoodPlaced = False
                        self.score += 1
                        self.fakeflag = False
                        self.fakenumber += 1
                        return True
                elif self.score >= 573*3:
                        print ("you win!")
                self.snakeArray.pop()
                return True
				
        def checkfake(self, x, y):
                for i in range(0,self.fakenumber+1):
                        if self.y == self.fakey[i] and self.x == self.fakex[i]:
                                return True
                return False
        
        #places the fake food 
        def fakeFood(self, qp):
                while self.fakeflag == False:
                        self.fakex[self.fakenumber] = randrange(24)*12*3
                        self.fakey[self.fakenumber] = randrange(6, 24)*12*3
                        self.fakeflag = True
                        for i in range(0,self.fakenumber+1):
                                if (self.foodx == self.fakex[i]) and (self.foody == self.fakey[i]):
                                        self.fakeflag = False                        
                qp.setBrush(QtGui.QColor(80, 80, 0, 240))
                for i in range(0,self.fakenumber+1):
                        qp.drawRect(self.fakex[i], self.fakey[i],12*3,12*3)
                        

	#thread
        def timerEvent(self, event):
                if event.timerId() == self.timer.timerId():
                        self.direction(self.lastKeyPress)
                        self.repaint()
                else:
                        QtGui.QFrame.timerEvent(self, event)				
						
	#places the food when theres none on the board
        def placeFood(self, qp):
                while (self.tempflag == False) and (self.FoodPlaced == False):
                        self.foodx = randrange(24)*12*3
                        self.foody = randrange(6, 24)*12*3
                        if not [self.foodx, self.foody] in self.snakeArray:
                                self.tempflag = True
                        for i in range(0,self.fakenumber+1):
                                if (self.foodx == self.fakex[i]) and (self.foody == self.fakey[i]):
                                        self.tempflag = False
                self.FoodPlaced = True
                qp.setBrush(QtGui.QColor(80, 180, 0, 160))
                qp.drawRect(self.foodx, self.foody, 12*3, 12*3)
                self.tempflag = False

        #draws each component of the snake
        def drawSnake(self, qp):
                qp.setPen(QtCore.Qt.NoPen)
                qp.setBrush(QtGui.QColor(245, 180, 0, 245))
                for i in self.snakeArray:
                        qp.drawRect(i[0], i[1], 12*3, 12*3)

       

def main():
        app = QtGui.QApplication(sys.argv)
        ex = Snake()
        status = app.exec_()
        

if __name__ == '__main__':
        main()