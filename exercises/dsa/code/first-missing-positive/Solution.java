class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        // Use the array itself as the table: number v belongs at position v - 1.
        for (int i = 0; i < n; i++) {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int home = nums[i] - 1;
                int moved = nums[home];
                nums[home] = nums[i];
                nums[i] = moved;
            }
        }
        // The first slot not holding its own number marks the gap.
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
}
