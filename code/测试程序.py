import csv
import os
import sys
from test_paper import Test_Paper

#原成绩单
SCORE_FILE = '../data/成绩.csv'
#更新后的成绩单
NEW_SCORE_FILE = '../tmp/更新后的成绩单.csv'
#每题分值
EACH_SCORE = 10


#提取学生名字
def extract_name(text):
    '''
    输入
    -------------
    text:学生输入的原始字符串

    输出
    -------------
    name:去掉首尾及多余的空白后的姓名，若为空说明输入无效
    '''
    name = text.replace('\u3000', ' ')   #全角空格转成普通空格
    name = ' '.join(name.split())       #去掉首尾空格并合并中间多余空格
    return name


#交互式获取学生名字
def get_name():
    while True:
        name = extract_name(input('请输入名字:'))
        if name:
            return name
        print('尚未输入，请重新输入名字:')


#计算成绩
def calculate_score(answers, standard):
    '''
    输入
    -------------
    answers:学生作答列表
    standard:标准答案列表

    输出
    -------------
    score:总得分(每答对一题得10分)
    '''
    score = 0
    for i, std in enumerate(standard):
        if i < len(answers) and answers[i] == std:
            score += EACH_SCORE
    return score


#查看成绩和标准答案
def show_result(answers, standard, score):
    print('\n------成绩与标准答案------')
    right = 0
    for i, std in enumerate(standard):
        my = answers[i] if i < len(answers) else '未作答'
        if my == std:
            right += 1
        print('第' + str(i + 1) + '题 | 我的答案:' + my +
              ' | 标准答案:' + std + ' | ' + ('正确' if my == std else '错误'))
    print('总题数:' + str(len(standard)) + ' 答对:' + str(right) +
          ' 答错:' + str(len(standard) - right) + ' 得分:' + str(score))


#读取原成绩单(自动兼容utf-8/utf-8-sig/gbk等编码，避免乱码或报错)
def read_score_rows():
    '''
    输出
    -------------
    rows:原成绩单的所有数据行
    '''
    if not os.path.exists(SCORE_FILE):
        return []
    for enc in ('UTF-8-sig', 'GBK', 'UTF-8'):
        try:
            with open(SCORE_FILE, 'r', encoding=enc, newline='') as f:
                return [row for row in csv.reader(f)]
        except UnicodeDecodeError:
            continue
    return []


#更新成绩单，写入csv文件
def update_score_file(name, score):
    '''
    输入
    -------------
    name:学生姓名
    score:本次得分

    输出
    -------------
    path:更新后成绩单的保存路径
    '''
    rows = [['姓名', '成绩']]
    for row in read_score_rows():
        if not row or not row[0].strip():
            continue
        if row[0].strip() == '姓名':   #表头最后统一写入
            continue
        rows.append([row[0].strip(), row[1].strip() if len(row) > 1 else '0'])
    #已有该学生则更新成绩，否则追加到末尾
    updated = False
    for row in rows[1:]:
        if row[0] == name:
            row[1] = str(score)
            updated = True
            print('成绩单中已存在学生[' + name + ']，成绩已更新为:' + str(score))
            break
    if not updated:
        rows.append([name, str(score)])
        print('新学生[' + name + ']，已添加到成绩单中')
    #写入csv文件(使用utf-8-sig带BOM，Excel双击打开不会乱码)
    folder = os.path.dirname(NEW_SCORE_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(NEW_SCORE_FILE, 'w', encoding=('utf-8-sig'), newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return NEW_SCORE_FILE


def main():
    total = Test_Paper.learning_coin()
    print('学习币值为:',total)
    topics = Test_Paper.rule(total)
    print('------试卷抽取完毕-------')
    if not topics:
        sys.exit('学习币值不在有效范围内(3~18)，本次测试无法进行！')
    print('试卷内容为:',topics)

    #获取试卷的标准答案
    standard = Test_Paper.standard_answer(total)
    print('本卷共有' + str(len(topics)) + '题，标准答案为:',standard)

    print('\n------测试开始-------')
    #提取学生名字
    new_name = get_name()
    print('学生名字:',new_name)

    answers = []
    tp = 0
    try:
        while tp < len(topics):
            print('第' + str(tp + 1) + '题:' + ' '.join(topics[tp]))
            answer = input('请输入第' + str(tp+1)+'题的答案(注意输入格式为"正确"或"错误"):').strip()
            print('\n')
            if answer == '正确' or answer == '错误':
                answers.append(answer)
                tp += 1
            else:
                print('输入格式有误，请重新审题并按正确格式作答。\n')
    except:
        print(' ')

    #计算成绩并查看成绩和标准答案
    score = calculate_score(answers, standard)
    show_result(answers, standard, score)

    #更新成绩单，写入csv文件
    path = update_score_file(new_name, score)
    print('\n更新后的成绩单已写入文件:',path)


if __name__ == '__main__':
    main()
