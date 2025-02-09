<!-- Tag: 动态规划 -->

<summary><b>问题简述</b></summary>

```txt
给定一个数字，我们按照如下规则把它翻译为字符串：0 翻译成 “a” ，1 翻译成 “b”，……，11 翻译成 “l”，……，25 翻译成 “z”。求一个数字有多少种不同的翻译方法。
```

<details><summary><b>详细描述</b></summary>

```txt
给定一个数字，我们按照如下规则把它翻译为字符串：0 翻译成 “a” ，1 翻译成 “b”，……，11 翻译成 “l”，……，25 翻译成 “z”。一个数字可能有多个翻译。请编程实现一个函数，用来计算一个数字有多少种不同的翻译方法。

示例 1:
    输入: 12258
    输出: 5
    解释: 12258有5种不同的翻译，分别是"bccfi", "bwfi", "bczi", "mcfi"和"mzi"

提示：
    0 <= num < 231

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路：动态规划</b></summary>

- 首先要意识到本题是一个有条件的斐波那契数列/跳台阶问题；
    - 假设不是26个字母，而是100个不同的字母，那么是不是 `dp[i] = dp[i-1] + dp[i-2]`？；
- 因此本题另一个考察点就是如何实现这个条件判断；

<details><summary><b>Python</b></summary>

```python
import math


class Solution:
    def translateNum(self, num: int) -> int:

        # num 的位数
        N = int(math.log10(num)) + 1 if num > 0 else 1

        def slide(i):
            """截取 num 中的两位数，效果如下
            Examples:
                >>> slide(54321, 1)
                54
                >>> slide(54321, 2)
                43
                >>> slide(54321, 3)
                32
            """
            return num // 10 ** (N - i - 1) % 100

        dp0 = 1
        dp1 = 2 if slide(1) < 26 else 1

        if N == 1:
            return dp0
        if N == 2:
            return dp1

        for i in range(2, N):
            if 9 < slide(i) < 26:  # “01” 不能翻译成 “a”，所以要大于 9
                dp0, dp1 = dp1, dp0 + dp1
            else:
                dp0, dp1 = dp1, dp1

        return dp1
```

</details>

