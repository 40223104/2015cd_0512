#coding: utf-8
import struct
      
class StLFacet:
    def __init__(self, normal, v1, v2, v3, att_bc=0):
        self.coords = [normal, v1, v2, v3]
        self.att_bc = att_bc
  
class StL:
    def __init__(self, header):
        self.header = header
        self.facets = []
    def add_facet(self, facet):
        self.facets.append(facet)
    def get_binary(self):
        # 原先 2.0 的版本
        #out = ['%-80.80s' % self.header]
        # 改為 Python 3.0 格式
        # 第一行標頭的格式
        header = ['%-80.80s' % self.header][0]
        # 利用 bytes() 將標頭字串轉為二位元資料
        out = [bytes(header,encoding="utf-8")]
        # 接著則計算三角形面的數量, 並以二位元長整數格式存檔
        out.append(struct.pack('L',len(self.facets)))
        # 接著則依照法線向量與三個點座標的格式, 分別以浮點數格式進行資料附加
        for f in self.facets:
            for coord in f.coords:
                out.append(struct.pack('3f', *coord))
            # att_bc 則內定為 0
            out.append(struct.pack('H', f.att_bc))
        return b"".join(out)
  
def test():
    stl=StL('Header ...')
    stl.add_facet(StLFacet((0.,0.,1.),(0.,0.,0.),(1.,0.,0.),(0.,1.,0.)))
    stl.add_facet(StLFacet((0.,0.,1.),(1.,0.,0.),(1.,1.,0.),(0.,1.,0.)))
    # 第二個平面
    stl.add_facet(StLFacet((0.,-1.,0.),(0.,0.,0.),(0.,0.,-1.),(1.,0.,-1.)))
    stl.add_facet(StLFacet((0.,-1.,0.),(0.,0.,0.),(1.,0.,-1.),(1.,0.,0.)))
    return stl.get_binary()
  
# 指定存為 binary 格式檔案
stlfile = open("test.stl", "wb")
stlcontent = test()
stlfile.write(stlcontent)