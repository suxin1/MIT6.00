## 问题优化
### 问题优化普遍包含两个重要部分：
* 一个目标， 找到最大或最小
* 一个约束的集合

### 问题简化
将复杂问题简化， 将新的问题映射到已经解决的经典问题

### 贪婪算法（Greedy Algorithm）

拿经典的背包问题为例， 当小偷闯进一栋豪宅准备steal someting，而他只能携带有限的重量和体积，他面临的最大问题是怎样选择，能获得最大收获。
最简单的就是先拿最值钱的。稍微聪明一点的会选择体积小，重量轻， 而且值钱的物品， 从mathematical角度来说，
the one which Value／weight is greatest。

    1). 将所有物品按照一定的方式排序。（value first, value/weight ratio first)
    2). 按先后顺序拿取物品，直到遇到条件限制。
    
贪婪算法的复杂度：
排序( len(items) * log(len(items)) ) + 选择( len(items) )

### 绝对优化
    
