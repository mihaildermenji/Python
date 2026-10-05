class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* back = nullptr;
        ListNode* node = head;
        while (node != nullptr) {
            ListNode* ahead = node->next;
            node->next = back;
            back = node;
            node = ahead;
        }
        return back;
    }
};
