<!-- Tag: 找规律 -->

<summary><b>问题简述</b></summary>

> [剑指 Offer 43. 1～n 整数中 1 出现的次数 - 力扣（LeetCode）](https://leetcode-cn.com/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/)

```txt
输入一个整数 n ，求1～n这n个整数的十进制表示中1出现的次数。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个整数 n ，求1～n这n个整数的十进制表示中1出现的次数。

例如，输入12，1～12这些整数中包含1 的数字有1、10、11和12，1一共出现了5次。

示例 1：
    输入：n = 12
    输出：5
示例 2：
    输入：n = 13
    输出：6

限制：
    1 <= n < 2^31

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路</b></summary>

- 找规律的题目，很费时，建议直接看：[1～n 整数中 1 出现的次数（清晰图解） - Krahets](https://leetcode-cn.com/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/solution/mian-shi-ti-43-1n-zheng-shu-zhong-1-chu-xian-de-2/)

<details><summary><b>Python</b></summary>

```python
class Solution:
    def countDigitOne(self, n: int) -> int:
        # 初始化一些变量
        digit, ret = 1, 0
        hi, cur, lo = n // 10, n % 10, 0

        while hi != 0 or cur != 0:
            if cur == 0:
                ret += hi * digit
            elif cur == 1:
                ret += hi * digit + lo + 1
            else:
                ret += (hi + 1) * digit
            lo += cur * digit
            cur = hi % 10
            hi //= 10
            digit *= 10
        return ret
```

</details>

