import sys ,os,re
import xlwings as xw

#保留字
key_word = ['abstract','assert','boolean','break','byte',
			'case','catch','char','class','const',
			'continue','default','do','double','else',
			'enum','extends','final','finally','float',
			'for','goto','if','implements','import',
			'instanceof','int','interface','long','native',
			'new','package','private','protected','public',
			'return','short','static','strictfp','super',
			'switch','synchronized','this','throw','throws',
			'transient','try','void','volatile','while']
#界符
delimiters = ['{','}','[',']','(',')','.',',',':',';']
#运算符
operator = ['+','-','*','/','%','++','--','+=','-=','+=','/=',#算术运算符
			'==','!=','>','<','>=','<=',#关系运算符
			'&','|','^','~','<<','>>','>>>',#位运算符
			'&&','||','!',#逻辑运算符
			'=','+=','-=','*=','/=','%=','<<=','>>=','&=','^=','|=',#赋值运算符
			'?:']#条件运算符
#标识符
identifier = []
#常数
number = []
token = []
#查找保留字
def searchReserve(word):
	return True if word in key_word  else False
#预处理
def filterResource(file,new_file):
	f2 = open(new_file,'w+')
	txt  =  ''.join(open(file,'r').readlines())
	deal_txt = re.sub(r'\/\*[\s\S]*\*\/|\/\/.*','',txt) 
	for line in deal_txt.split('\n'):
			line = line.strip()
			line = line.replace('\\t','')
			line = line.replace('\\n','')
			if not line:
				continue
			else:
				f2.write(line+'\n')
	f2.close()
	return sys.path[0]+'\\'+ new_file
# 扫描
def Scan(file):
	lines = open(file,'r').readlines()
	for line in lines:
		word = ''
		word_line = []
		i = 0
		while i <len(line):
			word +=line[i]
			if line[i]==' ' or  line[i] in delimiters or line[i] in operator:
				if word[0].isalpha() or word[0]=='$' or word[0]=='_':
					word = word[:-1]
					if searchReserve(word):
						# 保留字
						word_line.append({word[:-1]:key_word.index(word)})
					else:
						# 标识符
						identifier.append({word:-2})
						word_line.append({word:-2})
				# 常数
				elif word[:-1].isdigit():
					word_line.append({word:-1})
				#else:
					#error_word.append(word)
				# 字符是界符
				if line[i] in delimiters:
					word_line.append({line[i]:len(key_word)+delimiters.index(line[i])})
				# 字符是运算符
				elif line[i] in operator:
					s = line[i] +line[i+1]
					if s in operator:
						word_line.append({s:len(key_word)+len(delimiters)+operator.index(s)})
						i +=1
					else:
						word_line.append({line[i]:len(key_word)+len(delimiters)+operator.index(line[i])})
				word = ''
			i+=1
		token.append(word_line)
def check(number):
	hanzi = ''
	q = len(key_word)
	w = len(delimiters)
	e = len(operator)
	if 0<number<=q:
		hanzi = '保留字'
	elif q<number <= q+w:
		hanzi = '界符'
	elif q+w<number <=q+w+e:
		hanzi = '运算符'
	elif number == -1:
		hanzi ='常数'
	elif number == -2:
		hanzi ='标识符'
	return hanzi


