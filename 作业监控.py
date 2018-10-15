
import pytesser3 as pytesser
import numpy
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
import json
import os, shutil, tarfile
from PIL import Image
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

sender = 'yangxiaodong@unionpay.com'
receivers = ["wangkun@unionpay.com","huangtingting@fulan.com.cn","lingnan@unionpay.com","dongyibo@unionpay.com","hdgan@unionpay.com","huanghaiyu@unionpay.com","huangkai@unionpay.com","jiemengming@unionpay.com","lishuying1@unionpay.com","liwei9@unionpay.com","yjlu@unionpay.com","zspeng@unionpay.com","rongjia@unionpay.com","shenlinxiang@unionpay.com","tongpeng@unionpay.com","xiejiao@unionpay.com","zhangjiannan@unionpay.com","zhengtingting@unionpay.com","zhaoyanyang@unionpay.com","yangxiaodong@unionpay.com","yudongyi@unionpay.com","huangjian@unionpay.com","sunchuang@unionpay.com","xieyi@unionpay.com","haoyan@unionpay.com","lijin1@unionpay.com","wangqiang3@unionpay.com","xufangcheng1@unionpay.com","guliqiu@unionpay.com","yutao@unionpay.com","shijingfen@fulan.com.cn",]


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') ))

def sendEmail(str):
    from_addr = sender
    password = "1234qwer!"
    to_reciver = receivers
    #to_reciver = ["yangxiaodong@unionpay.com","shijingfen@fulan.com.cn"]
    cc_reciver = ["libeixuan@unionpay.com","lfyu@unionpay.com","yuwenqing@unionpay.com","tangyunji@unionpay.com",]
    #cc_reciver = []
    smtp_server = "mail.unionpay.com"
    msg = MIMEText(str, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(to_reciver)
    msg['Cc'] = ";".join(cc_reciver)
    msg['Subject'] = Header(u'服务单、服务工单和问题单自动化检查作业', 'utf-8').encode()

    reciver = to_reciver + cc_reciver
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, reciver, msg.as_string())
    server.quit()

def sendAutoEmail(str):
    str=""
    from_addr = sender
    password = "1234qwer!"
    to_reciver = receivers
    cc_reciver = ["libeixuan@unionpay.com","lfyu@unionpay.com","yuwenqing@unionpay.com","tangyunji@unionpay.com",]

    smtp_server = "mail.unionpay.com"
    msg = MIMEText(str, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(to_reciver)
    msg['Cc'] = ";".join(cc_reciver)
    msg['Subject'] = Header(u'应用一室生产环境规范性处理要求提醒（请大家认真学习和遵守）', 'utf-8').encode()

    reciver = to_reciver + cc_reciver
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, reciver, msg.as_string())
    server.quit()




s = requests.Session()
login_url="http://172.16.5.12:10060/sso/login"
data_url="http://172.16.5.12:10060/sso/login;jsessionid=w3NM4nCLr+NZtF835v4D6t+h?service=http://172.16.5.12:30000/HomePage.aspx&sysIdStr=59676A88C793508EDB7D3EEAAD319E5C"
incident_url="http://172.16.5.12:30000/_layouts/UOSP_Resources/ExtPages/INC/INC.ashx"
#incident_url="http://172.16.5.12:30000/_controltemplates/Pages/Incident/SearchIncident.aspx"
servicedir="http://172.16.5.12:33000/uosp/srv/operation/tblsrvServiceOrderAction_queryFindServiceorder.action"
workdir="http://172.16.5.12:33000/uosp/srv/operation/tblSrvWorkOrderAction_search.action"
servicedetail="http://172.16.5.12:33000/uosp/srv/operation/tblsrvServiceOrderAction_queryService.action"
servicelogin_url="http://172.16.5.12:33000/uosp/srv/operation/tblsrvServiceOrderAction_queryFindServiceorder.action"
startTime="2018-08-05 00:00:00"
endTime="2018-08-21 00:00:00"


def to_str(day):
    if(day<10 and day>0):
        return "0"+str(day)
    if(day <=0 ):
        day=(day+30)%31
        return to_str(day)
    return str(day)

def getday():
    year = time.strftime('%Y',time.localtime())
    month = time.strftime('%m',time.localtime())
    day = time.strftime('%d',time.localtime())
    srv_end=year+"-"+month+"-"+day
    srv_start=year+"-"+month+"-"+to_str(int(day)-14)
    if(int(day)<14):
        srv_start=year+"-"+to_str(int(month)-1)+"-"+to_str(int(day)-14)
    print(srv_start,srv_end)
    return srv_start,srv_end

