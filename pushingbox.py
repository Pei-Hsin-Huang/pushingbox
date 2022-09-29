# 演算法分析機測
# 學號 : 10724243 / 10827101 / 10827145
# 姓名 : 石顥澐 / 林語潔 / 黃霈昕
# 中原大學資訊工程系

class PushingBoxGame:
    def __init__(self,mp, col, row):
        self.mp = mp
        self.col = col
        self.row = row
        # sta和en 表示開始 结束
        # sta只有2,4,0 2表示箱子起始位置,4表示人的位置,0表示其他
        # en只有1,3,0 1表示大石塊,3表示箱子结束位置,0表示其他
        # sta中的2位置移到en的3的位置即滿足條件
        self.sta = ''
        self.en = ''
        # px, py表示人的位置
        self.px,self.py = -1,-1
        # paths表最短路徑（可能有多條）
        self.paths = []
        # len表最短路徑長度
        self.len = -1

        self.pre() # 取得sta en px py
        self.BFS() # 取得最短路徑

        if ( len( self.paths ) == 0 ):
            print( 'Impossible' )

        else:
            min = self.paths[0]
            for p in self.paths:
                if ( len(p) < len(min) ): # 只印最小
                    min = p
            if ( min == '' ):
                print( 'Impossible' )
            else:
                print(min)

        print()

    def pre(self):
        # 取得sta en px py
        for i in range( len(self.mp) ):
            for j in range( len( self.mp[i] ) ):
                cx, cy = i, j
                if self.mp[i][j] == 'S':
                    self.px, self.py = cx, cy
        
        # 設定sta en
        staDic = {'.': '0', '#': '0', 'B': '2', 'T': '0', 'S': '4'}
        enDic = {'.': '0', '#': '1', 'B': '0', 'T': '3', 'S': '0'}
        for l in range( len(self.mp) ):
            for k in range( len( self.mp[l] ) ):
                self.sta += staDic[self.mp[l][k]]
                self.en += enDic[self.mp[l][k]]

    def is_ok(self,sta):
        # 是否能將箱子移到終點
        # sta中的2位置移到en的3的位置即滿足條件
        for s,e in zip(sta,self.en):
            if e == '3' and s != '2':
                return False

        return True

    def BFS(self):
        # BFS 取得最短路徑
        # 小寫代表只有人移動，大寫代表人推着箱子一起移動
        dirs = [[-1,0,'n','N'],[1,0,'s','S'],[0,1,'e','E'],[0,-1,'w','W']]
        # 目前sta、目前的路徑、目前人的位置
        states = [[self.sta,'',self.px,self.py]]
        # 走過的路徑不再走
        visi = {}
        visi[self.sta] = 1

        s_len = 1000
        while len(states)>0:
            sta, path, px, py = states[0]
            ppos = px*self.col + py # 人的位置
            states = states[1:]
            if len(path)>s_len:
                break

            # 保存最短路徑到paths中
            if self.is_ok(sta):
                if self.len == -1 or len(path) == self.len:
                    self.paths.append(path)
                    self.len = len(path)
                continue

            for dir in dirs:
                # 人要移動到的位置
                cx, cy = px + dir[0], py + dir[1]
                pos = cx*self.col+cy
                # 人要移動到的位置的周圍
                nx, ny = px + 2*dir[0], py + 2*dir[1]
                npos = nx*self.col+ny
                # 到邊邊
                if not (nx>=0 and nx<self.row and ny>=0 and ny<self.col ):
                    if ( pos >= 0 ) and ( pos < len(sta) ):
                        if sta[pos] == '0' and self.en[pos] !='1':
                            # 只有人動，sta中人 空格，要走到的位置不能是石塊
                            digits = [int(x) for x in sta]
                            digits[ppos], digits[pos] = 0, 4
                            new_sta = ''.join(str(x) for x in digits) # 更新後的sta
                            if new_sta not in visi:
                                visi[new_sta] = 1
                                states.append([new_sta, path + dir[2], cx, cy])
                    continue

                if sta[pos] == '2' and sta[npos] == '0' and self.en[npos] != '1':
                    # 人和箱子一起推動，sta中為人 箱子 空格，要推到的位置不能是大石塊。推完之后sta變空格 人 箱子
                    digits = [int(x) for x in sta]
                    digits[ppos],digits[pos],digits[npos] = 0,4,2
                    new_sta = ''.join(str(x) for x in digits) # 更新後的sta
                    if new_sta not in visi:
                        visi[new_sta] = 1
                        states.append([new_sta, path+dir[3], cx, cy])

                elif sta[pos] == '0' and self.en[pos] !='1':
                    # 只有人動，sta中人 空格，要走到的位置不能是石塊
                    digits = [int(x) for x in sta]
                    digits[ppos], digits[pos] = 0, 4
                    new_sta = ''.join(str(x) for x in digits) # 更新後的sta
                    if new_sta not in visi:
                        visi[new_sta] = 1
                        states.append([new_sta, path + dir[2], cx, cy])

if __name__ == '__main__':
    cmd = input().split()
    if ( len(cmd) == 2 ):
        r = int( cmd[0] )
        c = int( cmd[1] )
    else:
        print( 'There should be exactly two numbers' )
        r = 0
        c = 0

    mNum = 0
    while(r != 0) or (c != 0):
        mp = []
        mp.clear()
        if ( (r > 0) and (r <= 20) and (c > 0) and (c <= 20) ):
            error = False
            i = 0
            while( (i < r) and (error == False) ):
                l = input().strip()
                if ( len(l) != c ):
                    error = True
                    print( 'There must be c characters' )
                else:
                    for j in range( len(l) ):
                        if not ( l[j] == 'S' or l[j] == 'B' or l[j] == 'T' or l[j] == '#' or l[j] == '.' ):
                            error = True
                            print( 'error character' )

                mp.append( l )
                i = i + 1

            if ( error == False ):
                mNum = mNum + 1
                print( 'Maze #', mNum )
                g = PushingBoxGame( mp, c, r )
            else:
                print()

        else:
            print( 'r and c should greater than 0 and less than 20' )

        cmd = input().split()
        if ( len(cmd) == 2 ):
            r = int( cmd[0] )
            c = int( cmd[1] )
        else:
            print( 'There should be exactly two numbers' )
            r = 0
            c = 0

