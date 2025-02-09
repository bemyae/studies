<!-- Tag: 二分 -->

<summary><b>问题简述</b></summary>

```txt
统计给定数字在排序数组中出现的次数。
```

<details><summary><b>详细描述</b></summary>

```txt
统计一个数字在排序数组中出现的次数。

示例 1:
    输入: nums = [5,7,7,8,8,10], target = 8
    输出: 2
示例 2:
    输入: nums = [5,7,7,8,8,10], target = 6
    输出: 0

提示：
    0 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
    nums 是一个非递减数组
    -10^9 <= target <= 10^9

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zai-pai-xu-shu-zu-zhong-cha-zhao-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 二分法分别查找目标值的左右边界；
- 小技巧：如果二分查找的是右边界，那么可以通过查找 `target - 1` 来获得左边界，因为二分查找实际上找的是目标值的插入位置；

<details><summary><b>Python：使用库函数</b></summary>

```python
import bisect

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        idx_r, idx_l = bisect.bisect_right(nums, target), bisect.bisect_left(nums, target)
        # idx_r, idx_l = bisect.bisect_right(nums, target), bisect.bisect_right(nums, target - 1)
        return idx_r - idx_l
```

</details>

<details><summary><b>Python：不使用库函数</b></summary>

```python
class Solution:
    def search(self, nums: [int], target: int) -> int:
        
        def bisect(tar):
            l, r = 0, len(nums) - 1
            while l <= r:
                m = (l + r) // 2
                if nums[m] <= tar: 
                    l = m + 1
                else: 
                    r = m - 1
            return l
        
        return bisect(target) - bisect(target - 1)
```

</details>

