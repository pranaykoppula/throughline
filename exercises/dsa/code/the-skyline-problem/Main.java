import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder all = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) all.append(line).append(' ');
        StringTokenizer st = new StringTokenizer(all.toString());
        int n = Integer.parseInt(st.nextToken());
        int[][] buildings = new int[n][3];
        for (int[] b : buildings) {
            for (int j = 0; j < 3; j++) b[j] = Integer.parseInt(st.nextToken());
        }
        StringBuilder out = new StringBuilder();
        for (List<Integer> p : new Solution().getSkyline(buildings)) {
            out.append(p.get(0)).append(' ').append(p.get(1)).append('\n');
        }
        System.out.print(out);
    }
}
