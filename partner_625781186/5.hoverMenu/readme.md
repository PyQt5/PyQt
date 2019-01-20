## 更新 2018年9月9日
- 在程序中定义 离开当前页面可以选择是删除数据还是保留 ;
- 收缩动画 ;

# 进入式下拉菜单

![效果图](ScreenShot/2.gif)

## [程序文档 , emmm可能没什么用](Documentation/README-5.hoverMenu.md)

### 添加额外菜单

- 1.将W1整个窗体(连通子部件，按住Ctrl+鼠标左键复制);
- 2.修改对象名更改为WX , 并将按钮的提升类设定为BX；
### ↑这两点至关重要↑

![提升类.png](https://upload-images.jianshu.io/upload_images/10769157-aded44441a666282.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 3.在Menu.py中为你的菜单添加图标及事件；
    - BaseElement.py 对菜单栏的框/按钮/下拉菜单 定义;
    - Menu.py 对菜单栏按钮添加功能/对下拉菜单添加条目及功能;

![image.png](https://upload-images.jianshu.io/upload_images/10769157-44f6e8eee864054e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 下一步要做的
没想好；