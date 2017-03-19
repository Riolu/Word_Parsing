#!/user/bin/python
# -*- coding:utf-8 -*-
# -*- coding: encoding -*-
#coding:gbk
#----------------------------------------------------------
import sqlite3
global maxlen
maxlen=5

def add_word(word,freq):   #向词典数据库添加词和词频
    first=word[0]
    r_tempdic(first)
    p=0
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)==False:
             tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
             conn.commit()
        else:
            return False
    else:
        tempdicname.execute(''''create table '''+first+''' (
        word text ,
        freq text
        )''')
        tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
        conn.commit()
    first=word[-1]
    l_tempdic(first)
    p=-1
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)==False:
             tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
             conn.commit()
        else:
            return False
    else:
        tempdicname.execute('''create table '''+first+''' (
        word text ,
        freq text
        )''')
        tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
        conn.commit()
def del_word(word):  #从词典数据库删词
    first=word[0]
    r_tempdic(first)
    p=0
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)!=False:
             tempdicname.execute('delete from '+first+' where word==?',(word,))
             conn.commit()
        else:
            return False
    else:
        return False
    first=word[-1]
    l_tempdic(first)
    p=-1
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)!=False:
             tempdicname.execute('delete from '+first+' where word==?',(word,))
             conn.commit()
        else:
            return False
    else:
        return False
#----------------------------------------------------------
conn1=sqlite3.connect('db\\a-h.db')   #与六个数据库建立连接并定义指针
conn2=sqlite3.connect('db\\i-p.db')
conn3=sqlite3.connect('db\\q-z.db')
conn4=sqlite3.connect('db\\l_a-h.db')
conn5=sqlite3.connect('db\\l_i-p.db')
conn6=sqlite3.connect('db\\l_q-z.db')
curs1=conn1.cursor()
curs2=conn2.cursor()
curs3=conn3.cursor()
curs4=conn4.cursor()
curs5=conn5.cursor()
curs6=conn6.cursor()
def able_word(fir,curs): #判断词典中是否有以某个字开头的词语
    try:
        curs.execute('select * from '+fir)
        return True
    except:
        return False
def find_word(word,curs,p):  #判断是否有某个词语并返回词频
    first=word[p]
    curs.execute('select * from '+first+' where word==?',(word,))
    line=curs.fetchone()
    if line==None:
        return False
    else:
        freq=line[1]
        return freq
#--------------------------------------------------------
import string
notchs=string.ascii_letters+string.digits+' +=' #标记 数字 字母 + = 以分为一个词
tempdicname=sqlite3.Cursor     #当前数据库游标
special=[]     #辅助分词词典
r_freq=0       #正向匹配词频和
l_freq=0       #逆向匹配词频和
#词库判断模块-----------数据库游标切换
a=[ i.encode('gbk') for i in ['祸', '瀑'] ]
def r_tempdic(s):
    global tempdicname
    global conn
    te=s.encode('gbk')
    if a[1]<te:     #声母在q-z
        tempdicname=curs3
        conn=conn3
    elif a[0]<te:   #声母在i-p
        tempdicname=curs2
        conn=conn2
    else:           #声母在a-h
        tempdicname=curs1
        conn=conn1
def l_tempdic(s):
    global tempdicname
    global conn
    te=s.encode('gbk')
    if a[1]<te:
        tempdicname=curs6  #声母在q-z
        conn=conn6
    elif a[0]<te:
        tempdicname=curs5  #声母在i-p
        conn=conn5
    else:                  #声母在a-h
        tempdicname=curs4
        conn=conn3   #-
def right_seg(text):     #正向分词
    global r_freq,tempdicname
    if len(text)>=1:
        if text[0] in notchs:    #如果分词内容第一个字不是中文（字母数字+=）
            try:                 #继续读取下一个字直到是中文为止，并分出前面部分
                if text[1] in notchs:
                    return text[0] + right_seg(text[1:])
                else:
                    return text[0]+'/' +right_seg(text[1:])
            except:
                return text[0] +'/' +right_seg(text[1:])
        else:
            length=5       #设定词语最大长度为5进行最大匹配
            if len(text)<length: #预处理最大长度以减小时间复杂度
                length=len(text)
            r_tempdic(text[0])        #首字游标预处理
            while length>1:
                if not able_word(text[0],tempdicname):      #判断首字是否可构成词
                    return text[0] + '/' + right_seg(text[1:])
                else:
                    tempfreq=find_word(text[:length],tempdicname,0)   #匹配词语
                    if tempfreq!=False:
                        r_freq=r_freq+int(tempfreq)    #计算正向词频
                        return text[:length] + '/' + right_seg(text[length:])
                length=length-1
            return text[0] + '/' + right_seg(text[1:])
    else:
        return text
