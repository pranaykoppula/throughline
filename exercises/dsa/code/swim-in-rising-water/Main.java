import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder all = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) all.append(line).append(' ');
        StringTokenizer st = new StringTokenizer(all.toString());
        int n = Integer.parseInt(st.nextToken());
        int[][] grid = new int[n][n];
        for (int[] row : grid)
            for (int c = 0; c < n; c++) row[c] = Integer.parseInt(st.nextToken());
        System.out.println(new Solution().swimInWater(grid));
    }
}