#cookie中的default-cookie-name,ASP.NET_SessionId,.ASPXUSERDEMO这三个值必须填

cookie={
        "ASP.NET_SessionId":"vnb2bb55erz5i2bbecahdy55",
        ".ASPXUSERDEMO":"1809D64CD8EB20F830B7EAD8FF64E3E17FCEA496C99B038C5DB388CC320B8ED70E04866E6AEC594AED7DC5923C1FF065BAA6F159039D07D4708217A11459E6BB038E56DD080ABAC461424E64C43E6807736DF7BA4253BBAF864EC11E0492CAEED9899CAA0289A299D3F62084198ADC4CE1854546083F089E0472448C9F255D8D4B993C5E687C0A80DA343FB2FE5E6040535F4833C76BD7C60832EA0AA3EEF50B24838F78A32B412A88D09560ADEF44C9706F7027D8C860D3E959D319DC8774425BE6E5665DBA44A4FC0B4E4810CC3E0D898953DAAAC19305B53690B39D90794C51C6F2303C1B364E05FFBD30D986E3D98BD7D811CFBC62DE105153881576947CFE2528E96543B7EEFA2A8BF9860D31D321D147C5079C10E3134B78F98D544E515613D2EB8070F1189E46DEF128FAFA83B07BA6883D5D595EF07534EA8DB8A25743EDB884C8BBFDAC0C0901BE6BAB1321545D9F6988F1384079DD9DC3AA576BD4F80D4186DEF971ABE55D5E493ABC91FD2D159A3F60BC1C008330C42C7123B63F4A15676E2E2DC641FC19B3680E68F6ED8DD59BA0C7AFC572E8CD6D43A98903D168149F11D9D34784C8B09165F5C7A9B1D4592B6B015B3A32EE3F931AEF0B0D4818B3BC4497E6ED334592DED59073567E3EA3A4ACE44A92E640E04E6AD50A64A4FE52E5F9EE88F4EE9F21154A20E75CD1DBB42217C14FFC7A8B8F9452E706253208FB1796C59C3E6F663E36A210D39B839B4256DBBA5F204401E7E40190A69408ABABE69E0D092411DB063A8E351D72A100DF49097B3345ED5E840433CC2D5A8C0458DCA7296DB7B7DD55BD23EBF728E30C6099BBF5E01E60C947E97EC8EE8B85F7ADFB72DDEF027C7F7F651AB0946A31209ABC7F01E45624A9C00D98D0BE659969F64AE84251F0774A6482B7583F2C0E4135DD4F51DAF6DCA837C02CC92A64B5E3FB9F13FDA858696F3326F878D4C6757ECED268CCC84DFD852A1346F11C451F0B2B26C8B708526D8E9C7620496B8F119BC889400BDF5D827C66C73A40B26ECD15CC9BE8D64E232217D883475C6C08B92926297C69BEF9F5F63517A3339F21CE33DD6C8E41C4DB4039DE2B9D55C6E61BEBE2BD393109D1613C04192A026AAC6705678E3CC3DE53E6129ADD10F41E4CE2C535EC0FB073DCF4C22384C5EF09D0C2BD2F9F8ABD0E11F03CA0FD3E32BACEE3255570737DF5624A17022128CB49B64AEFD63E6A920F2F4B036908C412AB308C02A48E3E8CAAFC7D9F932F88BBA363702F3A39277831E10DCB242B1B849EC66E1D88D3B8011DE4EE1CAFA7EA08C32BF957D1772DEF16A882629F67B6C9A2A29593BDC4F41F9763B428F7FBE5FC8409C6384E2B5A30C8DF84CF5BF9794BDC075C7ECA2B823364A233EB5DC972",
        "cookie-uosp-dof":"kYYT1iT8zcuBQWJ06LxWYXpc",
        "default-cookie-name":"7JC0mJB7cef0enbKssChcpCN",
        "NSC_WT_TTP":"ffffffff920f430445525d5f4f58455e445a4a423660",
        "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE":"zh_CN",
    }




