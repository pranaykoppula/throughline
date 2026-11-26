class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        // Use the list itself as the table: number v belongs at position v - 1.
        for (int i = 0; i < n; i++) {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                swap(nums[i], nums[nums[i] - 1]);
            }
        }
        // The first slot not holding its own number marks the gap.
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
};
