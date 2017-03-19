#!/user/bin/python
# -*- coding:utf-8 -*-
# -*- coding: encoding -*-
#coding:gbk
#----------------------------------------------------------
import re
import string
import sqlite3

#=====================初始值设定==================
global frequency_sum_forward,frequency_sum_backward
frequency_sum_forward=0
frequency_sum_backward=0
MaxLen=6

#=====================词库操作部分================

def get_first_shengmu(word):
        code = word.encode('gbk')  #tranform the word into 'gbk'code
        gbk_code = code[0] * 256 + code[1] - 65536  #according to the 'gbk'code we can get the first shengmu of the word
        if gbk_code >= -20319 and gbk_code <= -20284:
            return 'a'
        elif gbk_code >= -20283 and gbk_code <= -19776:
            return 'b'
        elif gbk_code >= -19775 and gbk_code <= -19219:
            return 'c'
        elif gbk_code >= -19218 and gbk_code <= -18711:
            return 'd'
        elif gbk_code >= -18710 and gbk_code <= -18527:
            return 'e'
        elif gbk_code >= -18526 and gbk_code <= -18240:
            return 'f'
        elif gbk_code >= -18239 and gbk_code <= -17923:
            return 'g'
        elif gbk_code >= -17922 and gbk_code <= -17418:
            return 'h'
        elif gbk_code >= -17417 and gbk_code <= -16475:
            return 'j'
        elif gbk_code >= -16474 and gbk_code <= -16213:
            return 'k'
        elif gbk_code >= -16212 and gbk_code <= -15641:
            return 'l'
        elif gbk_code >= -15640 and gbk_code <= -15166:
            return 'm'
        elif gbk_code >= -15165 and gbk_code <= -14923:
            return 'n'
        elif gbk_code >= -14922 and gbk_code <= -14915:
            return 'o'
        elif gbk_code >= -14914 and gbk_code <= -14631:
            return 'p'
        elif gbk_code >= -14630 and gbk_code <= -14150:
            return 'q'
        elif gbk_code >= -14149 and gbk_code <= -14091:
            return 'r'
        elif gbk_code >= -14090 and gbk_code <= -13119:
            return 's'
        elif gbk_code >= -13118 and gbk_code <= -12839:
            return 't'
        elif gbk_code >= -12838 and gbk_code <= -12557:
            return 'w'
        elif gbk_code >= -12556 and gbk_code <= -11848:
            return 'x'
        elif gbk_code >= -11847 and gbk_code <= -11056:
            return 'y'
        elif gbk_code >= -11055 and gbk_code <= -10247:
            return 'z'
        return 'other'



def open_lexicon():#the function to open the 27 databases
    global names
    position="lexicon\\'{:s}'.db"
    names=globals()
    alphabet=[]
    for i in string.ascii_lowercase:
        alphabet.append(i)
    alphabet.append('other')
    for i in alphabet:
        names['base%s'% i]=sqlite3.connect(position.format(i))
        names['curs%s'% i]=names['base%s'% i].cursor()



def search_in_lexicon(word):#search in the db whether the word is in the lexicon,if true return the frequency
    #global letter
    letter=get_first_shengmu(word[0])
    try:
        names['curs%s'% letter].execute("select * from "+word[0])
        line = names['curs%s'% letter].fetchone()
        while line!=None:
            if word != line[1]:
                line = names['curs%s'% letter].fetchone()
            else:
                frequency=line[0]
                names['base%s'% letter].commit()
                return frequency
        names['base%s'% letter].commit()
        return False
    except:
        names['base%s'% letter].commit()
        return False


def whether_word_in_lexicon(word):#the function to judge whether the word is already in the lexicon
    letter=get_first_shengmu(word[0])
    try:
        names['curs%s'% letter].execute("select * from "+word[0])
        line = names['curs%s'% letter].fetchone()
        while line!=None:
            if word != line[1]:
                line = names['curs%s'% letter].fetchone()
            else:
                names['base%s'% letter].commit()
                return True
        return False
    except:
        return False


