<!-- Tag: 优先队列、快排、经典 -->

<summary><b>问题简述</b></summary>

```txt
输入整数数组 arr ，找出其中最小的 k 个数
```

<details><summary><b>详细描述</b></summary>

```txt
输入整数数组 arr ，找出其中最小的 k 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。

示例 1：
    输入：arr = [3,2,1], k = 2
    输出：[1,2] 或者 [2,1]
示例 2：
    输入：arr = [0,1,2,1], k = 1
    输出：[0]
 
限制：
    0 <= k <= arr.length <= 10000
    0 <= arr[i] <= 10000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：快排中的 partition 过程</b></summary>

- 快排的过程：
    - **partition 过程**：以数组某个元素（一般取首元素）为基准数，将所有小于基准数的元素移动至其左边，大于基准数的元素移动至其右边。
    - 递归地对左右部分执行 **partition 过程**，直至区域内的元素数量为 1；
- 基于以上思想，当某次划分后基准数正好是第 k+1 小的数字，那么此时基准数左边的所有数字便是题目要求的最小的 k 个数。

<details><summary><b>Python</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:

        def partition(lo, hi):  # [lo, hi]
            if lo == hi: return

            p = arr[lo]  # 选取第一个位置为基准点
            l, r = lo, hi  # 注意点1）l 的初始位置在 lo，而不是 lo + 1
            # l, r = lo + 1, hi  # 这样写是错误的，因为不能保证 arr[lo + 1] <= arr[lo] 成立；如果 arr[lo + 1] > arr[lo]，那么最后一步交换就会出错
            while l < r:
                # 注意点2）如果选取 arr[lo] 为基准点，则需要先移动 r，
                # 这样才能保证结束循环时，l 和 r 指向一个小于等于 arr[lo] 的值
                # 反之，如果选择 arr[hi] 为基准点，则需要先移动 l
                while l < r and arr[r] >= p: r -= 1
                while l < r and arr[l] <= p: l += 1
                arr[l], arr[r] = arr[r], arr[l]
                
            arr[lo], arr[l] = arr[l], arr[lo]  # 将基准点移动到分界点

            if l < k: partition(l + 1, hi)
            if l > k: partition(lo, l - 1)

        partition(0, len(arr) - 1)
        return arr[:k]
```

</details>


<summary><b>思路2：堆（优先队列）</b></summary>

- **写法1）** 维护一个长度为 k 的大顶堆（第一个数最大），当下一个元素小于堆顶值，就更新堆（弹出堆顶，插入新值）；
- **写法2）** 直接对整个数组构建一个小顶堆，然后循环弹出前 k 个值；
- 注意写法1 的时间复杂度是 `O(NlogK)`，而写法2 是 `O(NlogN)`；

<details><summary><b>Python：写法1（使用库函数）</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k < 1 or not arr:  # 使用堆，要添加非空断言
            return []

        import heapq

        # python 默认是小顶堆，且不支持自定义比较函数，所以要添加负号转成取前 k 大的数
        ret = [-x for x in arr[:k]]
        heapq.heapify(ret)

        for i in range(k, len(arr)):
            if -arr[i] > ret[0]:
                heapq.heappop(ret)
                heapq.heappush(ret, -arr[i])

        return [-x for x in ret]
```

</details>

<details><summary><b>Python：写法2（使用库函数）</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k < 1 or not arr:  # 使用堆，要添加非空断言
            return []

        import heapq

        # python 默认是小顶堆
        heapq.heapify(arr)

        ret = []
        for _ in range(k):
            ret.append(heapq.heappop(arr))

        return ret
```

</details>


<summary><b>思路3：计数排序</b></summary>

- 因为题目限制了 `arr[i]` 的范围，所以还可以使用计数排序，时间复杂度 `O(N)`；

<details><summary><b>Python：写法1（不使用库函数）</b></summary>

```python
class Solution:
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k >= len(arr):  # 使用计数排序要加长度判断
            return arr

        dp = [0] * 10001

        for x in arr:
            dp[x] += 1
        
        ret = []
        cnt = 0
        for i in range(len(dp)):
            while dp[i] and cnt < k:
                ret.append(i)
                cnt += 1
                dp[i] -= 1
            if cnt == k:
                return ret
```

</details>