def query_srv_list(s,srv_start,srv_end):
    query_service_req={
        "start":"0",
        "limit":"500",
        "data":'{"ServiceOrderID":null,"AcceptWay":null,"StatusCode":'+'"'+"'iSRV00105'"+'"'+',"Description":null,"OneLevelSortID":null,"TwoLevelSortID":null,"ThreeLevelSortID":null,"FourLevelSortID":null,"AInsNO":null,"ACompanyName":null,"ADepartmentID":null,"ASectionID":null,"AName":null,"CInsNO":null,"CCompanyName":null,"CDepartmentID":null,"CSectionID":null,"CreatorName":null,"HInsNO":"00010000","HCompanyName":"i0001","HDepartmentID":"U000005755","HSectionID":"S000000260","HName":null,"FInsNO":null,"FCompanyName":null,"FDepartmentID":null,"FSectionID":null,"FName":null,"CreateDate1":"'+srv_start+'","CreateDate2":"'+srv_end+'","FinishDate1":null,"FinishDate2":null,"CloseDate1":null,"CloseDate2":null,"UpdateDate1":null,"UpdateDate2":null,"OverDueStatus1":null,"OverDueStatus2":2,"OverDueStatus3":null,"IsNeedLog":0,"DirectoryTypeId":null,"DirectoryId":null,"wophase":null,"MyHandleUserID":null,"isBlue":null}',
        "sort":"serviceOrderId",
        "dir":"DESC",
        "remoteURL":"http://172.16.5.12:33000/uosp/html/srv/operation/Search.html"
    }
    rev=s.post(servicedir,data = query_service_req)
    #print(query_service_req)
    json_rslt=rev.json()
    #print(json_rslt)
    count = len(json_rslt['result'])
    huangdeng_not_wait=[]
    huangdeng_wait=[]
    notify_text=u"\n\r一、服务单检查:\n\r\n\r"
    notify_text=notify_text+u"未置为等待的黄灯服务单检查结果如下:\n\r"
    if(count==0):
        notify_text=notify_text+u"今天没有新增的黄灯服务单。"
        #print(notify_text)
        return notify_text
    print("等待中的黄灯服务单:")
    for i in range(count):
        if(json_rslt['result'][i]['isfreeze']=='1'):
            huangdeng_wait.append(json_rslt['result'][i]['analysePname'])
            huangdeng_wait.append(json_rslt['result'][i]['serviceOrderId'])
            #print(json_rslt['result'][i]['analysePname'],json_rslt['result'][i]['serviceOrderId'])
            #print("等待中的黄灯服务单:",json_rslt['result'][i]['analysePname'],json_rslt['result'][i]['serviceOrderId'])
        if(json_rslt['result'][i]['isfreeze']!='1'):
            huangdeng_not_wait.append(json_rslt['result'][i]['analysePname'])
            huangdeng_not_wait.append(json_rslt['result'][i]['serviceOrderId'])
            #print("未等待中的黄灯服务单:",json_rslt['result'][i]['analysePname'],json_rslt['result'][i]['serviceOrderId'])
    index=0
    if(len(huangdeng_not_wait)==0):
        notify_text=notify_text+u"\n\r截止目前，没有未等待的黄灯服务单。\n\r"
        #print(notify_text)
        return  notify_text
    for srv in huangdeng_not_wait:
        if(index%2==0):
            notify_text=notify_text+"\n\r"
        notify_text=notify_text+srv
    notify_text=notify_text+u"\n\r未置为等待的黄灯服务单检查结束！\n\r"
    #print(notify_text)
    return  notify_text

def query_worker_list(s,srv_start,srv_end):
    query_service_req={
        "start":"0",
        "limit":"200",
        "data":' {"workStatus":"iSRV00201","planstarttime1":'+srv_start+',"planstarttime2":'+srv_end+'}',
        "sort":"serviceWorkOrderId",
        "dir":"DESC",
        "remoteURL":"http://172.16.5.12:33000/uosp/html/srv/operation/Search.html"
    }
    rev=s.post(workdir,data = query_service_req)
    notify_text=u"\n\r\n\r二、服务工单检查:\n\r\n\r"
    notify_text=notify_text+u"应用一岗未点击开始处理的服务工单检查结果如下:\n\r"
    #print(rev.text)
    json_rslt=rev.json()
    count = len(json_rslt['result'])
    result_count=0
    for i in range(count):
        if(u"应用支持一岗" in json_rslt['result'][i]['handlerName']):
            #print("ok",json_rslt['result'][i]['workOrderName'],json_rslt['result'][i]['planStartTime'])
            result_count+=1
            notify_text=notify_text+"\n\r"+json_rslt['result'][i]['serviceWorkOrderId']+" "+(json_rslt['result'][i]['workOrderName']+" "+json_rslt['result'][i]['planStartTime'])
    if(result_count==0):
        notify_text+=u"\n\r截止目前，没有未点击开始处理的服务工单。"
    #print(notify_text)
    return notify_text