def add_word_to_lexicon(word,frequency):#the function to add a word and its frequency to the lexicon
    letter=get_first_shengmu(word)
    name = "create table '{:s}' (fre integer,word_name varchar(10) UNIQUE)"
    insert = "insert into '{:s}' values({:d}, '{:s}')"
    try:
        names['curs%s'% letter].execute(name.format(word[0]))
        names['curs%s'% letter].execute(insert.format(word[0],int(frequency),word))
        names['base%s'% letter].commit()
    except:
        try:
            names['curs%s'% letter].execute(insert.format(word[0],int(frequency),word))
            names['base%s'% letter].commit()
        except:
            names['base%s'% letter].commit()


def del_word_in_lexicon(word):#the function to delete the word in lexicon
    letter=get_first_shengmu(word)
    if whether_word_in_lexicon(word):
        delete = "delete from '{:s}' where word_name like '{:s}'"
        names['curs%s'% letter].execute(delete.format(word[0],word))
        names['base%s'% letter].commit()
        showinfo(title="提示",message="恭喜您，删除成功！")
    else:showerror(title="错误",message="词库中没有该词！")





#=====================算法部分====================
def get_MaxLen(n):
    global MaxLen
    MaxLen=n

def judge_number(character):
    number_set="1234567890"
    if character in number_set:
        return True
    else:
        return False

def judge_english(character):
    english_set="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if character in english_set:
        return True
    else:
        return False

def judge_chinese(character):
    if character>=u'\u4e00' and character<=u'\u9fa5':
        return True
    return False

def regular(text):
    text=re.split(r'[ \t\n]+',text)
    return ''.join(text)

def divide(text,sentences,S):
    punctuation='。，、；：？！——（）……《》·~-/'
    if text=="":
        if S!='':
            sentences.append(S)
        return sentences
    if text[0] in punctuation:
        S+=text[0]
        sentences.append(S)
        return divide(text[1:],sentences,'')
    else:
        S+=text[0]
        return divide(text[1:],sentences,S)


def seperate_chinese(sentence):
    result=''
    length=len(sentence)
    try:
        for i in range(length):
            if judge_chinese(sentence[i])+judge_chinese(sentence[i+1])==1:
                result+=sentence[i]+"|"
            else:
                result+=sentence[i]
    except:
        result+=sentence[length-1]
    return result

def seperate_number(sentence):
    result=''
    length=len(sentence)
    try:
        for i in range(length):
            if judge_number(sentence[i])+judge_number(sentence[i+1])==1:
                result+=sentence[i]+"|"
            else:
                result+=sentence[i]
    except:
        result+=sentence[length-1]
    return result

def seperate_english(sentence):
    result=''
    length=len(sentence)
    try:
        for i in range(length):
            if judge_english(sentence[i])+judge_english(sentence[i+1])==1:
                result+=sentence[i]+"|"
            else:
                result+=sentence[i]
    except:
        result+=sentence[length-1]
    return result

def complete_seperate(sentence):
    result_by_num=[]
    words=seperate_chinese(sentence).split("|")
    for word in words:
        by_number=seperate_number(word)
        result_by_num+=by_number.split("|")
    result_by_eng=[]
    for word in result_by_num:
        by_english=seperate_english(word)
        result_by_eng+=by_english.split("|")
    return "|".join(result_by_eng)


def forward_max_matching_ch(S1,MaxLen,S2=''):
    global frequency_sum_forward
    if S1=="":
        return S2
    if len(S1)<=MaxLen:
        MaxLen=len(S1)
    W=S1[0:MaxLen]
    while len(W)!=1:
        if search_in_lexicon(W):
            S2+=W+"|"
            frequency_sum_forward+=search_in_lexicon(W)
            return forward_max_matching_ch(S1[len(W):],MaxLen,S2)
        else:
            length=len(W)-1
            W=W[:length]
    frequency_sum_forward+=search_in_lexicon(W)
    S2+=W+"|"
    return forward_max_matching_ch(S1[1:],MaxLen,S2)

def complete_forward_matching(sentence):
    global frequency_sum_forward
    sentences=complete_seperate(sentence).split("|")
    result=''
    for sentence in sentences:
        if judge_chinese(sentence):
            sentence=forward_max_matching_ch(sentence,MaxLen,"")
            result+=sentence
        else:
            result+=sentence+"|"
    return result


