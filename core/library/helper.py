from core import app
from flask import url_for
from datetime import datetime, date, time, timedelta


#settime working as global variable but commented for easy identification of this variable using class name 
# global settime
# settime = 5

class Helper:


	def footer_text():
		return "Virtual Conference - 1"	
	#set minutes for timesplitter and rowspan calc
	#settime = 10
# --------------------PROGRAM SHEET FUNCTIONS START------------------------------
	def timesplitter(starttime, endtime):
		fmt = '%H:%M'
		d1 = datetime.strptime(starttime, fmt)
		d2 = datetime.strptime(endtime, fmt)   
		# d1 = datetime.datetime(2019, 1, 1, 10, 0)
		# d2 = datetime.datetime(2019, 1, 1, 11, 0)
		delta = timedelta(minutes=15)
		times = []
		while d1 < d2:
			times.append(d1)
			d1 += delta
		times.append(d2)
		# print(times)

		new_list  =   []
		for i in range(len(times) - 1):
			result = "{} - {}".format(times[i], times[i+1])
			new_list.append(result)                
		# print(new_list)
		return new_list
		# yaxis_list = [] 
		# for i in new_list: 
		#     if i not in yaxis_list: 
		#         yaxis_list.append(i) 
		# print(yaxis_list)
		# return yaxis_list
	
	def date_diff(d1, d2):
		# fmt	= '%H:%M'
		d1		=	date(d1,'%Y, %m, %d')
		d2		=	date(d2,'%Y, %m, %d')   		
		diff	=	str(d1) - str(d2)		
		# print(diff)
		return diff

	def rowspan_calc(starttime, endtime):
		fmt = '%H:%M'
		d1 = datetime.strptime(starttime, fmt)
		d2 = datetime.strptime(endtime, fmt)   
		
		delta = timedelta(minutes=15)
		times = []
		counter = 0 
		while d1 < d2:
			times.append(d1)
			d1 += delta
			counter += 1
			times.append(d2)
		# print(counter)
		return counter

	# def endtime_calc(starttime):    
	# 	d1 = starttime       
	# 	delta = timedelta(minutes=55)    
	# 	d1 += delta            
	# 	return d1


	# to find starttime index
	def find_index(allhalldata, hall, starttime):     
		# print("----Hall Index---")
		# print(hall)
		# print(starttime)
		# data = allhalldata
		a = allhalldata[hall]      # pass hall as index     
		starttime_index =   a.index(str(starttime)) # starttime as index    
		#print(starttime_index)
		return starttime_index


	# to find next starttime pass startindex
	def find_nextstarttime(allhalldata, hall, startindex, dayend):    
		# print('----- HALLS ------')
		# print(hall)
		# print(startindex)
		# print(allhalldata[hall])
		next_startindex     =   startindex + 1             
		a                   =   allhalldata[hall]    
		
		if next_startindex < len(a):    
			newstarttime    =   a[next_startindex]
		elif next_startindex == len(a): 
			newstarttime    =   '23:55'			
		else:                           
			newstarttime    =   dayend
		
		#print(newstarttime)    
		return newstarttime



	def programsheet_html(dictList,final_data,allhalldata,dayend,hall):
		html = ""
		html += '<table id="maintable" class="table table-bordered " data-striped="true">'
		html += '<thead>'
		html += '<tr>'
		html += '<th class="hallcell"></th>'
		column = []
		col_count = {}
		for col in hall:
			col_count[col] =0
			html += '<th class="hallcell" colspan="1">'+col+'</th>'
		html += '</tr>'
		html += '</thead>'
		
		html += '<tbody>'
		starttime_index = {}
		last_rowspan = {}
		lst = []							
		count = 0
		sno = 0
		# print(dictList)
		for r in dictList:
			count = count + 1
			html += '<tr>'
			if count == 1:
				html += '<td class="h5 secondcolumn timecell"  rowspan="12" style="text-align: center;"> '+ r.get('Starttime') +'  </td>'
			elif count == 12:
				endtime = r.get('Endtime')
				count = 0
			i_index = 0
			
			for i in hall:
				# print(i)
				key = i +'-'+ r.get('Starttime')
				i_index += 1
				col_count[i] += 1
				try:
					data =  final_data[key]
				except KeyError as error:
					data = None	
				if data:
					col_count[i] = 1
					if data.get("session_title") != None:
						last_rowspan[i]		= Helper.rowspan_calc(data.get("session_start_date_time").time().strftime('%H:%M'),data.get("session_end_date_time").time().strftime('%H:%M'))
						starttime 			= r.get('Starttime')						
						st	=	data.get("session_start_date_time").time().strftime('%H:%M')
						et 	=	data.get("session_end_date_time").time().strftime('%H:%M')
						starttime_index[i]	= Helper.find_index(allhalldata, i, starttime)
						
						html +=	'<td rowspan="'+ str(last_rowspan[i]) +'" >'
						if data.get("session_subtitle") != None:
							html +=	'<div class="box" style="vertical-align: middle; background-color:'+ (data.get('bg_color') if data.get('bg_color') else '#000000') +';" > <a style="color:black" href="'+ url_for('sessions.hall_screen',session_id=data.get("session_id")) +'">' + '<spam class="h5">'+data.get("session_title")+'</spam>' +'<br>'+  data.get("session_subtitle") + '<br>' +  '('+ st + '-' + et+')'
						else:
							html +=	'<div class="box" style="vertical-align: middle; background-color:'+ (data.get('bg_color') if data.get('bg_color') else '#000000') +';" > <a style="color:black"  href="'+ url_for('sessions.hall_screen',session_id=data.get("session_id")) +'">' + '<spam class="h5">'+data.get("session_title") + '<br>' +  '('+ st + '-' + et+')'
						html +=	'</a></div>'
						html +=	'</td>'
				else:
					sno = sno + 1
					try:
						last_rowspan[i]
						starttime_index[i]
					except KeyError as error:
						last_rowspan[i] 	= 0
						starttime_index[i] 	= -1
					if col_count[i] > last_rowspan[i]:
						col_count[i] 		= 1
						newstarttime	= Helper.find_nextstarttime(allhalldata, i, starttime_index[i], dayend)
						last_rowspan[i] = Helper.rowspan_calc(r.get('Starttime'),newstarttime)
						html +=	'<td rowspan="'+str(last_rowspan[i]) +'">' #
						html += '</td>'
			html += '</tr>'
		html += '</tbody>'
		html += '</table>'

		return html



	def activesessions_html(dictList,final_data,allhalldata,dayend,hall):
		html = ""
		html += '<table class="table table bordered" data-striped="true" style="width:auto;">'
		html += '<thead>'
		html += '<div class="col-md-12">'
		# html += '<th>'
		# html += '</th>'
		html += '<th></th>'
		column = []
		col_count = {}
		for col in hall:
			col_count[col] =0
			html += '<th colspan="1">'+col+'</th>'
			# column.append(col)
		html += '</div>'
		html += '</thead>'
		
		html += '<tbody>'
		starttime_index = {}
		last_rowspan = {}
		lst = []							
		count = 0
		sno = 0
		print(dictList)
		for r in dictList:
			count = count + 1
			html += '<tr>'
			# html += '<td class="firstcolumn" style="background-color: #000040; color: white;">'
			# html += r.get('Starttime')
			# html += '</td>'
			if count == 1:
				html += '<td class="secondcolumn timecell"  rowspan="12"> '+ r.get('Starttime') +'  </td>'
			elif count == 12:
				endtime = r.get('Endtime')
				count = 0
			i_index = 0
			
			for i in hall:
				print(i)
				key = i +'-'+ r.get('Starttime')
				i_index += 1
				col_count[i] += 1
				# last_rowspan[i] =0
				# starttime_index[i] =0
				try:
					data =  final_data[key]
				except KeyError as error:
					data = None	
				if data:
					col_count[i] = 1
					if data.get("session_title") != None:
						last_rowspan[i]		= Helper.rowspan_calc(data.get("session_start_date_time").time().strftime('%H:%M'),data.get("session_end_date_time").time().strftime('%H:%M'))
						starttime 			= r.get('Starttime')
						starttime_index[i]	= Helper.find_index(allhalldata, i, starttime)
						html +=	'<td style="vertical-align: middle; background-color:'+ (data.get('bg_color')+'95' if data.get('bg_color') else '#00000095') +';" rowspan="'+ str(last_rowspan[i]) +'" >'  
						# html +=	data.get("session_title")
						html +=	'<a style="color:black" target="_blank" href="'+ url_for('sessions.hall_screen',session_id=data.get("session_id")) +'">' + data.get("session_title")
						html +=	'</a>'						
						html +=	'</td>'
				else:
					sno = sno + 1
					try:
						last_rowspan[i]
						starttime_index[i]
					except KeyError as error:
						last_rowspan[i] 	= 0
						starttime_index[i] 	= -1
					if col_count[i] > last_rowspan[i]:
						col_count[i] 		= 1
						# last_rowspan.setdefault(i, []).append(Helper.rowspan_calc(data.get("session_start_date_time").time().strftime('%H:%M'),data.get("session_end_date_time").time().strftime('%H:%M')))
						newstarttime	= Helper.find_nextstarttime(allhalldata, i, starttime_index[i], dayend)
						last_rowspan[i] = Helper.rowspan_calc(r.get('Starttime'),newstarttime)
						html +=	'<td rowspan="'+str(last_rowspan[i]) +'">' 						
						html += '</td>'
			html += '</tr>'
		html += '</tbody>'
		html += '</table>'

		return html


	# def activesessions_html(dictList,final_data,allhalldata,dayend,hall):
	# 	html = ""
	# 	html += '<table class="table table bordered" data-striped="true" style="width:auto;">'
	# 	html += '<thead>'
	# 	html += '<div class="col-md-12">'
	# 	# html += '<th>'
	# 	# html += '</th>'
	# 	html += '<th></th>'
	# 	column = []
	# 	col_count = {}
	# 	for col in hall:
	# 		col_count[col] =0
	# 		html += '<th colspan="1">'+col+'</th>'
	# 		# column.append(col)
	# 	html += '</div>'
	# 	html += '</thead>'
		
	# 	html += '<tbody>'
	# 	starttime_index = {}
	# 	last_rowspan = {}
	# 	lst = []							
	# 	count = 0
	# 	sno = 0
	# 	print(dictList)
	# 	for r in dictList:
	# 		count = count + 1
	# 		html += '<tr>'
	# 		# html += '<td class="firstcolumn" style="background-color: #000040; color: white;">'
	# 		# html += r.get('Starttime')
	# 		# html += '</td>'
	# 		if count == 1:
	# 			html += '<td class="secondcolumn timecell"  rowspan="12"> '+ r.get('Starttime') +'  </td>'
	# 		elif count == 12:
	# 			endtime = r.get('Endtime')
	# 			count = 0
	# 		i_index = 0
			
	# 		for i in hall:
	# 			print(i)
	# 			key = i +'-'+ r.get('Starttime')
	# 			i_index += 1
	# 			col_count[i] += 1
	# 			# last_rowspan[i] =0
	# 			# starttime_index[i] =0
	# 			try:
	# 				data =  final_data[key]
	# 			except KeyError as error:
	# 				data = None	
	# 			if data:
	# 				col_count[i] = 1
	# 				if data.get("session_title") != None:
	# 					last_rowspan[i]		= Helper.rowspan_calc(data.get("session_start_date_time").time().strftime('%H:%M'),data.get("session_end_date_time").time().strftime('%H:%M'))
	# 					starttime 			= r.get('Starttime')
	# 					starttime_index[i]	= Helper.find_index(allhalldata, i, starttime)
	# 					html +=	'<td style="vertical-align: middle; background-color:'+ (data.get('bg_color') if data.get('bg_color') else '#fff') +';" rowspan="'+ str(last_rowspan[i]) +'" >'  
	# 					# html +=	data.get("session_title")
	# 					html +=	'<a style="color:black" target="_blank" href="'+ url_for('sessions.hall_screen',session_id=data.get("session_id")) +'">' + data.get("session_title")
	# 					html +=	'</a>'
	# 					# html +=	'<br>'
	# 					# html +=	str(data.get("session_start_date_time")) + "-" + str(data.get("session_end_date_time"))
	# 					# html +=	'<br>'
	# 					# html +=	i
	# 					# html +=	'<br>'
	# 					# html += 'i_index : '+ str(i_index)
	# 					# html +=	'<br>'
	# 					# html += 'rowspan :' + str(last_rowspan[i])
	# 					# html +=	'<br> count :' + str(col_count[i])
	# 					# html +=	'<br> '
	# 					# html += 'starttime_index :' + str(starttime_index)
	# 					html +=	'</td>'
	# 			else:
	# 				sno = sno + 1
	# 				try:
	# 					last_rowspan[i]
	# 					starttime_index[i]
	# 				except KeyError as error:
	# 					last_rowspan[i] 	= 0
	# 					starttime_index[i] 	= -1
	# 				if col_count[i] > last_rowspan[i]:
	# 					col_count[i] 		= 1
	# 					# last_rowspan.setdefault(i, []).append(Helper.rowspan_calc(data.get("session_start_date_time").time().strftime('%H:%M'),data.get("session_end_date_time").time().strftime('%H:%M')))
	# 					newstarttime	= Helper.find_nextstarttime(allhalldata, i, starttime_index[i], dayend)
	# 					last_rowspan[i] = Helper.rowspan_calc(r.get('Starttime'),newstarttime)
	# 					html +=	'<td rowspan="'+str(last_rowspan[i]) +'">' #
	# 					# html += r.get('Starttime')
	# 					# html +=	'<br>'
	# 					# html +=	i
	# 					# html +=	'<br>'
	# 					# html += 'S index' + str(starttime_index[i])
	# 					# html +=	'<br>'
	# 					# html += 'count :' +	str(col_count[i])
	# 					# html +=	'<br>'
	# 					# html +=	'last rowspan :' +str(last_rowspan[i])
	# 					# html +=	'<br>'
	# 					# html +=	'New Start time :' + newstarttime
	# 					html += '</td>'
	# 		html += '</tr>'
	# 	html += '</tbody>'
	# 	html += '</table>'

	# 	return html
# --------------------PROGRAM SHEET FUNCTIONS END------------------------------


app.jinja_env.globals.update(Helper=Helper)	



