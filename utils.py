from Parameter import *
import math
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import time
import string
import jieba
import jieba.posseg as pseg

all_des = N_selector.match("名称")

def rad(d):
    return d * pi / 180.0

def print_detailed_info(mc):
    """
    打印景区详细信息
    :param mc:景区名称
    :return:返回详细信息(string)
    """
    node_des = N_selector.match("名称", name=mc).first()
    location = (R_selector.match((node_des,), "地址").first()).end_node['name']

    R_type = R_selector.match((node_des,), "名称2类型")
    type=" "
    for r in R_type:
        type= type +"#"+ r.end_node['name']
    level= (R_selector.match((node_des,), "级别").first()).end_node['name']
    ticket= (R_selector.match((node_des,), "票价").first()).end_node['name']
    characteristic= (R_selector.match((node_des,), "介绍").first()).end_node['name']
    monthly_sales= (R_selector.match((node_des,), "月销量").first()).end_node['name']
    picture = (R_selector.match((node_des,), "图片").first()).end_node['name']
    des="名称:"+ mc+"\n类型:"+type+"\n地址:"+location+"\n级别:"+level+"\n票价:"+ticket+"\n月销量:"+monthly_sales+"\n介绍:"+characteristic+"\n图片:"+picture
    return des

def getDistance(lat1, lng1, lat2, lng2):
    """
    :param lat1: 第一个点的纬度(str)
    :param lng1: 第一个点的经度
    :param lat2: 第儿个点的纬度
    :param lng2: 第二个点的经度
    :return: 两个景点间的距离(float)
    """
    lat1=float(lat1)
    lng1=float(lng1)
    lat2=float(lat2)
    lng2=float(lng2)

    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_RADIUS
    return round(s,2)

def inquire_min_distance(mc):
    """
    :param mingcheng: 用户输入的景区名称
    :return: 返回(同省)景区间距离从近到远排序的字典(dict)
    """
    #先得到用户输入景点的经纬度
    NODE_des = N_selector.match("名称", name=mc).first()
    R_lng1 = R_selector.match((NODE_des,), "经度").first()
    R_lat1 = R_selector.match((NODE_des,), "纬度").first()
    lng1 = R_lng1.end_node['name']
    lat1 = R_lat1.end_node['name']
    R_province = R_selector.match((NODE_des,), "省份").first()
    province = R_province.end_node
    R_same_province_des=R_selector.match((province,), "省份2名称")

    des={ }
    for i in R_same_province_des: #i是省份和景点的关系
        #print(i)
        d=i.end_node
        if (d['name'] != mc):
            R_lng2 = R_selector.match((d,), "经度").first()
            R_lat2 = R_selector.match((d,), "纬度").first()
            lng2 = R_lng2.end_node['name']
            lat2 = R_lat2.end_node['name']
            dis=getDistance(lat1, lng1, lat2, lng2)
            if(dis<50):
                des[d['name']]=dis

    des=sorted(des.items(), key=lambda kv: (kv[1], kv[0]))
    des_re= ' '
    for src in des:
        des_re= des_re + str(src) + ' \n '
    return des_re

def inquire_by_province_return_Rselector(province):
    #根据用户输入省份查询景区
    """
    #TODO:触发词：景区，关键词：省份。
    :param mc: 省份
    :return: 景区列表(list)
    """
    N_province=N_selector.match("省份", name=province).first()
    R_des= R_selector.match((N_province,), "省份2名称")
    return R_des



def inquire_by_province_return_list(province):
    #根据用户输入省份查询景区
    """
    #TODO:触发词：景区，关键词：省份。
    :param mc: 省份
    :return: 景区列表(str)
    """
    N_province=N_selector.match("省份", name=province).first()
    R_des= R_selector.match((N_province,), "省份2名称")
    #des=''
    des=set()
    for r in R_des:
        #es=des+r.end_node['name']+'\n'
        des.add(r.end_node['name']+'\n')
    return des



def inquire_by_type(type,rse):
    """
    #TODO:触发词和关键词都设置为类型字符串
    :param type:
    :return:返回某省或全国的(rse==None)的同类景区名称(list)
    """
    if(rse ==None):
        N_type = N_selector.match("类型", name=type).first()
        R_des = R_selector.match((N_type,), "include")
        t_des =set()

        for r in R_des:
            t_des.add(r.end_node['name']+'\n')
        #t3 = time.clock()
        # print("type_block1:%s" % (t2 - t1))
        # print("type_block2:%s" % (t3 - t2))
        return t_des
    else:
        des = set()
        for r in rse:
            #name_province = r.start_node['name']
            Node_des=r.end_node
            des_type_name=R_selector.match((Node_des,),"名称2类型").first().end_node['name']
            if(des_type_name == type):
                des.add(r.end_node['name']+'\n')
            #p_des=inquire_by_province_return_list(name_province)
            #des = t_des & p_des
        return des



def recommand_by_ticket(ticket,rse):
    """
    #TODO:触发词:票价 关键词:数字
    :param ticket:
    :return:   返回景区名称和票价字典(dict)
    """
    des=set()
    if rse!=None:
        for r in rse:
            d= r.end_node
            R_ticket = R_selector.match((d,),"票价").first()
            char_ticket =R_ticket.end_node['name']
            d_ticket=float(char_ticket)
            if d_ticket<=ticket:
                des.add(d['name']+' 票价:'+char_ticket+'\n')
    else:
        for d in all_des:
            R_ticket = R_selector.match((d,),"票价").first()
            char_ticket =R_ticket.end_node['name']
            d_ticket=float(char_ticket)
            if d_ticket<=ticket:
                des.add(d['name']+' 票价:'+char_ticket+'\n')
    return des

def recommand_by_sales(sales,rse):
    des=set()
    if rse !=None:
        for r in rse:
            d =r.end_node
            R_sales = R_selector.match((d,),"月销量").first()
            char_sales =R_sales.end_node['name']
            d_sales=int(char_sales)
            if d_sales>=sales:
                des.add(d['name'] + ' 月销量:' + char_sales + '\n')
    else:
        for d in all_des:
            R_sales = R_selector.match((d,), "月销量").first()
            char_sales = R_sales.end_node['name']
            d_sales = int(char_sales)
            if d_sales >= sales:
                des.add(d['name'] + ' 月销量:' + char_sales + '\n')
    return des



# def recommand_by_province(mc):
#     """
#     #TODO:触发词:"省份"；关键词："景点"
#     :param province:
#     :return:
#     """
#     N_des = N_selector.match("名称",name = mc).first()
#     R_des_pro = R_selector.match((N_des,), "省份").first()
#     province = R_des_pro.end_node['name']
#     N_province = N_selector.match("省份", name=province).first()
#     R_des = R_selector.match((N_province,), "省份2名称")
#     des = []
#     for r in R_des:
#         des.append(r.end_node['name'])
#     return des