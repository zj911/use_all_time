列表生成多个判断生成
对于多种情况获得多种结果，if else结构：
a=['零' if i==0 else '三' if i==3 else '五' if i==5 else i  for i in range(20) ]
将0,3,5换成中文的零，三，五，输出如下所示：


使用：
if source_video == 'rtmp://172.16.132.234:1935/live/rtmp_live_1080' or source_video == 'rtsp://172.16.132.234:1935/live/rtsp_live_1080':
        [mixstream_stuple_list.append((8,index[1],source_video,'1280x720',"3000k")) if index[1].find('720') != -1 and index[1].find('veryfast') != -1 \
        else mixstream_stuple_list.append((8,index[1],source_video,'1920x1080',"3000k")) if index[1].find('720') == -1 and index[1].find('veryfast')!= -1 \
        else mixstream_stuple_list.append((6,index[1],source_video,'1280x720',"3000k"))  if index[1].find('720') != -1 and index[1].find('medium')!= -1 \
        else mixstream_stuple_list.append((3,index[1],source_video,'1920x1080',"3000k")) if index[1].find('720') == -1 and index[1].find('medium')!= -1 else None for index in cc]

得出生成结果