# coding=utf-8
import re

def formula_clean(formula):
    """
    所有函数前面加入 "class_name." , 方便回测调用 class的 operator function。
    返回值 string 类型
    """
    class_name = '' 
    str_temp02 = formula.lower()
    str_temp03 = ''
    if str_temp02[0].isalpha():
        str_temp03 +=  class_name + str_temp02[0]
    else:
        str_temp03 +=  str_temp02[0]
    j = 1
    while 1:
        if j >= len(str_temp02):
            break
        elif str_temp02[j].isalpha() and str_temp02[j-1].isalpha()==False and str_temp02[j-1]!='_':
            str_temp03 +=  class_name + str_temp02[j]
        else:
            str_temp03 += str_temp02[j]
        j += 1
    # 替换？
    while 1:
        k = str_temp03.find('?')
        kk = str_temp03.find('?')
        if k>0:
            str_temp03 = str_temp03[0:k] + ',' + str_temp03[k+1:]
        else:
            break
        count = 0
        while (k>0):
            k -=1
            if str_temp03[k] == ')':
                count += 1
            elif str_temp03[k] == '(':
                count -= 1
            if count == 0 and k != kk -1:
                str_temp03 = str_temp03[0:k-1] + class_name + 'cond_expr' + str_temp03[k-1:]
                print('formula 有(cond? expr1: expr2)表达式')
                break
    str_temp03 = str_temp03.replace(':',',')
    # 替换||
    while 1:
        k = str_temp03.find('||')
        kk = str_temp03.find('||')
        if k>0:
            str_temp03 = str_temp03[0:k] + ', ' + str_temp03[k+2:]
        else:
            break
        count = 0
        while (k>0):
            k -=1
            if str_temp03[k] == ')':
                count += 1
            elif str_temp03[k] == '(':
                count -= 1
            if count == 0 and k != kk -1:
                str_temp03 = str_temp03[0:k-1] + class_name + 'or_expr' + str_temp03[k-1:]
                print('formula 有cond_a || cond_b表达式')
                break
    # 替换adv -> adv()
    str_temp03 = re.sub(r'(adv)(\d+)', '\g<1>(\g<2>)', str_temp03)
    # 替换 ^ -> **
    str_temp03 = str_temp03.replace('^', '**')
    #检查公式的括号的对称性：
    count = 0
    for k in range(0,len(str_temp03)):
        if str_temp03[k] =='(':
            count += 1
        elif str_temp03[k] == ')':
            count -= 1
    if count != 0:
        print('公式( and ) 不对齐')
    else:
        print('公式( and ) 已经全部对齐')
    return str_temp03