def backward_max_matching_ch(S1,MaxLen,S2=''):
    global frequency_sum_backward
    if S1=="":
        return S2
    if len(S1)<=MaxLen:
        MaxLen=len(S1)
    W=S1[-MaxLen:]
    while len(W)!=1:
        if search_in_lexicon(W):
            frequency_sum_backward+=search_in_lexicon(W)
            S2=W+"|"+S2
            return backward_max_matching_ch(S1[:-len(W)],MaxLen,S2)
        else:
            length=len(W)-1
            W=W[-length:]
    frequency_sum_backward+=search_in_lexicon(W)
    S2=W+"|"+S2
    return backward_max_matching_ch(S1[:len(S1)-1],MaxLen,S2)

def complete_backward_matching(sentence):
    global frequency_sum_backward
    sentences=complete_seperate(sentence).split("|")
    result=''
    for sentence in sentences:
        if judge_chinese(sentence):
            sentence=backward_max_matching_ch(sentence,MaxLen,"")
            result+=sentence
        else:
            result+=sentence+"|"
    return result

def accurate_matching(sentence):
    global frequency_sum_forward,frequency_sum_backward
    forward=complete_forward_matching(sentence)
    forward_counting=forward.count("|")
    backward=complete_backward_matching(sentence)
    backward_counting=backward.count("|")
    if forward_counting>backward_counting:
        return forward
    if forward_counting<backward_counting:
        return backward
    else:
        if frequency_sum_forward>=frequency_sum_backward:
            return forward
        else:
            return backward

def segmentation(text):
    i=1
    text_seg=["您的分词结果如下：\n"]
    regular_text=regular(text)
    sentences=divide(regular_text,[],'')
    for sentence in sentences:
        sentence_seg=accurate_matching(sentence)
        text_seg.append(str(i)+"."+sentence_seg+"\n")
        i=i+1
    return ''.join(text_seg)
#==============================================================================================
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
    winsound.PlaySound('流星分词素材\\【ゆめこ】文乃的幸福理論', winsound.SND_ASYNC)

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
        self.fm2.add_command(label='最大词长修改',command=self.open_MaxLen)

#        self.fm2.add_radiobutton(label='1',variable=self.v,value=1)
#        self.fm2.add_radiobutton(label='2',variable=self.v,value=2)
#        self.fm2.add_radiobutton(label='3',variable=self.v,value=3)
#        self.fm2.add_radiobutton(label='4',variable=self.v,value=4)
#        self.fm2.add_radiobutton(label='5',variable=self.v,value=5)
#        self.fm2.add_radiobutton(label='6',variable=self.v,value=6)
#        self.fm2.add_radiobutton(label='7',variable=self.v,value=7)
#        self.fm2.add_radiobutton(label='8',variable=self.v,value=8)
#        self.fm2.add_radiobutton(label='9',variable=self.v,value=9)

        self.fm3=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='字典调整',menu=self.fm3)
        self.fm3.add_command(label='添加/删除',command=self.open_dic)

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
    def open_dic(self):   #打开词频操作窗口
        self.tl=MyTL1(root)
    def open_instr(self):   #打开说明窗口
        self.tl=MyTL2(root)
    def open_about(self):   #打开关于窗口
        self.tl=MyTL3(root)
    def open_MaxLen(self):
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
        if self.text1.get()=='\n':
            showerror(title='错误',message='分词输入内容不能为空！')
        else:
            self.text.set('正在分词，请耐心等待………')

            result=segmentation(self.text1.get())
            self.text2.insert(result)

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
        self.tl.title('字典操作')
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
    def open(self):     #打开新窗口
        self.tl2=MyTL5(self.tl)
    def add(self):
        if self.text1.get() == '':
            showerror(title='错误',message='添加的词不能为空！')
        else:
            if self.text2.get() == 0:
                showerror(title='错误',message='添加词的词频不能为0！')
            else:
                if whether_word_in_lexicon(self.text1.get()) == True:
                    showerror(title='错误',message='添加的词已存在！')
                else:
                    add_word_to_lexicon(self.text1.get(),self.text2.get())
                    showinfo(title='消息',message='添加成功！')
                    self.tl.destroy()

    def dele(self):
        if self.text1.get() == '':
            showerror(title='错误',message='删除的词不能为空！')
        else:
            if whether_word_in_lexicon(self.text1.get()) == False:
                showerror(title='错误',message='删除的词不存在！')
            else:
                del_word_in_lexicon(self.text1.get())
                showinfo(title='消息',message='删除成功！')
                self.tl.destroy()

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