def left_seg(text):    #逆向分词
    global tempdicname,l_freq
    if len(text)>=1:
        if text[-1] in notchs:     #如果分词内容最后一个字不是中文（字母数字+=）
            try:                   #继续读取上一个字直到是中文为止，并分出后面部分
                if text[-2] in notchs:
                    return left_seg(text[:-1]) + text[-1]
                else:
                    return left_seg(text[:-1]) +'/'+text[-1]
            except:
                return  left_seg(text[:-1])+'/'+text[-1]
        else:
            length=5           #设定词语最大长度为5进行最大匹配
            if len(text)<length:   #预处理最大长度以减小时间复杂度
                length=len(text)
            l_tempdic(text[-1])    #尾字游标预处理
            while length>1:
                if not able_word(text[-1],tempdicname):    #判断尾字是否可构成词
                    return  left_seg(text[:-1]) + '/' + text[-1]
                else:
                    tempfreq=find_word(text[-length:],tempdicname,-1)  #匹配词语
                    if tempfreq!=False:
                        l_freq=l_freq+int(tempfreq)      #计算逆向词频
                        return left_seg(text[:-length]) + '/' + text[-length:]
                length=length-1
            return left_seg(text[:-1]) + '/' + text[-1]
    else:
        return text
def divide(text): #按标点分割句子
    punctuation='，。、：；《》（）？！.~…\"“”()‘’——'
    sentences=[]
    for i in punctuation:
        text=text.replace(i,' ')
    sentences=text.split()
    return sentences
def accurate_seg(sentence):  #精准分词
    r=right_seg(sentence)
    if r[-1]=='/':     #首末/符处理
        r=r[:-1]
    l=left_seg(sentence)
    if l[0]=='/':
        l=l[1:]
    if r==l:
        return r
    else:
        return reprocess(r,l)
def fast_seg(sentence):      #快速分词
    r=left_seg(sentence)
    if r[0]=='/':
        r=r[1:]
    return r
def reprocess(rseg,lseg):   #精准分词词频处理
    r=rseg.count('/')       #对分词个数进行比较取较小者
    l=lseg.count('/')
    if r==l:
        if r_freq>l_freq:
            return rseg
        else:
            return lseg
    elif r<l:
        return rseg
    elif r>l:
        return lseg
def special_divide(text,words):  #辅助分词划分处理
    global special
    special=words.split('|')
    for i in special:
        text=('，'+i+'，').join(text.split(i))   #将辅助词语分隔为句子
    return text
#============================================================================================
def is_postiveN(n): #判断是否为正整数
    try:
        n_1=int(n)
        if str(n_1)==str(n) and n_1>=1:
            return True
        else:return False
    except:return False
#==============================================================================================

from tkinter import*
from tkinter.filedialog import*
from tkinter.messagebox import*
from tkinter.font import*
from tkinter.ttk import Combobox
import winsound

def musicON():
    winsound.PlaySound('流星分词素材\\NEXT TO YOU - ken arai', winsound.SND_ASYNC)

def musicOFF():
    winsound.PlaySound('NULL', winsound.SND_ASYNC)