def query_overworker_list(s,srv_start,srv_end):
    query_service_req = {
        "start": "0",
        "limit": "500",
        "data": '{"handlerInscode":"00010000","handlerDeps":"U000005755","handlerSects":"S000000260","planfinishtime1":' + srv_start + ',"planfinishtime2":' + srv_end + '}',
        #"data": '{"handlerInscode":"00019999","handlerSects":"S000000575","planfinishtime1":' + srv_start + ',"planfinishtime2":' + srv_end + '}',
        "sort": "serviceWorkOrderId",
        "dir": "DESC",
        "remoteURL": "http://172.16.5.12:33000/uosp/html/srv/operation/Search.html"
    }
    #print(query_service_req)
    rev = s.post(workdir, cookies=cookie, data=query_service_req)
    notify_text = u"\n\r\n\r即将到期的外部服务工单检查结果如下:\n\r"
    #print(rev.text)
    json_rslt = rev.json()
    count = len(json_rslt['result'])
    result_count = 0
    print(count)
    #print(str(json_rslt['result']))
    for i in range(count):
        #print(json_rslt['result'][i]['serviceWorkOrderId'])
        if("00010000" in json_rslt['result'][i]['createUserid'] or "iSRV00203" in json_rslt['result'][i]['status'] or "iSRV00203" not in json_rslt['result'][i]['status']):
            continue
        #if ("U000005755" not in json_rslt['result'][i]['createUserSubCompanyId'] and "iSRV00203" not in json_rslt['result'][i]['status'] and "iSRV00206" not in json_rslt['result'][i]['status']):
        if ("0120" not in json_rslt['result'][i]['createUserid'] and "iSRV00205" not in json_rslt['result'][i]['status']):
            otime=json_rslt['result'][i]['reqFinishTimeOla']
            otime=otime.replace("T"," ")
            now=time.time()
            otime_unix=int(time.mktime(time.strptime(otime, '%Y-%m-%d %H:%M:%S')))
#            print(otime_unix-now)/86400.0
            if(otime_unix-now<86400 and otime_unix-now>0):
                continue
            result_count += 1
            notify_text = notify_text + "\n\r" + (
            json_rslt['result'][i]['serviceWorkOrderId'] + " " + json_rslt['result'][i]['handlerName']+" "+json_rslt['result'][i]['workOrderName'] + " OLA时间" +
            json_rslt['result'][i]['reqFinishTimeOla'])
    if (result_count == 0):
        notify_text += u"\n\r截止目前，没有即将到期的外部服务工单。"
    #print(notify_text)
    return notify_text


