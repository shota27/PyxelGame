#効果音については敵に当たった時に効果音がなる
import pyxel
import random

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER=2
SCENE_GAMECLEAR=3

class Dragon:
    #初期化
    def __init__(self):
        self.x = pyxel.rndi(30, 100)
        self.y = 10
        self.life=3
        self.dragon_x_list=[-1,0]
        self.random = pyxel.rndi(1,2)
        print("random",self.random)
        if self.random<=2:
            print("type2",self.random)
            self.type=1
        elif self.random > 2:
            print("type1",self.random)
            self.type=2
        
      
    #敵役を動かす関数
    def move(self):
        #敵によってスコアが変わる
        if self.type==1:
            self.y+=3
        elif self.type==2:
            self.y+=3

        
        if self.y >= 210:
            self.x = pyxel.rndi(70, 100)
            self.y=10
            self.type = pyxel.rndi(1, 2)
    
               
    #敵役を書く関数
    def draw(self):
   
        self.x+=random.choice(self.dragon_x_list)
        
        if self.type == 1:
            pyxel.blt(self.x,self.y,0,16,16,16,16)
        elif self.type == 2:
            pyxel.blt(self.x,self.y,0,32,16,16,16)
      
        
# キャラクターのクラスを作成
class Player:
    #初期化
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # x,yの変化量と、全体の移動量
        self.dx = 0
        self.dy = 0
        self.move_count = 0

        self.vector=0
        self.plot_player_x_coordinate=0
        self.dragon=Dragon()
        

    # x,yの変化量分x,yを増減させる関数
    def move(self):
        self.x += self.dx
        self.y += self.dy
        #print("x座標",self.x,"y座標",self.y)
    
    #敵に当たった時にスコアを引く部分  Appクラスのupdatemoveで呼び出し
    def catch(self,dragon):
        #dragonの左右10の範囲にプレイヤーのx座標がある時を判定
        if dragon.x-8<self.x and  dragon.x+8>self.x:
                  if dragon.y-2<self.y and dragon.y+2>self.y:
                      return True



    


class App:
    def __init__(self):
        pyxel.init(128, 128)

        pyxel.load("resource.pyxres")
        pyxel.sound(0).set("c3e3g3c4c4", "s", "6", "n", 5)
        

        
        # Playerクラスのインスタンスを生成、初期位置の座標を引数に渡す
        self.player = Player(112,112 )
        self.dragon=Dragon()
        self.score = 50
        self.reset()

        self.u=0
        self.v=16
        self.scene = SCENE_TITLE
        pyxel.run(self.draw, self.update)



    def reset(self):
        self.dragon=Dragon()
        self.player=Player(112,112)
        self.score=50

    
    #画面遷移
    def update(self):
        #初めはタイトル画面
        if self.scene == SCENE_TITLE:
            
            print("SCENE")
            self.update_title_scene()
        #プレイ画面の動作
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene==SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene==SCENE_GAMECLEAR:
            self.update_gameclear_scene()

    #sceneに関する関数
    # タイトル画面の処理
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    # プレイ画面におけるに関する情報を更新する関数
    def update_play_scene(self):
        self.dragon.move()
        self.player.move()
        
        #catchに当てはまるならscoreを変更
        if self.player.catch(self.dragon):
            pyxel.play(0, 0)
            if self.dragon.type==1:
                
                self.score-=20
            elif self.dragon.type==2:
                
                self.score-=30

        #スコアが0になったらgameover
            if self.score<0:
                self.scene=SCENE_GAMEOVER
        
        #ゴール地点でクリア画面に遷移 　プレイヤーのx座標が0になるのは一箇所なためy座標は入れず簡潔にした
        if self.player.x==0:
            self.scene=SCENE_GAMECLEAR
        

        pyxel.text(5, 5, "SCORE:" + str(self.score), 7)
        

        # 移動量が0であれば、キー入力があるか判定する
        if self.player.move_count == 0:
            if pyxel.btn(pyxel.KEY_LEFT):
                
                self.u=16
                self.v=32
                self.player.dx = -0.5
                
            
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.u=32
                self.v=32
                self.player.dx = 0.5
            
            elif pyxel.btn(pyxel.KEY_UP):
                self.u=0
                self.v=16
                self.player.dy = -0.5
            
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.u=0
                self.v=32
                self.player.dy = 0.5

            # キー入力がありx,yの変化量がセットされれば、移動量16をセット
            if self.player.dx != 0 or self.player.dy != 0:
                self.player.move_count = 16
            print(pyxel.tilemap(0).pget(
                    self.player.x / 8 + self.player.dx ,   
                    self.player.y / 8 + self.player.dy ))
            # 移動先が壁であれば、各変数を0にして移動をキャンセル
            if pyxel.tilemap(0).pget(
                    self.player.x / 8 + self.player.dx*2 ,   
                    self.player.y / 8 + self.player.dy *2 )== (5,0) or pyxel.tilemap(0).pget(
                    self.player.x / 8 + self.player.dx*2 ,   
                    self.player.y / 8 + self.player.dy *2 )== (4,0):

                self.player.dx = 0
                self.player.dy = 0
                self.player.move_count = 0

        # 移動量が0でなければ、移動中の状態
        else:
            # playerを移動させ、移動量を1減らす
            
            self.player.move_count -= 1

            # 移動量が0になったら移動終了、x,yの変化量をリセットする
            if self.player.move_count == 0:
                self.player.dx = 0
                self.player.dy = 0
    
    def update_gameover_scene(self):
      if self.scene==SCENE_GAMEOVER:  
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            self.scene=SCENE_PLAY
    
    def update_gameclear_scene(self):
        if self.scene==SCENE_GAMECLEAR:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset()
                self.scene= SCENE_PLAY

    def draw(self):
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene==SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene==SCENE_GAMECLEAR:
            self.draw_gameclear_scene()

    #ここからはdraw内で分岐で呼びだされるdraw_title_sceneなどの関数
    #タイトル画面の描画
    def draw_title_scene(self):
        pyxel.cls(0)
        pyxel.text(43, 50, "MEIRO GAME", 7)
        pyxel.text(35, 70, "- PRESS ENTER -", 6)

    #Appを書く関数
    def draw_play_scene(self):
        
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 256 ,256)
        pyxel.blt(self.player.x, self.player.y, 0, self.u, self.v, 8, 8)
        self.dragon.draw()
    
    def draw_gameclear_scene(self):
        pyxel.cls(0)
        pyxel.text(43,50,"GAME CLEAR",7)
        pyxel.text(30,70,"CONGRATULATIONS!",6)
        pyxel.text(35,90,"- PRESS ENTER -",6)

    def draw_gameover_scene(self):
        pyxel.cls(0)
        pyxel.text(46,50,"GAME OVER",7)
        pyxel.text(25,70,"- PRESS R TO RESTART -",6)

    
App()