class MyMenu: #主界面
    def __init__(self,root,text1,text2):
        self.root=root

        self.text1=text1
        self.text2=text2
        self.menubar=Menu(root)

        self.fm1=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='文件',menu=self.fm1)
        self.fm1.add_command(label='打开',command=self.open_file)
        self.fm1.add_command(label='另存为',command=self.save_file)
        self.fm1.add_command(label='退出',command=self.quit)

        self.v=IntVar()
        self.v.set(5)
        self.fm2=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='最大词长',menu=self.fm2)
        self.fm2.add_command(label='最大词长修改',command=self.open_maxlen)

        self.fm3=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='字典调整',menu=self.fm3)
        self.fm3.add_command(label='添加/删除',command=self.open_dic)
        self.fm3.add_command(label='字典查询',command=self.find_dic)
        self.fm3.add_command(label='词频调整',command=self.revise_dic)

        self.fm4=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='帮助',menu=self.fm4)
        self.fm4.add_command(label='说明',command=self.open_instr)
        self.fm4.add_command(label='关于',command=self.open_about)

        self.root['menu']=self.menubar

    def open_file(self):    #导入文件
        self.t=askopenfilename(filetypes=[("文本文档","*.txt")])
        if self.t != '':
           self.file=open(self.t,'r')
           self.content=self.file.read()
           self.text1.insert(self.content)
    def save_file(self):    #保存文件
        if self.text2.get()=='\n':
            showerror(title='错误',message='保存的分词结果不能为空！')
        else:
            self.t=asksaveasfilename(filetypes=[("文本文档","*.txt")],defaultextension='txt')
            if self.t != '':
                self.file=open(self.t,'w')
                self.file.write(self.text2.get())
                self.file.close()
    def open_dic(self): #打开添加/删除窗口
        self.tl=MyTL1(root)
    def find_dic(self): #打开字典查询窗口
        self.tl=MyTL5(root)
    def revise_dic(self): #打开词频调整窗口
        self.tl=MyTL1(root)

    def open_instr(self):   #打开说明窗口
        self.tl=MyTL2(root)
    def open_about(self):   #打开关于窗口
        self.tl=MyTL3(root)
    def open_maxlen(self):
        self.t1=MyTL4(root)
    def quit(self):
        root.destroy()

class Mybottun:  #主界面按钮
    def __init__(self,root,text1,text2,menu):
        self.root=root
        self.text1=text1
        self.text2=text2
        self.menu=menu

        self.text=StringVar()
        self.text.set('')
        self.label=Label(self.root,textvariable=self.text,fg='blue',font=("黑体",12,BOLD))
        self.label.place_configure(x=466,y=570)

        self.img1=PhotoImage(file="流星分词素材\\开始分词’.gif")
        self.bottun1=Button(self.root,image=self.img1,command=self.start,relief=GROOVE,cursor="hand2")
        self.bottun1.place_configure(x=392,y=500)

        self.img2=PhotoImage(file="流星分词素材\\清空原文.gif")
        self.bottun2=Button(self.root,image=self.img2,command=self.clean1,relief=GROOVE,cursor="hand2")
        self.bottun2.place_configure(x=92,y=520)

        self.img3=PhotoImage(file="流星分词素材\\清空结果.gif")
        self.bottun3=Button(self.root,image=self.img3,command=self.clean2,relief=GROOVE,cursor="hand2")
        self.bottun3.place_configure(x=671,y=521)




    def start(self): #慢点改成尊神的分词程序
        global special
        global r_freq
        global l_freq
        if self.text1.get()=='\n':
            showerror(title='错误',message='分词输入内容不能为空！')
        else:
            self.text.set('正在分词，请耐心等待………')
            result=[]
            special={}
            if self.menu.v.get() == 1:
                if self.AW.text1.get() != '':
                    temp=special_divide(self.text1.get(),self.AW.text1.get())
                else:
                    temp=self.text1.get()
                sentences=divide(temp)
                if self.AW.v.get() == 1:
                    for i in sentences:
                        if i in special:
                            result.append(i)
                        else:
                            r_freq=0
                            l_freq=0
                            result.append(accurate_seg(i))
                else:
                    for i in sentences:
                        if i in special:
                            result.append(i)
                        else:
                            r_freq=0
                            l_freq=0
                            r=left_seg(i)
                            if r[0]=='/':
                                r=r[1:]
                            result.append(r)
            if self.menu.v.get() == 2:
                sentences=divide(self.text1.get())
                for i in range(len(sentences)):
                    r_freq=0
                    l_freq=0
                    result.append(fast_seg(sentences[i]))

            self.text2.insert('/'.join(result))
            self.text.set('分词完毕')
    def clean1(self):
        if askquestion(title='提示',message='真的要清空分词原文么？') == 'yes':
            self.text1.clear()
    def clean2(self):
        if askquestion(title='提示',message='真的要清空分词结果么？') == 'yes':
            self.text2.clear()
            self.text.set('')

class inputText:   #文本输入框
    def __init__(self,root):
        self.root=root
        self.frame=Frame(root)
        self.T=Text(self.frame,width=37,height=25,cursor="star")
        self.sl=Scrollbar(self.frame)
        self.sl.pack(side=RIGHT,fill=Y)
        self.T['yscrollcommand']=self.sl.set
        self.T.pack(side=LEFT)
        self.sl['command'] = self.T.yview
        self.frame.place_configure(x=80,y=120)

    def insert(self,r):
        self.T.insert(1.0,r)
    def clear(self):
        self.T.delete(1.0,END)
    def get(self):
        return self.T.get(1.0,END)