def query_wtd_list(s,begintime,endtime):
    rlogs=u"\n\r\n\r三、问题单检查:\n\r\n\r"
    rlogs=rlogs+u"问题单检查结果如下:\n\r"
    wtd_url="http://172.16.5.12:30000/_layouts/UOSP_Resources/ExtPages/PBI/PBI.ashx"
    queryByTime_data = {
        "action": "SearchProblem",
        "data": '{"ProblemID":"","ProblemSummary":"","ProblemDesc":"","OneLevelSortID":"","TwoLevelSortID":"","ThreeLevelSortID":"","EnvironmentCode":"","AreaCode":"","ProblemStatusCode":"","StatusReason":"","SourceTypeCode":"","PriorityCode":"","AnalystGroupID":"","AnalystName":"","DepartmentID":"D001","SectionID":"S002","SectionID_Creator":"","CreatorName":"","DateType":"1","StepA":"","StepB":"","StepDetail":"","IndexValue":"","StartDate":"'+begintime+'","EndDate":"'+endtime+'T23:59:59"}',
        "dir": "desc",
        "limit": 500,
        "sort": "ProblemID",
        "start": 0
    }
    rev = s.post(wtd_url, data=queryByTime_data)
    #print(rev.text)
    json_rslt = rev.json()
    count = json_rslt['Count']
    #print(count)
    for i in range(0,count):
        #print(json_rslt['Data'][i]['ProblemSummary'])
        #print(json_rslt['Data'][i]['ProblemStatusCode'])
        #case1:问题单未接单处理
        ctimestamp = json_rslt['Data'][i]['CreateDate'].split('(')[1].split('+')[0]
        timestamp = int(ctimestamp[0:-3])
        cur_timestamp = time.time()
        lasttime = cur_timestamp - timestamp
        #print(json_rslt['Data'][i]['ProblemID'])
        if(u"已分派" in json_rslt['Data'][i]['ProblemStatusCode']):
            if(lasttime>86400.0):
                rlogs=rlogs+json_rslt['Data'][i]['AnalystName']
                #print(rlogs)
                rlogs = rlogs +(u"问题单未及时接单,"+" "+u"问题单号：")
                rlogs = rlogs +(json_rslt['Data'][i]['ProblemID'])
                rlogs=rlogs+"\n\r"
            continue
        #case2：手册 解决延迟 u"手册" in json_rslt['Data'][i]['ProblemSummary'] or
        if(json_rslt['Data'][i]['ThreeLevelSortName'] in (u"应急手册",u"桌面演练")):
            if (json_rslt['Data'][i]['ProblemStatusCode'] not in (u"已解决",u"已关闭") and lasttime > 86400.0):
                rlogs = rlogs +(json_rslt['Data'][i]['AnalystName'])
                rlogs = rlogs +(u"应急手册2天未解决," + " " + "问题单号：")
                rlogs = rlogs +(json_rslt['Data'][i]['ProblemID'])
                rlogs = rlogs + "\n\r"
            continue
        #case3：日志更新慢的问题
        logs=query_wtd_log(s,json_rslt['Data'][i]['ProblemID'])
        #print(logs)
        if(len(logs)==0 and lasttime>259200.0):
            rlogs = rlogs +(json_rslt['Data'][i]['AnalystName'])
            rlogs = rlogs +(u"问题单3天未写日志，分析内容未及时明确," + " " + "问题单号：")
            rlogs = rlogs +(json_rslt ['Data'][i]['ProblemID'])
            rlogs = rlogs + "\n\r"
            continue
        if(len(logs)==0 ):
            continue
        log1time = (int)(logs[-1]['CreateDate'].split('(')[1].split('+')[0][0:-3])
        log2time = timestamp
        if(len(logs)>1):
            log2time=(int)(logs[-2]['CreateDate'].split('(')[1].split('+')[0][0:-3])
        interval_time= abs(log1time - log2time)
        if(interval_time>1209600.00):
            rlogs = rlogs +(json_rslt['Data'][i]['AnalystName'])
            rlogs = rlogs +(u"问题单日志2周未及时更新," + " " + "问题单号：")
            rlogs = rlogs +(json_rslt['Data'][i]['ProblemID'])
            rlogs = rlogs + "\n\r"
    if(u"问题单号" not in rlogs):
        rlogs=rlogs+u"\n\r无不作为问题单\n\r"
    return rlogs

def query_wtd_log(s,wtd_id):
    wtd_url="http://172.16.5.12:30000/_layouts/UOSP_Resources/ExtPages/Public/Public.ashx"
    query_data = {
        "action": "GetWorkLogByFormID",
        "id": wtd_id,
    }
    rev = s.post(wtd_url, data=query_data)
    json_rslt = rev.json()
    return json_rslt

def query_wtd_detail(s,wtd_id):
    wtd_url="http://172.16.5.12:30000/_layouts/UOSP_Resources/ExtPages/PBI/PBI.ashx"
    query_data = {
        "action": "GetPBIInfoByID",
        "id": wtd_id,
    }
    rev = s.post(wtd_url, data=query_data)
    json_rslt = rev.json()
    #print(json_rslt)

#notify_srv=query_srv_list()
#sendEmail(notify_srv)


def query_inc_time():
    queryByTime_data = {
        "action":"GetIncidentAdvancedSearch",
        "data":'{"IncidentID":null,"IncidentSummary":null,"IncidentDesc":null,"UmpEventID":null,"SourceTypeCode":null,"PriorityCode":"4","OneLevelSortID":null,"TwoLevelSortID":null,"ThreeLevelSortID":null,"AnalystAreaCode":"D001","AnalystGroupID":"R0439","AnalystID":null,"CreatorID":null,"EnvironmentTypeCode":null,"AreaCode":null,"RequestorID":null,"IncidentStatusCode":null,"IsCheckedMyDealWith":false,"StatusReason":null,"CurSubcID":"U0001","CurDeptID":"D001","CreateDate1":null,"CreateDate2":null,"ActualEmergeTime1":"'+startTime+'","ActualEmergeTime2":"'+endTime+'","CloseDate1":null,"CloseDate2":null,"StartToHandleDate1":null,"StartToHandleDate2":null,"SolveDate1":null,"SolveDate2":null,"LastUpdateDate1":null,"LastUpdateDate2":null,"ResTime1":null,"ResTime2":null}',    "dir":"desc",
        "limit":20,
        "sort":"IncidentID",
        "start":0
    }
    rev=s.post(incident_url,cookies=cookie,data = queryByTime_data)
    #print(rev.text)
    json_rslt=rev.json()
    #print(json_rslt)

