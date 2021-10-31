from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import utils
import classifier
import re
import time
from Parameter import *
import jieba
from flask import Flask
import eventlet

#eventlet.monkey_patch()



app = Flask(__name__)

"""
支持的输入模式:
1."景区"+附近的景区 / "景区"+旁边的景区  ###['安徽大龙山乌龙溪景区', '附近', '的', '景区']/['安徽大龙山乌龙溪景区', '旁边', '的', '景区']
2.(省份)票价50元以下的景区################[ '票价', '70', '元', '以下', '的', '景区'])
3."景区"+详细信息##########################['安徽大龙山乌龙溪景区', '的', '详细信息']
4."(省份)景区类型"##############################['山川', '公园', '农家度假', '古建筑', '游乐场', '展馆', '城市观光', '自然风光', '文化古迹', '运动健身']
5."省份"的景点############################['福建省', '的', '景点']
6."(省份)销量"+500以上的景区####################['(北京)','月销量', '500', '以上', '的', '景点']
"""

"""
若输入中包含省份,一般情况下只有一个省份输入.

"""


#TODO:删除jieba中北京市等


t1=time.clock()
user_input = input()
t2=time.clock()
des_list=None
#with eventlet.Timeout(10, False):
des_list=classifier.classify(user_input)
t3=time.clock()
# for src in des_list:
#     src_result= src_result + src +'\n'
if(type(des_list)==str):
    print(des_list)
elif(type(des_list)==set):
    print(''.join(des_list))
else:
    print("能力一般,水平有限,请您重新输入问题")
t4=time.clock()
print("block1:%s"%(t2-t1))
print("block2:%s"%(t3-t2))
print("block3:%s"%(t4-t3))
#
# #
# @app.route('/')
# def hello_world():
#     if type(des_list) == list:
#         print("good")
#         return "".join(des_list)
#     elif type(des_list) == dict:
#         print("good+22")
#         return "".join(des_list)
#     elif type(des_list) == str:
#         print("good_str")
#         return des_list
#
# if __name__ == '__main__':
#     app.run()
#
#print(des_list)


#exercise:
# jieba.load_userdict("景区名称.txt")
# jieba.load_userdict("景区类型.txt")
# jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持
# words = jieba.cut("安徽大龙山乌龙溪景区旁边的景区",cut_all=False) #paddle模式
# for word in words:
#     print(word)
# assert (0)


# province="北京"
# type ="自然风光"
# ticket=50
# sales=500
#utils.inquire_min_distance(mingcheng)

#utils.print_detailed_info(mingcheng)
# utils.inquire_by_province(province)
# utils.inquire_by_type(type)
# utils.recommand_by_province(mingcheng)
# utils.recommand_by_ticket(ticket)
#utils.recommand_by_sales(sales)
    #NODE_des = N_selector.match("名称", name = mc ).first()
    #print(lng1['name'])

    #lng1=R_selector.match((NODE_des,), "经度" ).first()
#    lat1=R_selector.match("纬度").where('_.name= mc').first()
    #print(lng1.end_node['name'])
  #  print(lat1)



#经纬度提取(将字符串转换为浮点数,精度不够)
# c=selector.match("名称").limit(2)
#
# for b in c:
#d = N_selector.match("名称").where('_.name="上海犹太难民纪念馆"').first()
#print(d['name'])




# print(c[1])
# print(c[2])

# for b in c:
#     d=dict(b)
#     e=d['name']
#     f=float(e)
#     print(f)




# jieba(结巴分词测试)
# str = "慈城孔庙附近的景点"
# words=pseg.cut(str,use_paddle=True)
# for word, flag in words:
#     print('%s %s' % (word, flag))



#
# # 根据热度排序查询:
# # persons = selector.match('名称').order_by('_.热度').skip(10)
# # print(list(persons))
#
# #名字以什么开头的查询
# # c=list(selector.match("类型").where('_.name =~ "山.*"'))
# # print(c)

# coding=utf-8
