from tkinter import * 
from tkinter.filedialog import askdirectory,askopenfilename
import java_analysis
import xlwings as xw
def openfiles():
	fname = askopenfilename(title='打开文件', filetypes=[('All Files', '*')])
	path.set(fname)

def open_excel():
	# 预处理
	row,col=0,0
	if path.get()!='':

		txt = java_analysis.filterResource(path.get(),new_file)
		print(txt)
		#扫描
		java_analysis.Scan(txt)
		app = xw.App(visible=True,add_book=False)
		wb =app.books.open(sys.path[0]+'\\'+'test.xlsx')
		sheet = wb.sheets.active
		sheet.clear() 
		print(java_analysis.token)
		for i in range(len(java_analysis.token)):
			sheet[row,0].value = '第'+str(i+1)+'行'
			row +=1
			for word in java_analysis.token[i]:
				for k,w in word.items():
					sheet[row,3].value = k
					sheet[row,5].value = w
					sheet[row,7].value = java_analysis.check(w)
				row +=1
		sheet.autofit()#整个sheet自动调整
		#wb.save()
	
if __name__ == "__main__":
	new_file = 'test1.txt'
	root = Tk()
	root.title('词法分析')
	root.resizable(0, 0)
	path = StringVar() 
	Label(root,text = "目标路径:").grid(row = 0, column = 0) 
	Entry(root, textvariable = path).grid(row = 0, column = 1) 
	Button(root, text = "路径选择", command = openfiles).grid(row = 0, column = 2)
	Button(root,text='词法分析',command= open_excel).grid(row = 0,column = 3)
	root.mainloop()
	