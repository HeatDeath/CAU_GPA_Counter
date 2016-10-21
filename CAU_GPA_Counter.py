#Python
#coding=utf-8

import requests
import re
from bs4 import BeautifulSoup
import msvcrt

class course:
    def __init__(self,c1='0',c2='0',cn='0',ce='0',cr='0',ca='0',cg='0'):
        self.CourseNumber1 = c1;
        self.CourseNumber2 = c2;
        self.CourseName = cn;
        self.CourseEnglishName = ce;
        self.CourseCredit = cr;
        self.CourseAttribute = ca;
        self.CourseGrade = cg;

    def get_CourseNumber1(self):
        return self.CourseNumber1

    def get_CourseName(self):
        return self.CourseName

    def get_CourseCredit(self):
        return self.CourseCredit

    def get_CourseGrade(self):
        return self.CourseGrade

    def get_Mul(self):
        return float(self.CourseGrade)*float(self.CourseCredit)

    def change_CourseGrade(self,grade):
        self.CourseGrade=grade

    def change_CourseName(self,name):
        self.CourseName=name

    def change_CourseCredit(self,credit):
        self.CourseCredit=credit



def grade_change(grade_before):
    if grade_before == '优秀':
        grade = 4.0
        return grade
    if grade_before == '良好':
        grade = 3.7
        return grade
    if grade_before == '中等':
        grade = 2.7
        return grade
    if grade_before == '及格':
        grade = 2.0
        return grade
    if grade_before == '不及格':
        grade = 0.0
        return grade
    #然而并不清楚不能使用is或者.find的原因
    else:
        try:
            float(grade_before)
        except (ValueError, TypeError):
            return 0
        if float(grade_before) in range(90, 750):
            grade = 4.0
            return grade
        if float(grade_before) in range(85, 90):
            grade = 3.7
            return grade
        if float(grade_before) in range(82, 85):
            grade = 3.3
            return grade
        if float(grade_before) in range(78, 82):
            grade = 3.0
            return grade
        if float(grade_before) in range(75, 78):
            grade = 2.7
            return grade
        if float(grade_before) in range(72, 75):
            grade = 2.3
            return grade
        if float(grade_before) in range(68, 72):
            grade = 2.0
            return grade
        if float(grade_before) in range(64, 68):
            grade = 1.7
            return grade
        if float(grade_before) in range(60, 64):
            grade = 1.3
            return grade
        # Change failed grade's GPA
        if float(grade_before) < 5:
            grade = float(grade_before) * 0.6
            return grade
            return 0


def UrpLogin(params):
    session=requests.Session()
    s=session.post("http://urpjw.cau.edu.cn/loginAction.do",params)
    s=session.get("http://urpjw.cau.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA%C7%EF(%C8%FD%D1%A7%C6%DA)")
    #s=session.get("http://urpjw.cau.edu.cn/gradeLnAllAction.do?type=ln&oper=lnFajhKcCjInfo&lnxndm=2015-2016%D1%A7%C4%EA%C7%EF(%C8%FD%D1%A7%C6%DA)")
    bsObj=BeautifulSoup(s.text,'lxml')
    #print(bsObj)

    CourseList=[]
    for CourseMessageHtml in bsObj.find_all('td',align="center"):
        CourseMessageText=CourseMessageHtml.get_text()
    #CourseList.append(list(map(str,CourseMessageText.re.split('\n'))))
        CourseList.append(re.sub('\s','',CourseMessageText))
    #strip()返回移除字符串头尾指定的字符生成的新字符串,似乎可以达到相同的效果
#CourseList= [str(course.strip()[1:]) for course in CourseMessageText.split('\n')]
#Courses=str(CourseMessage.text)
#print(CourseList)
#print(len(CourseList))
#print(CourseList)
#print(CourseList)
    LessonList=[]

    for i in range(int(len(CourseList)/7)):
        LessonList.append("%s"% i)
        try:
            LessonList[i]=course(CourseList[i * 7], CourseList[i * 7 + 1], CourseList[i * 7 + 2], CourseList[i * 7 + 3],CourseList[i * 7 + 4], CourseList[i * 7 + 5], CourseList[i * 7 + 6])
        except IndexError:
            pass
    #print(len(LessonList))
    #可以考虑用某种方式将数据导入到Excel中
    #可以采集【全体新生】个人信息
    #print(LessonList[0].CourseName)
    '''
    #--------------提取学期信息-----------------
    for TermHtml in bsObj.find_all('td',valign='middle'):
        TermText=TermHtml.get_text()
        print(TermText)
    '''
    #将双学位和英语四六级对应的学分转换为0
    for i in range(len(LessonList)):
        if LessonList[i].get_CourseName().find('双学位') > 1:
            LessonList[i].change_CourseCredit(0)
        if LessonList[i].get_CourseName().find('CET') > 1:
            LessonList[i].change_CourseCredit(0)


    '''
    #检验转换是否成功
    for i in range(len(LessonList)):
        print(LessonList[i].CourseName)
        print(LessonList[i].CourseCredit)
        print(LessonList[i].CourseGrade)
    '''
    SumCreMulGra=float(0)
    SumCredit=float(0)
    for i in range(len(LessonList)):
        LessonList[i].change_CourseGrade(grade_change(LessonList[i].get_CourseGrade()))
    #print(LessonList[i].CourseName)
    #print(LessonList[i].CourseGrade)
        SumCreMulGra=SumCreMulGra+LessonList[i].get_Mul()
        SumCredit=SumCredit+float(LessonList[i].get_CourseCredit())

    print('当前Gpa为：%.2f' % (SumCreMulGra/SumCredit))

def UserInfoGet(params):
    params['zjh']=input('学号:')
    params['mm']=input('密码:')
    return params
params = {'zjh': '0', 'mm': '0'}
UrpLogin(UserInfoGet(params))
#UserInfoGet(params)
#print(params)

