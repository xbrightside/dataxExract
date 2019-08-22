import requests
import numpy as np
import pandas as pd

re_df = pd.DataFrame(getRequirmentData())
test_df = pd.DataFrame(getTestTasksData())
df = test_df.merge(re_df, left_on='UnionReID', right_on='ReId')[['TestModuleID','TestName','BusiLeaderList','JiraId','ImDeveloperList','TestLeaderList','TestPhase','CreateTime','ReUrl']]
processData(df)

def getRequirmentData():
	#获取正常状态的需求列表
	r = requests.post("http://40.24.95.52:57710/display/AnalysisProxy", 
		data = {"ProxyTransId":"PMQueryRequireList", "noLogin": "Y", "ReStatus": "1"})
	return r.json()['ResultMap']['ReList']
	
def getTestTasksData():
	r = requests.post("http://40.24.95.52:57710/display/AnalysisProxy", 
		data = {"ProxyTransId":"PMTestJobList", "noLogin": "Y","TestPhase":"01|02|03|04|05|06|08|07|09"})
	return r.json()['ResultMap']['TestList']
	
def processData(df):
	#阶段名转义
	df['TestPhase'] = df['TestPhase'].apply(renameTestPhase)
	df['TestModuleID'] = df['TestModuleID'].apply(renameTestModuleID)
	origin = ['TestModuleID','TestName','BusiLeaderList','JiraId','ImDeveloperList','TestLeaderList','TestPhase','CreateTime','ReUrl']
	tag = ['发起模块','任务名称','业务负责人','Jira号','开发负责人','测试负责人','任务状态','提测时间','需求链接']
	df.rename(columns={x:y for x,y in zip(origin,tag)}, inplace=True)
	df1 = df.groupby(['发起模块','任务名称']).sum()
	df1['业务负责人'] = df1['业务负责人'].apply(listToStr)
	df1['开发负责人'] = df1['开发负责人'].apply(listToStr)
	df1['测试负责人'] = df1['测试负责人'].apply(listToStr)
	df1.to_excel('test.xlsx')
	
def listToStr(obj):
	if isinstance(obj, list):
		return "|".join(obj)
		
def renameTestPhase(x):
	if x == '01':
		return '提测等待'
	elif x == '02':
		return '案例编写中'
	elif x == '03':
		return '案例编写暂停'
	elif x == '04':
		return 'UAT测试'
	elif x == '05':
		return 'UAT测试暂停'
	elif x == '06':
		return 'UAT测试完成'
	elif x == '07':
		return '版本机测试'
	elif x == '08':
		return '版本机暂停'
	elif x == '09':
		return '版本机测试完成'
	elif x == '10':
		return '已上线'

def renameTestModuleID(x):
	if x == '01':
		return '后管'
	elif x == '02':
		return '电子账户'
	elif x == '03' | x == '04' | x == '05'| x == '11' | x == '16':
		return '渠道'
	elif x == '07':
		return '慧选宝'
	elif x == '08':
		return '质押贷'
	elif x == '09':
		return '贷款'
	elif x == '10':
		return '营销活动'
	elif x == '12':
		return '银行理财'
	elif x == '14':
		return '第三方商户平台'
	elif x == '17':
		return '如意宝'
	elif x == '19':
		return '新多利'
	elif x == '22':
		return '金融云服务平台'