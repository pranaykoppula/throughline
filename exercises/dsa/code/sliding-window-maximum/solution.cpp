class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        // Indices of readings that could still be a window's maximum,
        // with their values in decreasing order from front to back.
        deque<int> candidates;
        vector<int> result;
        for (int i = 0; i < (int)nums.size(); i++) {
            // A new reading outlives every smaller one before it.
            while (!candidates.empty() && nums[candidates.back()] <= nums[i]) {
                candidates.pop_back();
            }
            candidates.push_back(i);
            // The front has slid out of the window.
            if (candidates.front() <= i - k) {
                candidates.pop_front();
            }
            if (i >= k - 1) {
                result.push_back(nums[candidates.front()]);
            }
        }
        return result;
    }
};
