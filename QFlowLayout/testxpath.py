#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023/02/21
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: testxpath.py
@description:
"""

import os

from lxml.etree import HTML  # @UnresolvedImport

# 作者
Actor = '''<a href="{href}" target="_blank" title="{title}" style="text-decoration: none;font-size: 12px;color: #999999;">{title}</a>&nbsp;'''


def _makeItem(lis):
    for li in lis:
        a = li.find('.//div/a')
        play_url = "https://music.163.com" + a.get("href")  # 视频播放地址
        img = li.find(".//div/img")
        cover_url = img.get("src")  # 封面图片
        playlist_title = a.get("title")  # 歌单名
        # figure_info = a.find("div/span")
        figure_info = "aaa"  #if figure_info is None else figure_info.text  # 影片信息
        figure_score = ""  # 评分
        # 歌手
        figure = li.xpath(".//p[2]/a")[0]
        playlist_author = "<span style=\"font-size: 12px;\"作者：{}</span>".format(
            Actor.format(href="https://music.163.com" +figure.get("href"),title=figure.get("title")))
        # 播放数
        play_count = (li.xpath(".//div/div/span[2]/text()") or [""])[0]
        path = "cache/{0}.jpg".format(
            os.path.splitext(os.path.basename(cover_url).split('?')[0])[0])
        cover_path = "Data/pic_v.png"
        if os.path.isfile(path):
            cover_path = path

        print(cover_path, playlist_title,  playlist_author,
              play_count, play_url, cover_url, path)
        # iwidget = ItemWidget(cover_path, playlist_title,
        #                       playlist_author, play_count, play_url,
        #                      cover_url, path, self)
        # self._layout.addWidget(iwidget)


def _parseHtml(html):
    html = HTML(html)
    # 查找所有的li
    lis = html.xpath("//ul[@id='m-pl-container']/li")
    # if not lis:
    #     self.Page = -1  # 后面没有页面了
    #     return
    # self.Page += 1
    _makeItem(lis)


if __name__ == '__main__':
    data = open(r'D:\Computer\Desktop\163.html', 'rb').read()
    _parseHtml(data)