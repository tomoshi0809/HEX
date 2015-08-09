#2015/08/09

#!/usr/bin/python
#coding: UTF-8
 
import wx
import math
import sys


class playPanel(wx.Panel):
    def __init__(self, parent, num_X, num_Y, size_x, size_y):
        self.num_X  = num_X   #X軸方向のセル数
        self.num_Y  = num_Y   #Y軸方向のセル数
        self.size_x = size_x  #フレームサイズ
        self.size_y = size_y
        wx.Panel.__init__(self, parent, size = (self.size_x, self.size_y))
        self.end_X  = 20   #端点（盤面最左点）の座標
        self.end_Y  = self.size_y / 2     #端点（盤面最左点）の座標
	self.player_flag = 1	#プレイヤーの手番を表す（赤：１，青：２）
        self.state = [[1 if i == 2 or j == 3 else 0 for j in range(self.num_X )] for i in range(self.num_Y )]  
	#セルの状態 state[i][j] i軸:1,2,3..., j軸: a,b,c.. 
	self.hex_vrtx   = [[[] for i in range(self.num_X)] for j in range(self.num_Y)]    #各セルの頂点の座標
	s = [[[30 * i + 30 * j, (-17) * i + 17 * j]for i in range(self.num_X )] for j in range(self.num_Y )]    #各セルの座標を定めるためのリスト
        xl = [0,10,30,40,30,10]
        yl = [0,17,17,0,-17,-17]
	for i in range(self.num_Y ):
		for j in range(self.num_X ):
			sx = self.end_X  + s[i][j][0] 
                	sy = self.end_Y  + s[i][j][1] 
			for k in range(6):
				self.hex_vrtx[i][j].append([sx + xl[k], sy + yl[k]])
       	
	self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN , self.on_click)
	#self.counter = 0

    def is_include(self, x,y,coordinates): #点(x,y)がcoordinatesで表される多角形に含まれるかを判定
        angle = 0
        for k in range(6):
            tmp = self.calc_tan(x,y,k,coordinates)
            angle += tmp

        if math.fabs(2 * math.pi - math.fabs(angle)) < 0.01:
            return True
        else:
            return False

    def calc_tan(self, x, y, k, coordinates ):  #多角形の辺と点との向き付き角度を計算する.
        Ax = coordinates [k][0] - x
        Ay = coordinates [k][1] - y
        Bx = coordinates [(k + 1) % 6][0] - x
        By = coordinates [(k + 1) % 6][1] - y
        AvB = Ax * Bx + Ay * By
        AxB = Ax * By - Ay * Bx
        angle = math.atan2(AxB,AvB)
        return(angle)

    def on_paint(self, Event=None):	#盤面の描画処理
	#print self.counter	
	#self.counter += 1	
	dc = wx.PaintDC(self)        
	dc.Clear()
        
        for i in range(self.num_Y ):
            for j in range(self.num_X ):
		dc.SetPen(wx.Pen(wx.BLACK, 2))
                if self.state[i][j] == 1:    #盤面をセルの状態に応じて塗る
                    dc.SetBrush(wx.Brush(wx.RED))
                elif self.state[i][j] == 2:
                    dc.SetBrush(wx.Brush(wx.BLUE))
                else:
                    dc.SetBrush(wx.Brush(wx.WHITE))
		
                polygon = tuple((self.hex_vrtx[i][j][k][0], self.hex_vrtx[i][j][k][1]) for k in range(6))
                dc.DrawPolygon(polygon)

	alphabet = [chr(i) for i in range(97,123)]
	for i in range(self.num_Y):	#盤面の端に，ゴールライン，座標を描画（赤）
		dc.SetPen(wx.Pen(wx.RED, 3))
		dc.DrawLine(self.hex_vrtx[i][0][0][0], self.hex_vrtx[i][0][0][1], self.hex_vrtx[i][0][1][0], self.hex_vrtx[i][0][1][1])
		dc.DrawLine(self.hex_vrtx[i][0][1][0], self.hex_vrtx[i][0][1][1], self.hex_vrtx[i][0][2][0], self.hex_vrtx[i][0][2][1])
		dc.DrawText(text = str(i), x = self.hex_vrtx[i][0][0][0] -10, y = self.hex_vrtx[i][0][0][1] + 10)
		dc.DrawLine(self.hex_vrtx[i][num_X - 1][3][0],self.hex_vrtx[i][num_X - 1][3][1], self.hex_vrtx[i][num_X - 1][4][0], self.hex_vrtx[i][num_X - 1][4][1])
		dc.DrawLine(self.hex_vrtx[i][num_X - 1][4][0], self.hex_vrtx[i][num_X - 1][4][1], self.hex_vrtx[i][num_X - 1][5][0], self.hex_vrtx[i][num_X - 1][5][1])
		dc.DrawText(text = str(i), x = self.hex_vrtx[i][num_X - 1][3][0], y = self.hex_vrtx[i][num_X - 1][3][1] - 20)
	
	for i in range(self.num_X):	#盤面の端に，ゴールライン，座標を描画（青）
		dc.SetPen(wx.Pen(wx.BLUE, 3))
		dc.DrawLine(self.hex_vrtx[0][i][4][0], self.hex_vrtx[0][i][4][1],self.hex_vrtx[0][i][5][0], self.hex_vrtx[0][i][5][1])
		dc.DrawLine(self.hex_vrtx[0][i][5][0], self.hex_vrtx[0][i][5][1], self.hex_vrtx[0][i][0][0], self.hex_vrtx[0][i][0][1])
		dc.DrawText(text = alphabet[i], x = self.hex_vrtx[0][i][0][0]-10, y = self.hex_vrtx[0][i][0][1] - 20)
		dc.DrawLine(self.hex_vrtx[num_Y - 1][i][1][0], self.hex_vrtx[num_Y - 1][i][1][1],self.hex_vrtx[num_Y - 1][i][2][0], self.hex_vrtx[num_Y - 1][i][2][1])
		dc.DrawLine(self.hex_vrtx[num_Y - 1][i][2][0], self.hex_vrtx[num_Y - 1][i][2][1], self.hex_vrtx[num_Y - 1][i][3][0], self.hex_vrtx[num_Y - 1][i][3][1])
		dc.DrawText(text = alphabet[i], x = self.hex_vrtx[num_Y - 1][i][3][0], y = self.hex_vrtx[num_Y - 1][i][3][1] + 10)
		
	
    def set_state(self, x,y):	#クリックした座標から，状態stateを更新
	flag = False	#多重ループbreak用フラグ
        for i in range(self.num_Y):
		if (self.hex_vrtx[i][0][0][0] < x < self.hex_vrtx[i][num_X - 1][3][0]) and (self.hex_vrtx[i][0][1][1] > y > self.hex_vrtx[i][num_X - 1][4][1]):
			for j in range(self.num_X):


			        if self.is_include(x,y,self.hex_vrtx[i][j]) and self.state[i][j] == 0:
					self.state[i][j] = self.player_flag
					print str(self.player_flag)+"["+str(i)+","+chr(97+j)+"]"
					self.player_flag = 1 + self.player_flag % 2
					flag = True
					break
			if flag:
				break

    def on_click(self, event): #クリック時のイベント
        pos = event.GetPosition()
        self.set_state(pos[0],pos[1])
        self.Refresh()

