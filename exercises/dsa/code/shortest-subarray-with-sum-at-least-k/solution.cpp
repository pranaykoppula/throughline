class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        int n = nums.size();
        // prefix[j] - prefix[i] is the total of days i .. j-1.
        vector<long long> prefix(n + 1, 0);
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        int best = n + 1;
        // Start points worth keeping, with prefix totals increasing from front to back.
        deque<int> starts;
        for (int j = 0; j <= n; j++) {
            // The oldest start that already reaches k gives its best answer now.
            while (!starts.empty() && prefix[j] - prefix[starts.front()] >= k) {
                best = min(best, j - starts.front());
                starts.pop_front();
            }
            // A start with a total at least as high as this one is never better.
            while (!starts.empty() && prefix[starts.back()] >= prefix[j]) {
                starts.pop_back();
            }
            starts.push_back(j);
        }
        return best <= n ? best : -1;
    }
};