def query_inc_detail():
    form_data={
    "action":"GetINCInfoByID",
    "id":"INC000287932",
    }
    rev=s.post(incident_url,cookies=cookie,data = form_data)
    #print(rev.text)
    json_rslt=rev.json()
    #print(json_rslt[0]['IncidentSummary'])

def get_code(img):
    """
    读取验证码图片文件获得验证码
    :param img: 验证码图片文件
    :return: validateCode: 解析的验证码
    """
    SPLIT_VALUE = 30  # 噪音过滤条件
    WHITE_VALUE = 255  # 白色的RGB颜色
    box = (4, 4, 68, 26)
    img = img.crop(box)
    img = img.convert("L")  # 灰度转换
    img.save('before.jpg')
    array = numpy.array(img)  # 转换成numpy数组便于运算
    array[array > SPLIT_VALUE] = WHITE_VALUE  # np进行过滤
    cimg = Image.fromarray(array)  # 优化后的数组变成图片
    cimg.save('after.jpg')
    textcode = pytesser.image_to_string(cimg)  # 使用pytesser转换图片
    validateCode = textcode.strip().replace(' ', '')  # 将空格剔除掉
    return validateCode



def auto_login():
    s = requests.Session()
    r = s.get(login_url)
    bs = BeautifulSoup(r.text,'html.parser')
    image = bs.find("img", {"id": "vcJpeg"})['src']
    lt_data = bs.find("input", {"name": "lt"})['value']
    csr_data = bs.find("input", {"name": "csrftoken"})['value']
    sec_data = bs.find("input", {"name": "sec"})['value']
    #print(lt_data,",",csr_data,",",sec_data)
    rootdir="http://172.16.5.12:10060"
    ir = s.get(rootdir+image)
    if ir.status_code == 200:
        with open('valid.jpg', 'wb') as f:
            f.write(ir.content);
            f.close();
        validateCode = get_code(Image.open('valid.jpg'))  # 通过本地图片解析验证码
        print(validateCode)
    postdata={
        'csrftoken': csr_data,
        'username': '01203624',
        'password': 'culgp@123',
        'institute': '00010000',
        'validateCode': validateCode,
        'lt': lt_data,
        'sec': sec_data,
        'dn': '',
        'ip': '145.4.33.12',
        '_eventId':'submit',
    }
    form_data={
        "action":"GetINCInfoByID",
        "id":"INC000287932",
    }
    s.post(login_url,data = postdata)
    s.post(incident_url,data = form_data)
    s.post(servicelogin_url)
    cookies_dict = requests.utils.dict_from_cookiejar(s.cookies)  # 登录后页面的cookie转化为dict
    #print("cookies is that ",cookies_dict)
    if ('.ASPXUSERDEMO' in  cookies_dict):  # 如果登录成功，cookie中会有.ASPXUSERDEMO字段值
        cookies = open('login_cookies', 'w')
        cookies.write(str(cookies_dict))  # 将cookie信息写入本地文件，其他模块直接访问文件可以绕过登录
        cookies.close()
        return s
    else:
            return None


if __name__ == "__main__":
    for i in range(20):
        session = auto_login()
        if session:
            print("success login in!")
            break
        else:
            #print(u"第" + str(i) + u'次登陆失败！')
            if i == 19:
                print(u'登录失败！')
    srv_start,srv_end=getday()
    notify_srv=query_srv_list(session,srv_start,srv_end)
    notify_work=query_worker_list(session,srv_end,srv_end)
    notify_wtd=query_wtd_list(session,srv_start,srv_end)
    notify_srw=query_overworker_list(session,srv_start,srv_end)
    print(notify_srv)
    print(notify_work)
    print(notify_srw)
    print(notify_wtd)
    notify=u"注：检查周期："
    notify=notify+srv_start+" - "+srv_end+notify_srv+notify_work+notify_srw+notify_wtd
    print("邮件内容")
    print(notify)
    sendEmail(notify)
