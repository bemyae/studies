<!-- Tag: 二叉树、深度优先搜索、前缀和 -->

<summary><b>问题描述</b></summary>

```txt
给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。

路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

示例 1：（见图示）
    输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
    输出：3
    解释：和等于 8 的路径有 3 条，如图所示。
示例 2：
    输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
    输出：3

提示:
    二叉树的节点个数的范围是 [0,1000]
    -10^9 <= Node.val <= 10^9 
    -1000 <= targetSum <= 1000 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/path-sum-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

<div align="center"><img src="../../../_assets/pathsum3-1-tree.jpeg" height="300" /></div>


<summary><b>思路</b></summary>

<details><summary><b>法1）Python：双重递归</b></summary>

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:  # noqa
        """"""
        if root is None:
            return 0

        # 双重递归
        ret = self.dfs_root(root, targetSum)
        # 把左右节点当做根节点都遍历一遍
        ret += self.pathSum(root.left, targetSum)
        ret += self.pathSum(root.right, targetSum)

        return ret

    def dfs_root(self, root, targetSum):  # noqa
        """ 计算从根节点开始的路径数 """
        if root is None:
            return 0

        ans = 0
        if root.val == targetSum:  # 因为节点的值可能为 0，所以这里还不能直接返回
            ans += 1

        # 差值
        delta_sum = targetSum - root.val

        # 继续遍历左右子树
        ans += self.dfs_root(root.left, delta_sum)
        ans += self.dfs_root(root.right, delta_sum)
        return ans
```
</details>

<details><summary><b>法2）Python：前缀和+DFS</b></summary>

```python
from collections import defaultdict


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # 保存前缀和
    prefix = defaultdict(int)
    targetSum: int

    def pathSum(self, root: TreeNode, targetSum: int) -> int:  # noqa
        """ 解法2：前缀和 + DFS """
        self.prefix[0] = 1
        self.targetSum = targetSum
        return self.dfs(root, 0)

    def dfs(self, root, cur):
        if root is None:
            return 0

        ret = 0
        cur += root.val
        ret += self.prefix[cur - self.targetSum]

        self.prefix[cur] += 1
        ret += self.dfs(root.left, cur)
        ret += self.dfs(root.right, cur)
        self.prefix[cur] -= 1

        return ret
```

</details>
