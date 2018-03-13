#coding:utf-8

import xml.etree.ElementTree as ET
import time


class NewsItem(object):
    def __init__(self, title,desc,pic_url,url):
        self.title = title
        self.desc = desc
        self.pic_url = pic_url
        self.url = url
    def __str__(self):
        template = '''<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>'''
        return template % (self.title,self.desc,self.pic_url,self.url)



class WeiXinMsg(object):
    def __init__(self, xml_body=None):
        self.xml_body = xml_body#unicode(xml_body).encode("utf-8")
        root = ET.fromstring(self.xml_body)

        self.j={}
        for child in root:
            if child.tag == 'CreateTime':
                value = int(child.text)
            else:
                value = child.text
            self.j[child.tag] = value
        self.ToUserName = self.j['FromUserName']
        self.FromUserName = self.j['ToUserName']
        self.MsgType = self.j['MsgType']
        
        self.MsgId = self.j['MsgId'] if 'MsgId' in self.j else ''
        self.Content = self.j['Content'] if 'Content' in self.j else ''
        self.PicUrl = self.j['PicUrl'] if 'PicUrl' in self.j else ''
        self.MediaId = self.j['MediaId'] if 'MediaId' in self.j else ''
        self.Recognition = self.j['Recognition'] if 'Recognition' in self.j else ''
        self.Format = self.j['Format'] if 'Format' in self.j else ''
        self.ThumbMediaId = self.j['ThumbMediaId'] if 'ThumbMediaId' in self.j else ''
        self.Location_X = self.j['Location_X'] if 'Location_X' in self.j else ''
        self.Location_Y = self.j['Location_Y'] if 'Location_Y' in self.j else ''
        self.Scale = self.j['Scale'] if 'Scale' in self.j else ''
        self.Label = self.j['Label'] if 'Label' in self.j else ''
        self.Title = self.j['Title'] if 'Title' in self.j else ''
        self.Description = self.j['Description'] if 'Description' in self.j else ''
        self.Url = self.j['Url'] if 'Url' in self.j else ''
        self.EventKey = self.j['EventKey'] if 'EventKey' in self.j else ''
        self.Event = self.j['Event'].lower() if 'Event' in self.j else ''
        self.Ticket = self.j['Ticket'].lower() if 'Ticket' in self.j else ''
        # # ToUserName  开发者微信号
        # # FromUserName    发送方帐号（一个OpenID）
        # # CreateTime  消息创建时间 （整型）
        # # MsgType 消息类型
        # # Content 文本消息内容
        # # MsgId   消息id，64位整型      
        # # PicUrl  图片链接
        # # MediaId 图片消息媒体id，可以调用多媒体文件下载接口拉取数据。
        # # MediaId 语音消息媒体id，可以调用多媒体文件下载接口拉取数据。
        # # Format  语音格式，如amr，speex等
        # # MediaId 视频消息媒体id，可以调用多媒体文件下载接口拉取数据。
        # # ThumbMediaId    视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
        # # MediaId 视频消息媒体id，可以调用多媒体文件下载接口拉取数据。
        # # ThumbMediaId    视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
        # # Location_X  地理位置维度
        # # Location_Y  地理位置经度
        # # Scale   地图缩放大小
        # # Label   地理位置信息
        # # Title   消息标题
        # # Description 消息描述
        # # Url 消息链接


    def __getitem__(self,name):
        return self.j[name] if name in self.j else ''

            
    def resp_text(self,text,funcFlag=0):
        template = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>%s</FuncFlag>
</xml>'''
        return template % (self.ToUserName,self.FromUserName,int(time.time()),text,funcFlag)

        
    def resp_news(self,news_items,funcFlag=0):
        template='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%s</ArticleCount>
<Articles>
  %s
</Articles>
<FuncFlag>%s</FuncFlag>
</xml>'''
        return template % (self.ToUserName,self.FromUserName,int(time.time()),len(news_items),\
        (''.join([str(i) for i in news_items])),funcFlag)


        
    def resp_music(self, title, desc, music_url, hq_music_url, funcFlag=0):
        '''回复音乐'''
        template='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
  <Title><![CDATA[%s]]></Title>
  <Description><![CDATA[%s]]></Description>
  <MusicUrl><![CDATA[%s]]></MusicUrl>
  <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
</Music>
<FuncFlag>%s</FuncFlag>
</xml>'''
        return template % (self.ToUserName, self.FromUserName, int(time.time()), \
                           title, desc, music_url, hq_music_url, funcFlag)
            
        
        