class MyTL3:        #关于窗口
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('关于')
        self.ft1=Font(family = '黑体',size = 35)
        self.bm = PhotoImage(file='流星分词素材\\Silver Comet.gif')
        self.blank1=Label(self.tl,text='                                     ')
        self.blank1.pack()
        self.frame1=Frame(self.tl)
        self.gif=Label(self.frame1,image=self.bm)
        self.gif.pack(side=LEFT)
        self.label1=Label(self.frame1,text='中文分词系统 ',font=self.ft1,fg='#4F4F4F')
        self.label1.pack()
        self.label2=Label(self.frame1,text='Chinese Word Segmentating System')
        self.label2.pack()
        self.frame1.pack()
        self.xhx=Label(self.tl,text='————————————————————————————',fg='#8E8E8E')
        self.xhx.pack()
        self.frame2=Frame(self.tl)
        for i in ['K.O.1 小组','Verson 3.0（内部版本 3.3.7）','Copyright © 2012-2013 K.O.1 小组保留所有权利。'
        ,'中文分词系统 Verson 3.0 分词算法及其用户界面受中国和其他','国家/地区的商标法和其他待颁布或已颁布的知识产权法保护。']:
            self.label=Label(self.frame2,text=i)
            self.label.pack(anchor='nw')
        self.xhx2=Label(self.frame2,text='————————————————————————————',fg='#8E8E8E')
        self.xhx2.pack()
        for i in ['重要更新历史：','————Verson 3.0：','    1.增加辅助词语分词功能，人工干预分词结果更精准'
        ,'    2.分词算法优化，速度更快更流畅','————Verson 2.1：','    1.改进分词算法和查询结构，分词速度优化'
        ,'    2.同步改进数据库结构','    3.分词算法的细微调整，优化了分词速度'
        ,'————Verson 2.0：','    1.语料词典保存在数据库中，启动速度大幅优化'
        ,'    2.分词算法查询系统优化','    3.增加了数据库词典操作功能','————Verson 1.1：',
        '    1.分离双向分词功能为快速分词和精准分词，用户可自行选择','    2.分词算法大幅优化，快速分词更快，精准分词更准']:
            self.label=Label(self.frame2,text=i)
            self.label.pack(anchor='nw')
        self.frame2.pack()
        self.blank2=Label(self.tl,text='                                     ')
        self.blank2.pack()

class MyTL4:   #最大词长调整
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('最大词长调整')
        self.MaxLentemp = StringVar() #设置下拉框
        self.MaxLentemp.set(MaxLen)
        items = [ ]
        for i in range(10):
            items.append(i+1)
        self.gcombobox1=Combobox(self.tl,values=items,textvariable=self.MaxLentemp,height=10,width=6)
        self.gcombobox1.pack()

        self.bottun=Button(self.tl,text="确定",relief=GROOVE,cursor="hand2",command=self.MaxLen_return)
        self.bottun.pack(side=RIGHT,padx=15)


    def MaxLen_return(self): #得到最大词限
        global MaxLen
        if is_postiveN(self.MaxLentemp.get()):
            if int(self.MaxLentemp.get())<=10:
                MaxLen=int(self.MaxLentemp.get())
                showinfo(title="提示",message="修改成功！")
            else:showerror(title="错误",message="选择有误！")
        else:showerror(title="错误",message="选择有误！")



class MyTL5:   #字典调整是操作帮助
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('帮助')
        for i in ['通过选择操作选项可以切换‘添加词语’与‘删除词语’模式。',
        '‘添加词语’：向字典中添加输入的词语与它的词频。添加词必须为字典中不存在的词。',
        '‘删除词语’：在字典中删除输入的词语与它的词频，删除词必须为字典中已存在的词。']:
            self.label=Label(self.tl,text=i)
            self.label.pack()
        self.bm = PhotoImage(file='流星分词素材\\Silver Comet.gif')
        self.label1=Label(self.tl,image=self.bm)
        self.label1.pack()

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
open_lexicon()

init_tk()

img=PhotoImage(file='流星分词素材\\bg.gif')  #背景
bg=Label(root,image=img)
bg.place_configure(x=0,y=0)

text1=inputText(root)
text2=outputText(root)

menu=MyMenu(root,text1,text2)
bottun=Mybottun(root,text1,text2,menu)

welMenu()

musicON()
root.mainloop()
musicOFF()
