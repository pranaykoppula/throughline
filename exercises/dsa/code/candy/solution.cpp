class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> give(n, 1);  // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for (int i = 1; i < n; i++)
            if (ratings[i] > ratings[i - 1]) give[i] = give[i - 1] + 1;
        // Right to left: the same for right neighbours, without undoing the first pass.
        for (int i = n - 2; i >= 0; i--)
            if (ratings[i] > ratings[i + 1]) give[i] = max(give[i], give[i + 1] + 1);
        return accumulate(give.begin(), give.end(), 0);
    }
};