class MyWindow(wx.Frame):
	def __init__(self, num_X, num_Y):
		self.num_X  = num_X	#X軸方向のセル数
		self.num_Y  = num_Y	#Y軸方向のセル数
		self.size_x = 30 * ((self.num_X  + self.num_Y ) - 1) + 10  + 40 #フレームサイズ
		self.size_y = 17 * (self.num_X  + self.num_Y) + 50
		wx.Frame.__init__(self, None, title = "HEX", size = (self.size_x, self.size_y+30))    #Frame宣言
		self.pl = playPanel(parent = self, num_X = self.num_X, num_Y = self.num_Y, size_x = self.size_x, size_y = self.size_y)   #Panel 宣言
		self.button1 = wx.Button(self, -1, "Start")
		self.button2 = wx.Button(self, -1, "Reset")
		self.button1.Bind(wx.EVT_BUTTON, self.click_sbutton)
		self.button2.Bind(wx.EVT_BUTTON, self.click_rbutton)
		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz2 = wx.BoxSizer(wx.HORIZONTAL)
		sz2.Add(self.button1)
		sz2.Add(self.button2)
		sz1.Add(sz2)
		sz1.Add(self.pl)
		self.SetSizer(sz1)

	def click_sbutton(self, event):
		print "Start"     
	
	def click_rbutton(self, event):
		print "Reset"

if __name__ == '__main__':
    app = wx.App(False)
    num_X = 13
    num_Y = 13
    frame = MyWindow(num_X, num_Y)
    frame.Show()
    app.MainLoop()
