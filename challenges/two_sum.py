class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        With time complexity less than O(n^2)
        """
        dict = {}
        for i in range(len(nums)):
            if target - nums[i] in dict:
                return [dict[target - nums[i]], i]            
            dict[nums[i]] = i        
        return []


solution = Solution()
print(solution.twoSum([2, 7, 11, 15], 9))