class outputText:   #文本输出框
    def __init__(self,root):
        self.root=root
        self.frame=Frame(root)
        self.T=Text(self.frame,width=37,height=25,cursor="star")
        self.sl=Scrollbar(self.frame)
        self.sl.pack(side=RIGHT,fill=Y)
        self.T['yscrollcommand']=self.sl.set
        self.T.pack(side=LEFT)
        self.sl['command'] = self.T.yview
        self.frame.place_configure(x=645,y=120)

    def insert(self,r):
        self.T.insert(1.0,r)
    def clear(self):
        self.T.delete(1.0,END)
    def get(self):
        return self.T.get(1.0,END)

class MyTL1:        #词频操作窗口
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)        #顶层部件的工作，直接由窗口管理器管理的窗口。切出新的窗口
        self.tl.title('添加/删除')
        self.v=IntVar()
        self.v.set(1)
        self.menubar=Menu(self.tl)
        self.fm1=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='操作选项',menu=self.fm1)
        self.fm1.add_radiobutton(label='添加词语',variable=self.v,value=1,command=self.TJ)
        self.fm1.add_radiobutton(label='删除词语',variable=self.v,value=2,command=self.SC)
        self.menubar.add_command(label='操作帮助',command=self.open)
        self.tl['menu']=self.menubar
        self.frame=Frame(self.tl)
        self.frame1=Frame(self.frame)
        self.text3=StringVar()
        self.text3.set('添加词：')
        self.label1=Label(self.frame1,textvariable=self.text3)
        self.label1.pack(anchor='nw',ipadx=40)
        self.text1=StringVar()
        self.entry1=Entry(self.frame1,textvariable=self.text1,width=25)
        self.entry1.pack()
        self.frame1.pack(side=LEFT,ipadx=40)
        self.frame2=Frame(self.frame)
        self.label2=Label(self.frame2,text='添加词词频：')
        self.label2.pack(anchor='nw',ipadx=40)
        self.text2=IntVar()
        self.entry2=Entry(self.frame2,textvariable=self.text2,wid=10)
        self.entry2.pack()
        self.frame2.pack(side=LEFT,ipadx=40)
        self.frame.pack(fill=X)
        self.frame3=Frame(self.tl)
        self.button1=Button(self.frame3,text='添加',command=self.add,width=12)
        self.button2=Button(self.frame3,text='删除',command=self.dele,width=12)
        self.frame3.pack(side=BOTTOM)
        self.button1.pack()

    def SC(self):       #切换删除模式
        self.text3.set('删除词：')
        self.text1.set('')
        self.text2.set(0)
        self.frame3.forget()
        self.frame2.forget()
        self.frame1.pack(ipadx=40)
        self.frame3.pack(side=BOTTOM)
        self.button1.forget()
        self.button2.pack()
    def TJ(self):       #切换添加模式
        self.text3.set('添加词：')
        self.text1.set('')
        self.frame3.forget()
        self.frame2.pack(ipadx=40)
        self.frame3.pack(side=BOTTOM)
        self.button2.forget()
        self.button1.pack()
    def open(self):     #打开帮助窗口
        self.tl2=MyTL2(self.tl)
    def add(self):
        if self.text1.get() == '':
            showerror(title='错误',message='添加的词不能为空！')
        else:
            if self.text2.get() == 0:
                showerror(title='错误',message='添加词的词频不能为0！')
            else:
                if add_word(self.text1.get(),str(self.text2.get())) == False:
                    showerror(title='错误',message='添加的词已存在！')
                else:
                    showinfo(title='消息',message='添加成功！')
    def dele(self):
        if self.text1.get() == '':
            showerror(title='错误',message='删除的词不能为空！')
        else:
            if del_word(self.text1.get()) == False:
                showerror(title='错误',message='删除的词不存在！')
            else:
                showinfo(title='消息',message='删除成功！')

class MyTL2:        #说明窗口
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('说明')
        for i in ['文件：点击菜单中的‘文件’可以选择‘打开’来打开一个txt文档，将其导入‘分词原文’。',
        '         也可以选择‘保存’将‘分词结果’的内容以txt文档格式保存。',
        '         点击‘退出’可以退出本软件。',' ',
        '最大词长：分词所选用的最大词长',' ',
        '工具：点击菜单中的‘工具’可以选择‘字典操作’来在分词的数据库添加、删除词语。',' ',
        '帮助：点击菜单中的‘帮助’可以获取‘说明’中的软件使用方法，和‘关于’中的软件信息。']:
            self.label=Label(self.tl,text=i)
            self.label.pack(anchor='nw')
        self.bm = PhotoImage(file='Comet.gif')
        self.label1=Label(self.tl,image=self.bm)
        self.label1.pack()

