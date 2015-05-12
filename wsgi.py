# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝



import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random
import math
from cherrypy.lib.static import serve_file
# 導入 gear 模組
#import gear

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"


def downloadlist_access_list(files, starti, endi):
    # different extension files, associated links were provided
    # popup window to view images, video or STL files, other files can be downloaded directly
    # files are all the data to list, from starti to endi
    # add file size
    outstring = ""
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileExtension = fileExtension.lower()
        fileSize = sizeof_fmt(os.path.getsize(download_root_dir+"downloads/"+files[index]))
        # images files
        if fileExtension == ".png" or fileExtension == ".jpg" or fileExtension == ".gif":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # stl files
        elif fileExtension == ".stl":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/static/viewstl.html?src=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # flv files
        elif fileExtension == ".flv":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/flvplayer?filepath=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # direct download files
        else:
            outstring += "<input type='checkbox' name='filename' value='"+files[index]+"'><a href='/download/?filepath="+download_root_dir.replace('\\', '/')+ \
            "downloads/"+files[index]+"'>"+files[index]+"</a> ("+str(fileSize)+")<br />"
    return outstring
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Midterm(object):

    # Midterm 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
    @cherrypy.expose
    def index(self, N=20 ,N1=20 , M=4, P=20,midx=400):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <h1>cda_g2_w11 練習</h1>
    <h2>班級:四設計二甲    學號:40223104    姓名:林瑩禎</h2>

    <form method=POST action=index>

    <a href="spur">spur</a><br />
    <a href="drawspur">drawspur</a><br />
    <a href="fileuploadform">上傳檔案</a><br />
    <a href="download_list">列出上傳檔案</a><br />







    '''
        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def spur(self, N=20 , M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">


    <form method=POST action=spuraction>
    齒數:<input type=text name=N><br />
    模數:<input type=text name=M><br />
    壓力角:<input type=text name=P><br />
    <input type=submit value=send>

    </form>
    <hr>

    '''

        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def spuraction(self, N=20 , M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    齒數:'''+str(N)+'''<output name=N for=str(N)><br />
    模數:'''+str(M)+'''<output name=M for=str(M)><br />
    壓力角:'''+str(P)+'''<output name=P for=str(P)><br />
    '''

        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def drawspur(self, N=20, N1=10, N2=30, N3=10, N4=20, N5=30, N6=30,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <form method=POST action=drawspuraction>
    第1齒數:<input type=text name=N><br />
    第2齒數:<input type=text name=N1><br />
    第3齒數:<input type=text name=N2><br />
    第4齒數:<input type=text name=N3><br />
    第5齒數:<input type=text name=N4><br />
    第6齒數:<input type=text name=N5><br />
    第7齒數:<input type=text name=N6><br />
    模數:<input type=text name=M><br />
    壓力角:<input type=text name=P><br />
    <input type=submit value=send>

    </form>
    <hr>

    '''

        return outstring
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def drawspuraction(self, N=20, N1=10, N2=30, N3=10, N4=20, N5=30, N6=30,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    第1齒數:'''+str(N)+'''<output name=N for=str(N)><br />
    第2齒數:'''+str(N1)+'''<output name=N1 for=str(N1)><br />
    第3齒數:'''+str(N2)+'''<output name=N2 for=str(N2)><br />
    第4齒數:'''+str(N3)+'''<output name=N3 for=str(N3)><br />
    第5齒數:'''+str(N4)+'''<output name=N4 for=str(N4)><br />
    第6齒數:'''+str(N5)+'''<output name=N5 for=str(N5)><br />
    第7齒數:'''+str(N6)+'''<output name=N5 for=str(N6)><br />
    模數:'''+str(M)+'''<output name=M for=str(M)><br />
    壓力角:'''+str(P)+'''<output name=P for=str(P)><br />
    齒數比:'''+str(N)+''':'''+str(N1)+''':'''+str(N2)+''':'''+str(N3)+''':'''+str(N4)+''':'''+str(N5)+''':'''+str(N6)+'''<br />

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度
    pa = 20
    # m 為模數
    m = '''+str(M)+'''
    # 第1齒輪齒數
    n_g1 = '''+str(N)+'''
    # 第2齒輪齒數
    n_g2 = '''+str(N1)+'''
    # 第3齒輪齒數
    n_g3 ='''+str(N2)+'''
    # 第4齒輪齒數
    n_g4 ='''+str(N3)+'''
    # 第5齒輪齒數
    n_g5 ='''+str(N4)+'''
    # 第6齒輪齒數
    n_g6 ='''+str(N5)+'''
    # 第7齒輪齒數
    n_g7 ='''+str(N6)+'''



    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2
    rp_g5= m*n_g5/2
    rp_g6= m*n_g6/2
    rp_g7= m*n_g7/2

    # 繪圖第1齒輪的圓心座標
    x_g1 = 400
    y_g1 = 400
    # 第2齒輪的圓心座標, 假設排列成水平, 表示各齒輪圓心 y 座標相同
    x_g2 = x_g1 + rp_g1 + rp_g2
    y_g2 = y_g1
    # 第3齒輪的圓心座標
    x_g3 = x_g1 + rp_g1 + 2*rp_g2 + rp_g3
    y_g3 = y_g1

    # 第4齒輪的圓心座標
    x_g4 = x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 + rp_g4
    y_g4 = y_g1

    # 第5齒輪的圓心座標
    x_g5= x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 +2* rp_g4+ rp_g5
    y_g5 = y_g1

    # 第6齒輪的圓心座標
    x_g6= x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 +2* rp_g4+2* rp_g5+rp_g6
    y_g6= y_g1

    # 第7齒輪的圓心座標
    x_g7= x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 +2* rp_g4+2* rp_g5+2*rp_g6+rp_g7
    y_g7= y_g1


    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖

    ctx.font = "10px Verdana";
    ctx.fillText("組員:31",x_g1-20, y_g1-10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g1, y_g1)
    # rotate to engage
    ctx.rotate(pi/2)
    # put it back
    ctx.translate(-x_g1, -y_g1)
    spur.Spur(ctx).Gear(x_g1, y_g1, rp_g1, n_g1, pa, "blue")
    ctx.restore()

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合

    ctx.font = "10px Verdana";
    ctx.fillText("組員:04",x_g2-20, y_g2-10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g2, y_g2)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g2)
    # put it back
    ctx.translate(-x_g2, -y_g2)
    spur.Spur(ctx).Gear(x_g2, y_g2, rp_g2, n_g2, pa, "black")
    ctx.restore()

    # 將第3齒輪逆時鐘轉 90 度之後, 再往回轉第2齒輪定位帶動轉角, 然後再逆時鐘多轉一齒, 以便與第2齒輪進行囓合

    ctx.font = "10px Verdana";
    ctx.fillText("組員:07",x_g3-20, y_g3-10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g3, y_g3)
    # rotate to engage
    # pi+pi/n_g2 為第2齒輪從順時鐘轉 90 度之後, 必須配合目前的標記線所作的齒輪 2 轉動角度, 要轉換到齒輪3 的轉動角度
    # 必須乘上兩齒輪齒數的比例, 若齒輪2 大, 則齒輪3 會轉動較快
    # 第1個 -pi/2 為將原先垂直的第3齒輪定位線逆時鐘旋轉 90 度
    # -pi/n_g3 則是第3齒與第2齒定位線重合後, 必須再逆時鐘多轉一齒的轉角, 以便進行囓合
    # (pi+pi/n_g2)*n_g2/n_g3 則是第2齒原定位線為順時鐘轉動 90 度, 
    # 但是第2齒輪為了與第1齒輪囓合, 已經距離定位線, 多轉了 180 度, 再加上第2齒輪的一齒角度, 因為要帶動第3齒輪定位, 
    # 這個修正角度必須要再配合第2齒與第3齒的轉速比加以轉換成第3齒輪的轉角, 因此乘上 n_g2/n_g3
    ctx.rotate(-pi/2-pi/n_g3+(pi+pi/n_g2)*n_g2/n_g3)
    # put it back
    ctx.translate(-x_g3, -y_g3)
    spur.Spur(ctx).Gear(x_g3, y_g3, rp_g3, n_g3, pa, "red")
    ctx.restore()

    # 按照上面三個正齒輪的囓合轉角運算, 隨後的傳動齒輪轉角便可依此類推, 完成6個齒輪的囓合繪圖

    #第4齒輪

    ctx.font = "10px Verdana";
    ctx.fillText("組員:02",x_g4-20, y_g4-10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g4, y_g4)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g4+(pi+pi/n_g3)*n_g3/n_g4-(pi+pi/n_g2)*n_g2/n_g4)
    # put it back
    ctx.translate(-x_g4, -y_g4)
    spur.Spur(ctx).Gear(x_g4, y_g4, rp_g4, n_g4, pa, "green")
    ctx.restore()

    #第5齒輪

    ctx.font = "10px Verdana";
    ctx.fillText("組員:06",x_g5-20, y_g5+10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g5, y_g5)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g5+(pi+pi/n_g4)*n_g4/n_g5-(pi+pi/n_g3)*n_g3/n_g5+(pi+pi/n_g2)*n_g2/n_g5)
    # put it back
    ctx.translate(-x_g5, -y_g5)
    spur.Spur(ctx).Gear(x_g5, y_g5, rp_g5, n_g5, pa, "purple")
    ctx.restore()

    #第6齒輪

    ctx.font = "10px Verdana";
    ctx.fillText("組員:05",x_g6-20, y_g6+10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g6, y_g6)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g6+(pi+pi/n_g5)*n_g5/n_g6-
    (pi+pi/n_g4)*n_g4/n_g6+(pi+pi/n_g3)*n_g3/n_g6-
    (pi+pi/n_g2)*n_g2/n_g6)
    # put it back
    ctx.translate(-x_g6, -y_g6)
    spur.Spur(ctx).Gear(x_g6, y_g6, rp_g6, n_g6, pa, "blue")
    ctx.restore()

    #第7齒輪

    ctx.font = "10px Verdana";
    ctx.fillText("組員:40023107",x_g7-20, y_g7+10);

    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g7, y_g7)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g7+(pi+pi/n_g6)*n_g6/n_g7-
    (pi+pi/n_g5)*n_g5/n_g7+(pi+pi/n_g4)*n_g4/n_g7-
    (pi+pi/n_g3)*n_g3/n_g7+(pi+pi/n_g2)*n_g2/n_g7)
    # put it back
    ctx.translate(-x_g7, -y_g7)
    spur.Spur(ctx).Gear(x_g7, y_g7, rp_g7, n_g7, pa, "Brown")
    ctx.restore()

    </script>
    <canvas id="plotarea" width="3000" height="3000"></canvas>
    </body>
    </html>
    '''

        return outstring
    '''

    # 第5齒輪的圓心座標
    x_g5= x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 +2* rp_g4+ rp_g5
    y_g5 = y_g1

    # 第6齒輪的圓心座標
    x_g6= x_g1 + rp_g1 + 2*rp_g2 + 2* rp_g3 +2* rp_g4+2* rp_g5+rp_g6
    y_g6= y_g1

    #第5齒輪
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g5, y_g5)
    # rotate to engage
    ctx.rotate(-pi-pi/n_g5+(pi+pi/n_g4)*n_g4/n_g5)
    # put it back
    ctx.translate(-x_g5, -y_g5)
    spur.Spur(ctx).Gear(x_g5, y_g5, rp_g5, n_g5, pa, "purple")
    ctx.restore()

    #第6齒輪
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x_g6, y_g6)
    # rotate to engage
    ctx.rotate(-pi/2-pi/n_g6-pi/n_g6+(pi+pi/n_g5)*n_g5/n_g6)
    # put it back
    ctx.translate(-x_g6, -y_g6)
    spur.Spur(ctx).Gear(x_g6, y_g6, rp_g6, n_g6, pa, "blue")
    ctx.restore()
    '''
    @cherrypy.expose
    # W 為正方體的邊長
    def cube(self, W=10):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    </head>
    <body>
    <!-- 使用者輸入表單的參數交由 cubeaction 方法處理 -->
    <form method=POST action=cubeaction>
    正方體邊長:<input type=text name=W value='''+str(W)+'''><br />
    <input type=submit value=送出>
    </form>
    <br /><a href="index">index</a><br />
    </body>
    </html>
    '''

        return outstring
    @cherrypy.expose
    # W 為正方體邊長, 內定值為 10
    def cubeaction(self, W=10):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 先載入 pfcUtils.js 與 wl_header.js -->
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    document.writeln ("Error loading Pro/Web.Link header!");
    </script>
    <script>
    window.onload=function(){
    brython();
    }
    </script>
    </head>
    <!-- 不要使用 body 啟動 brython() 改為 window level 啟動 -->
    <body onload="">
    <h1>Creo 參數化零件</h1>
    <a href="index">index</a><br />

    <!-- 以下為 Creo Pro/Web.Link 程式, 將 JavaScrip 改為 Brython 程式 -->

    <script type="text/python">
    from browser import document, window
    from math import *

    # 這個區域為 Brython 程式範圍, 註解必須採用 Python 格式
    # 因為 pfcIsWindows() 為原生的 JavaScript 函式, 在 Brython 中引用必須透過 window 物件
    if (!window.pfcIsWindows()) window.netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    # 若第三輸入為 false, 表示僅載入 session, 但是不顯示
    # ret 為 model open return
    ret = document.pwl.pwlMdlOpen("cube.prt", "v:/tmp", false)
    if (!ret.Status):
        window.alert("pwlMdlOpen failed (" + ret.ErrorCode + ")")
        # 將 ProE 執行階段設為變數 session
        session = window.pfcGetProESession()
        # 在視窗中打開零件檔案, 並且顯示出來
        pro_window = session.OpenFile(pfcCreate("pfcModelDescriptor").CreateFromFileName("cube.prt"))
        solid = session.GetModel("cube.prt", window.pfcCreate("pfcModelType").MDL_PART)
        # 在 Brython 中與 Python 語法相同, 只有初值設定問題, 無需宣告變數
        # length, width, myf, myn, i, j, volume, count, d1Value, d2Value
        # 將模型檔中的 length 變數設為 javascript 中的 length 變數
        length = solid.GetParam("a1")
        # 將模型檔中的 width 變數設為 javascript 中的 width 變數
        width = solid.GetParam("a2")
        # 改變零件尺寸
        # myf=20
        # myn=20
        volume = 0
        count = 0
        try:
            # 以下採用 URL 輸入對應變數
            # createParametersFromArguments ();
            # 以下則直接利用 javascript 程式改變零件參數
            for i in range(5):
                myf ='''+str(W)+'''
                myn ='''+str(W)+''' + i*2.0
                # 設定變數值, 利用 ModelItem 中的 CreateDoubleParamValue 轉換成 Pro/Web.Link 所需要的浮點數值
                d1Value = window.pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myf)
                d2Value = window.pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn)
                # 將處理好的變數值, 指定給對應的零件變數
                length.Value = d1Value
                width.Value = d2Value
                # 零件尺寸重新設定後, 呼叫 Regenerate 更新模型
                # 在 JavaScript 為 null 在 Brython 為 None
                solid.Regenerate(None)
                # 利用 GetMassProperty 取得模型的質量相關物件
                properties = solid.GetMassProperty(None)
                # volume = volume + properties.Volume
                volume = properties.Volume
                count = count + 1
                window.alert("執行第"+count+"次,零件總體積:"+volume)
                # 將零件存為新檔案
                newfile = document.pwl.pwlMdlSaveAs("cube.prt", "v:/tmp", "cube"+count+".prt")
                if (!newfile.Status):
                    window.alert("pwlMdlSaveAs failed (" + newfile.ErrorCode + ")")
                # window.alert("共執行:"+count+"次,零件總體積:"+volume)
                # window.alert("零件體積:"+properties.Volume)
                # window.alert("零件體積取整數:"+Math.round(properties.Volume));
        except:
            window.alert ("Exception occurred: "+window.pfcGetExceptionType (err))
    </script>
    '''

        return outstring
    @cherrypy.expose
    def fileuploadform(self):
        return '''<h1>file upload</h1>
    <script src="/static/jquery.js" type="text/javascript"></script>
    <script src="/static/axuploader.js" type="text/javascript"></script>
    <script>
    $(document).ready(function(){
    $('.prova').axuploader({url:'fileaxupload', allowExt:['jpg','png','gif','7z','pdf','zip','flv','stl','swf'],
    finish:function(x,files)
        {
            alert('All files have been uploaded: '+files);
        },
    enable:true,
    remotePath:function(){
    return 'downloads/';
    }
    });
    });
    </script>
    <div class="prova"></div>
    <input type="button" onclick="$('.prova').axuploader('disable')" value="asd" />
    <input type="button" onclick="$('.prova').axuploader('enable')" value="ok" />
    </section></body></html>
    '''
    @cherrypy.expose
    def fileaxupload(self, *args, **kwargs):
        filename = kwargs["ax-file-name"]
        flag = kwargs["start"]
        if flag == "0":
            file = open(download_root_dir+"downloads/"+filename, "wb")
        else:
            file = open(download_root_dir+"downloads/"+filename, "ab")
        file.write(cherrypy.request.body.read())
        file.close()
        return "files uploaded!"
    @cherrypy.expose
    def download_list(self, item_per_page=5, page=1, keyword=None, *args, **kwargs):
        files = os.listdir(download_root_dir+"downloads/")
        total_rows = len(files)
        totalpage = math.ceil(total_rows/int(item_per_page))
        starti = int(item_per_page) * (int(page) - 1) + 1
        endi = starti + int(item_per_page) - 1
        outstring = "<form method='post' action='delete_file'>"
        notlast = False
        if total_rows > 0:
            outstring += "<br />"
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "download_list?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'><<</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "download_list?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
                if index>= 0 and index< totalpage:
                    page_now = index + 1 
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "download_list?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "

            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>>></a><br /><br />"
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
                outstring += downloadlist_access_list(files, starti, endi)+"<br />"
            else:
                outstring += "<br /><br />"
                outstring += downloadlist_access_list(files, starti, total_rows)+"<br />"
            
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "download_list?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'><<</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "download_list?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
            #for ($j=$page-$range;$j<$page+$range;$j++)
                if index >=0 and index < totalpage:
                    page_now = index + 1
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "download_list?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "
            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>>></a>"
        else:
            outstring += "no data!"
        outstring += "<br /><br /><input type='submit' value='delete'><input type='reset' value='reset'></form>"

        return "<div class='container'><nav>"+ \
            "</nav><section><h1>Download List</h1>"+outstring+"<br/><br /></body></html>"
class Download:
    @cherrypy.expose
    def index(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
    
root = Midterm()
root.download = Download()
#root.gear = gear.Gear()

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(root, config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(root, config=application_conf)
