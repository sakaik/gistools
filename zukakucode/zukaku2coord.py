#!/usr/bin/python3
#  
#  zukaku2coord.py
#        引数で与えられた図郭コードから、平面直角座標系の
#        メッシュ情報に変換して返す。
#
#  2020/06/24 osgeojapan-discuss mailing list での岩崎さんの投稿を見て
#  試しに作ってみたもの。Pythonをよく分かっていない（見様見真似）のと、
#  一段階一段階、値の内容を確認しながら進めたので、無駄に変数にツッコん
#  でいるなど、恥ずかしいのですが、期待する結果は得られているように見え
#  るので一旦公開します。
#  動きの正当性が確認できれば、書き直したい・・・・
#  
#  図郭の説明： https://club.informatix.co.jp/?p=1293
#
#  2020/06/24 @sakaik :initial version (trial)
#

import argparse
import math
from decimal import *

class OPT:
  verbose_mode=False

class ZUKAKU_INFO:
  tateKms = {"50000":30000, "5000":3000, "2500":1500, "1000":600, "500":300}
  yokoKms = {"50000":40000, "5000":4000, "2500":2000, "1000":800, "500":400}
  tate50000mesh = "ABCDEFGHIJKLMNOPQRST"
  yoko50000mesh = "ABCDEFGH"
  yoko1000mesh = "ABCDE"
  def __init__(self):
    self.zukakucode = ""
    
  @classmethod
  def setZukakuCode(self, code):
    self.zukakucode = code
    self.level = self.mapLevel(self,code)
    self.kei = code[0:2]
    #50000
    self.code50000 = code[2:4]
    self.code50000tate = (self.code50000[0:1])
    self.code50000yoko = (self.code50000[1:2])
    self.code50000top = (self.tate50000mesh.find(self.code50000tate)-10) * self.tateKms["50000"] * -1
    self.code50000left = (self.yoko50000mesh.find(self.code50000yoko)-4) * self.yokoKms["50000"] 
    #5000
    if (self.level <= "5000"):
      self.code5000 = code[4:6]
      self.code5000tate = (self.code5000[0:1])
      self.code5000yoko = (self.code5000[1:2])
      self.code5000top  = int(self.code5000tate) * self.tateKms["5000"]
      self.code5000left  = int(self.code5000yoko) * self.yokoKms["5000"]
    #2500
    if (self.level == "2500"):
      self.code2500 = code[6:7]
      self.code2500top  = math.floor( (int(self.code2500)-1) /2) * self.tateKms["2500"]
      self.code2500left = math.floor( (int(self.code2500)+1) %2) * self.yokoKms["2500"]
    #1000
    if (self.level == "1000"):
      self.code1000 = code[6:8]
      self.code1000tate = (self.code1000[0:1])
      self.code1000yoko = (self.code1000[1:2])
      self.code1000top  = int(self.code1000tate) * self.tateKms["1000"]
      self.code1000left = self.yoko1000mesh.find(self.code1000yoko) * self.yokoKms["1000"]    #500
    if (self.level == "500"):
      self.code500 = code[6:8]
      self.code500tate = (self.code500[0:1])
      self.code500yoko = (self.code500[1:2])
      self.code500top  = int(self.code500tate) * self.tateKms["500"]
      self.code500left = int(self.code500yoko) * self.yokoKms["500"]
    #TOTAL
    if (self.level == "50000"):
      self.totaltop = self.code50000top
      self.totalleft = self.code50000left
    if (self.level == "5000"):
      self.totaltop = self.code50000top - self.code5000top
      self.totalleft = self.code50000left + self.code5000left
    if (self.level == "2500"):
      self.totaltop = self.code50000top - self.code5000top - self.code2500top
      self.totalleft = self.code50000left + self.code5000left + self.code2500left
    if (self.level == "1000"):
      self.totaltop = self.code50000top - self.code5000top - self.code1000top 
      self.totalleft = self.code50000left + self.code5000left + self.code1000left
    if (self.level == "500"):
      self.totaltop = self.code50000top - self.code5000top - self.code500top 
      self.totalleft = self.code50000left + self.code5000left + self.code500left
    self.totalbottom = self.totaltop  - self.tateKms[self.level]
    self.totalright  = self.totalleft + self.yokoKms[self.level]
    
  def mapLevel(self, code):
    if (len(code) == 4):
      return "50000"
    elif (len(code) == 6):
      return "5000"
    elif (len(code) == 7):
      return "2500"
    elif (len(code) == 8):
      if (code[7:8].isnumeric()):
        return "500"
      else:
        return "1000"
    else:
      return ""
  
opt=OPT

def main():
  zukakuinfo=ZUKAKU_INFO
  zukakuinfo.setZukakuCode (getZukakuCodeFromArgs())

  #----------
  if (opt.verbose_mode):
    print (zukakuinfo.zukakucode)
    print ('maplevel: '+ zukakuinfo.level)
    print ('kei:      '+ zukakuinfo.kei)
    print ('topleft50K: ('+ str(zukakuinfo.code50000top) +","+str(zukakuinfo.code50000left)+")")
    print ('topleft5K: ('+ str(zukakuinfo.code5000top) +","+str(zukakuinfo.code5000left)+")")
    if (zukakuinfo.level == "2500"):
      print ('topleft2500: ('+ str(zukakuinfo.code2500top) +","+str(zukakuinfo.code2500left)+")")
    if (zukakuinfo.level == "1000"):
      print ('topleft1000: ('+ str(zukakuinfo.code1000top) +","+str(zukakuinfo.code1000left)+")")
    if (zukakuinfo.level == "500"):
      print ('topleft500: ('+ str(zukakuinfo.code500top) +","+str(zukakuinfo.code500left)+")")
    print ("-------------")
  #----------

  print (zukakuinfo.zukakucode +' '+ zukakuinfo.kei +'kei:'+'('+ str(zukakuinfo.totaltop) +','+str(zukakuinfo.totalleft) +') - '+'('+ str(zukakuinfo.totalbottom) +','+ str(zukakuinfo.totalright)+')' + '  [level: '+ zukakuinfo.level+"]")
    
    
    
def  getZukakuCodeFromArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("zukakucode", help="zukaku code")
  parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
  args = parser.parse_args()
  zukakucode = args.zukakucode
  if args.verbose:
    OPT.verbose_mode = True

  return zukakucode
  
  
  
main()
