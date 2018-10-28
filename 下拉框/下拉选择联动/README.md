# QComboBox下拉数据关联

这里简单的做了一个省市区关联的三级联动，数据源在data.json中

主要用了QComboBox的setModel设置一个QSortFilterProxyModel过滤模型

并根据唯一编码过滤，为了不影响内容显示，唯一编码的角色为ToolTipRole

匆忙中写出来，可能有些不完善，或者该方式效率不是很高

# 截图
![截图1](ScreenShot/1.gif)