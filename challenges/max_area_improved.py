class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        max_area = 0
        left, right = 0, len(height) - 1

        while left < right:
            # Calculate the area
            width = right - left
            current_area = width * min(height[left], height[right])
            max_area = max(max_area, current_area)

            # Move the pointer pointing to the shorter line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area
        
        
solution = Solution()
print(solution.maxArea([1,8,6,2,5,4,8,3,7]))
print(solution.maxArea([1,1]))            