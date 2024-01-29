class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        max_area: int = -1
        for i in range(len(height)):
            for j in range(i+1, len(height)):
                area = (j-i) * min(height[i], height[j])
                if area > max_area:
                    max_area = area     
        return max_area
        
        




        
solution = Solution()
print(solution.maxArea([1,8,6,2,5,4,8,3,7]))
print(solution.maxArea([1,1]))