class MyTL3: #关于窗口(信息，更新历史，心路历程)
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('关于我们')
        self.tl.geometry("800x700")
        self.tl.resizable(0,0)
        self.img=PhotoImage(file='流星分词素材\\about.gif')
        self.about=Label(self.tl,image=self.img)
        self.about.place_configure(x=0,y=0)


class MyTL4:   #最大词长调整
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('最大词长调整')
        self.maxlentemp = StringVar() #设置下拉框
        self.maxlentemp.set(maxlen)
        items = [ ]
        for i in range(10):
            items.append(i+1)
        self.gcombobox1=Combobox(self.tl,values=items,textvariable=self.maxlentemp,height=10,width=6)
        self.gcombobox1.pack()

        self.bottun=Button(self.tl,text="确定",relief=GROOVE,cursor="hand2",command=self.maxlen_return)
        self.bottun.pack(side=RIGHT,padx=15)


    def maxlen_return(self): #得到最大词限
        if is_postiveN(self.maxlentemp.get()):
            if int(self.maxlentemp.get())<=10:
                maxlen=self.maxlentemp.get()
                showinfo(title="提示",message="修改成功！")
            else:showerror(title="错误",message="选择有误！")
        else:showerror(title="错误",message="选择有误！")



class MyTL5: #字典查询窗口
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('字典查询')




def init_tk(): #窗体初始化
    global root
    root = Tk()
    root.title('流星分词素材\\Silver Comet     -银色流星┈━═☆')
    root.geometry("1000x600")   #主窗口大小
    root.resizable(0,0)

def welMenu():
    global root,bg,title,title2,start,start1,logo

    img=PhotoImage(file='流星分词素材\\welcome bg.gif')  #背景
    bg=Label(root,image=img)
    bg.img=img
    bg.place_configure(x=0,y=0)

    title= Canvas(root,cursor="hand2",width=510,height=130,highlightthickness=0)
    img=PhotoImage(file='流星分词素材\\流星分词.gif')
    title.create_image((258,72),image = img)
    title.img=img
    title.place_configure(x=2,y=2)

    start= Canvas(root,cursor="hand2",width=260,height=78,highlightthickness=0)
    img=PhotoImage(file='流星分词素材\\Start.gif')
    start.create_image((130,40),image = img)
    start.img=img
    start.place_configure(x=360,y=241)

    logo= Canvas(root,cursor="star",width=630,height=110,highlightthickness=0)
    img=PhotoImage(file='流星分词素材\\Silver Comet.gif')
    logo.create_image((320,56),image = img)
    logo.img=img
    logo.place_configure(x=348,y=485)

    title.bind("<Button-1>",change_title)
    start.bind("<Button-1>",vanish)
    start.bind("<Enter>",show_start1)
    start.bind("<Leave>",unshow_start1)


#=======================切换或弹出用====================
    title2= Canvas(root,cursor="hand2",width=510,height=130,highlightthickness=0)
    img=PhotoImage(file='流星分词素材\\流星分词（亮）.gif')
    title2.create_image((258,72),image = img)
    title2.img=img
    title2.bind("<Button-1>",return_title)

    start1= Canvas(root,width=200,height=55,highlightthickness=0)
    img=PhotoImage(file='流星分词素材\\开始分词.gif')
    start1.create_image((100,28),image = img)
    start1.img=img



#================event==========================
def vanish(event):
    bg.place_forget()
    title.place_forget()
    start.place_forget()
    logo.place_forget()
    title2.place_forget()

def change_title(event):
    title.place_forget()
    title2.place_configure(x=2,y=5)

def return_title(event):
    title2.place_forget()
    title.place_configure(x=2,y=2)

def show_start1(event):
    start1.place_configure(x=558,y=331)

def unshow_start1(event):
    start1.place_forget()
#====================================================

init_tk()

img=PhotoImage(file='流星分词素材\\bg.gif')  #背景
bg=Label(root,image=img)
bg.place_configure(x=0,y=0)

text1=inputText(root)
text2=outputText(root)

menu=MyMenu(root,text1,text2)
bottun=Mybottun(root,text1,text2,menu)

welMenu()

#musicON()
root.mainloop()
#musicOFF()


