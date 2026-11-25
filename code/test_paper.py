import random
import csv
import os

class Test_Paper:
    #定义函数获取学习币值
    def learning_coin(numbers=3, points=None):
        '''
        输入
        -------------
        numbers:骰子个数
        points:骰子点数

        输出
        -------------
        total:学习币值
        '''
        points = []
        while numbers > 0:
            point = random.randint(1,6)
            points.append(point)
            numbers -= 1
        total = sum(points)
        return total

    #定义函数根据学习币值确定试卷名称
    def paper_name(total):
        '''
        输入
        -------------
        total:学习币值

        输出
        -------------
        name:试卷名称(A卷/B卷)，超出有效范围返回None
        '''
        if 3 <= total <= 10:
            return 'A卷'
        elif 11 <= total <= 18:
            return 'B卷'
        return None

    #定义抽取试卷函数
    def rule(total):
        print('全部试卷文件有:','/'.join(os.listdir('../data/试卷')))
        name = Test_Paper.paper_name(total)
        if name is None:
            print('学习币值超出有效范围(3~18)，无法抽取试卷！')
            return None
        with open('../data/试卷/' + name + '.csv','r',encoding=('UTF-8-sig')) as f:
            reader = csv.reader(f)
            #过滤掉空行，保证题号和题目一一对应
            volume = [row for row in reader if row and row[0].strip()]
            print('------正在抽取' + name + '------')
        return volume

    #定义函数获取试卷的标准答案
    def standard_answer(total):
        '''
        输入
        -------------
        total:学习币值(决定抽到哪一套卷子)

        输出
        -------------
        answers:标准答案列表，如['正确','错误',...]，与试卷题目一一对应
        '''
        name = Test_Paper.paper_name(total)
        if name is None:
            return []
        path = '../data/试卷答案/' + name + '答案.csv'
        with open(path,'r',encoding=('UTF-8-sig')) as f:
            reader = csv.reader(f)
            rows = [row for row in reader if row and row[0].strip()]
        answers = []
        #第一行是表头(题目,答案)，从第二行开始取标准答案
        for row in rows[1:]:
            if len(row) >= 2:
                answers.append(row[1].strip())
            else:
                answers.append('')
        return answers
