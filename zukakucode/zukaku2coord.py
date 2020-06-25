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
#  るので一旦公開します。→修正してちょっとマシになった
#  エラー処理は入れていないので、実行時は正しいコードを与えてください:-)
#  
#  図郭の説明： https://club.informatix.co.jp/?p=1293
#
#  2020/06/24 @sakaik :initial version (trial)
#  2020/06/25 @sakaik :refactoring and ..
#

import argparse

class OPT:
  verbose_mode=False
  ofmt=""
  
class ZUKAKU_INFO:
  tateKms = {"50000":30000, "5000":3000, "2500":1500, "1000":600, "500":300}
  yokoKms = {"50000":40000, "5000":4000, "2500":2000, "1000":800, "500":400}
  
  def __init__(self):
    self.zukakucode = ""
    
  @classmethod
  def setZukakuCode(self, code):
    tate50Kmesh = "ABCDEFGHIJKLMNOPQRST"
    yoko50Kmesh = "ABCDEFGH"
    yoko1000mesh = "ABCDE"
    #
    self.zukakucode = code
    self.level = self.mapLevel(self,code)
    self.kei = code[0:2]
    def getOne(code, n):
      return code[n:n+1]
    def getOneInt(code, n):
      return int(getOne(code,n))
    
    #50000
    self.code50Ktop = (tate50Kmesh.find(getOne(code,2))-10) * self.tateKms["50000"] * -1
    self.code50Kleft = (yoko50Kmesh.find(getOne(code,3))-4) * self.yokoKms["50000"] 
    self.totaltop = self.code50Ktop
    self.totalleft = self.code50Kleft
    #5000
    if (self.level <= "5000"):
      self.code5000top  = getOneInt(code,4) * self.tateKms["5000"]
      self.code5000left  = getOneInt(code,5) * self.yokoKms["5000"]
      self.totaltop = self.code50Ktop - self.code5000top
      self.totalleft = self.code50Kleft + self.code5000left
    #2500
    if (self.level == "2500"):
      self.code2500top  = math.floor( (getOneInt(code,6)-1) /2) * self.tateKms["2500"]
      self.code2500left = math.floor( (getOneInt(code,6)+1) %2) * self.yokoKms["2500"]
      self.totaltop = self.code50Ktop - self.code5000top - self.code2500top
      self.totalleft = self.code50Kleft + self.code5000left + self.code2500left
    #1000
    if (self.level == "1000"):
      self.code1000top  = getOneInt(code,6) * self.tateKms["1000"]
      self.code1000left = yoko1000mesh.find(getOne(code,7)) * self.yokoKms["1000"]
      self.totaltop = self.code50Ktop - self.code5000top - self.code1000top 
      self.totalleft = self.code50Kleft + self.code5000left + self.code1000left
    #500
    if (self.level == "500"):
      self.code500top  = getOneInt(code,6) * self.tateKms["500"]
      self.code500left = getOneInt(code,7) * self.yokoKms["500"]
      self.totaltop = self.code50Ktop - self.code5000top - self.code500top 
      self.totalleft = self.code50Kleft + self.code5000left + self.code500left
      
    self.totalbottom = self.totaltop  - self.tateKms[self.level]
    self.totalright  = self.totalleft + self.yokoKms[self.level]
    
  def mapLevel(self, code):
    length_levels = {4: "50000", 6:"5000", 7:"2500", 8:"nd"}  #nd: did not determined
    level = length_levels[len(code)];
    if (level=="nd"):
      if (code[7:8].isnumeric()):
        return "500"
      else:
        return "1000"
    return level
    
  
opt=OPT

def main():
  zkinfo=ZUKAKU_INFO
  zkinfo.setZukakuCode (getZukakuCodeFromArgs())

  #----------
  if (opt.verbose_mode):
    print ("-------------")
    print (zkinfo.zukakucode)
    print ('maplevel: '+ zkinfo.level)
    print ('kei:      '+ zkinfo.kei)
    print ('topleft50K: ('+ str(zkinfo.code50Ktop) +","+str(zkinfo.code50Kleft)+")")
    print ('topleft5K: ('+ str(zkinfo.code5000top) +","+str(zkinfo.code5000left)+")")
    if (zkinfo.level == "2500"):
      print ('topleft2500: ('+ str(zkinfo.code2500top) +","+str(zkinfo.code2500left)+")")
    if (zkinfo.level == "1000"):
      print ('topleft1000: ('+ str(zkinfo.code1000top) +","+str(zkinfo.code1000left)+")")
    if (zkinfo.level == "500"):
      print ('topleft500: ('+ str(zkinfo.code500top) +","+str(zkinfo.code500left)+")")
    print ("-------------")
  #----------
  if (OPT.ofmt=="TAB"):
    print ("\t".join([zkinfo.zukakucode, zkinfo.kei, str(zkinfo.totaltop), str(zkinfo.totalleft),
                      str(zkinfo.totalbottom), str(zkinfo.totalright), 'level:'+ zkinfo.level]))
  else:
    print (zkinfo.zukakucode +' '+ zkinfo.kei +'kei:'+'('+ str(zkinfo.totaltop) +','+str(zkinfo.totalleft) +') - '+'('+ str(zkinfo.totalbottom) +','+ str(zkinfo.totalright)+')' + '  [level: '+ zkinfo.level+"]")
    
    
    
def  getZukakuCodeFromArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("zukakucode", help="zukaku code")
  parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
  parser.add_argument("-t", "--tab", help="output by tab separated", action="store_true")
  args = parser.parse_args()
  zukakucode = args.zukakucode
  if args.verbose:
    OPT.verbose_mode = True
  if args.tab:
    OPT.ofmt = "TAB"

  return zukakucode
  
  
  
main()
