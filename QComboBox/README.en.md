# QComboBox

- Catalog
  - [Data Linkage](#1data-linkage)

## 1、Data Linkage
[Run CityLinkage.py](CityLinkage.py)

Three level linkage, data file is data.json

1. use `QComboBox`,`setModel` and `QSortFilterProxyModel` to filter
2. the filter role is `Qt::ToolTipRole`
3. can use `QColumnView` maybe like this example

![CityLinkage](ScreenShot/CityLinkage.gif)