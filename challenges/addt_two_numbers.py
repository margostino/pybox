# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
        You may assume the two numbers do not contain any leading zero, except the number 0 itself.

        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """



solution = Solution()
l1 = ListNode(2, ListNode(4, ListNode(3)))
l2 = ListNode(5, ListNode(6, ListNode(4)))
print(solution.addTwoNumbers(l1, l2))



        