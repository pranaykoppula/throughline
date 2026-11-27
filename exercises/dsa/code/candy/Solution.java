import java.util.Arrays;

class Solution {
    public int candy(int[] ratings) {
        int n = ratings.length;
        int[] give = new int[n];
        Arrays.fill(give, 1);  // everyone gets at least one
        // Left to right: anyone rated above their left neighbour gets one more than them.
        for (int i = 1; i < n; i++)
            if (ratings[i] > ratings[i - 1]) give[i] = give[i - 1] + 1;
        // Right to left: the same for right neighbours, without undoing the first pass.
        for (int i = n - 2; i >= 0; i--)
            if (ratings[i] > ratings[i + 1]) give[i] = Math.max(give[i], give[i + 1] + 1);
        int total = 0;
        for (int g : give) total += g;
        return total;
    }
}
