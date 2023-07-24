
class Solution(object):
    def __init__(self, nums, T):
        self.nums = nums
        self.T = T

    def find_pair(self):
        """
        Given an array of integers, and a target T, 
        return the first instance of a tuple (n1, n2), such that n1 + n2 = T
        If not found, return -1
        O[n]
        """

        for i in range(len(self.nums)):
            for j in range(len(self.nums)):
                if i != j and self.nums[i] + self.nums[j] == self.T:
                    return (self.nums[i], self.nums[j])
        return -1


if __name__ == '__main__':
    nums1 = [1, 1, 4]
    T1 = 2
    s1 = Solution(nums1, T1)
    print(s1.find_pair())

    nums2 = [1, 2, 3]
    T2 = 6
    s2 = Solution(nums2, T2)
    print(s2.find_pair())




