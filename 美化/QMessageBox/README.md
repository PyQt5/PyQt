# 消息提示框的按钮和图标美化

### [1.方案一](方案一/)
 - 1.1 该方案使用dialogbuttonbox-buttons-have-icons: 1; 开启自带的图标样式
 - 1.2 再利用dialog-xx-icon: url(); 来设置自定义的图标, 具体参考[list-of-icons](http://doc.qt.io/qt-5/stylesheet-reference.html#list-of-icons)
 - 1.3 缺点 部分按钮图标无效，无法自定义不同按钮的颜色
 
### [2.方案二](方案二/)
 - 2.1 采用样式表中的属性选择器 QPushButton[text="xxx"] 可以根据按钮中的文字来区分
 - 2.2 在利用属性样式qproperty-icon: url();来设置自定义图标
 - 2.3 解决方案一的缺点