from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import utils
import time
import jieba
import jieba.posseg as pseg
graph = Graph(
    "http://localhost:7474",
    password="200171"
)

N_selector = NodeMatcher(graph)
R_selector = RelationshipMatcher(graph)

all_des = N_selector.match("名称")



def min_distance(mc):
    """

    :param mingcheng: 用户输入的景区名称
    :return: 返回距离从近到远排序的字典
    """
    #先得到用户输入景点的经纬度
    NODE_des = N_selector.match("名称", name=mc).first()
    R_lng1 = R_selector.match((NODE_des,), "经度").first()
    R_lat1 = R_selector.match((NODE_des,), "纬度").first()
    lng1 = R_lng1.end_node['name']
    lat1 = R_lat1.end_node['name']
    R_province = R_selector.match((NODE_des,), "省份").first()
    province = R_province.end_node
    R_same_province_des=R_selector.match((province,), "省2名")

    des={ }
    for i in R_same_province_des: #i是省份和景点的关系
        #print(i)
        d=i.end_node
        R_lng2 = R_selector.match((d,), "经度").first()
        R_lat2 = R_selector.match((d,), "纬度").first()
        lng2 = R_lng2.end_node['name']
        lat2 = R_lat2.end_node['name']
        dis=utils.getDistance(lat1, lng1, lat2, lng2)
        des[d['name']]=dis

     print(sorted(des.items(), key=lambda kv: (kv[1], kv[0])))




    #NODE_des = N_selector.match("名称", name = mc ).first()
    #print(lng1['name'])

    #lng1=R_selector.match((NODE_des,), "经度" ).first()
#    lat1=R_selector.match("纬度").where('_.name= mc').first()
    #print(lng1.end_node['name'])
  #  print(lat1)

mingcheng="上海犹太难民纪念馆"
min_distance(mingcheng)

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
