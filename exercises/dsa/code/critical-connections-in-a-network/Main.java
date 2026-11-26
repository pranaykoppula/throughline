import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder all = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) all.append(line).append(' ');
        StringTokenizer st = new StringTokenizer(all.toString());
        int n = Integer.parseInt(st.nextToken()), m = Integer.parseInt(st.nextToken());
        List<List<Integer>> edges = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            edges.add(List.of(Integer.parseInt(st.nextToken()), Integer.parseInt(st.nextToken())));
        }
        List<int[]> out = new ArrayList<>();
        for (List<Integer> e : new Solution().criticalConnections(n, edges)) {
            out.add(new int[] {Math.min(e.get(0), e.get(1)), Math.max(e.get(0), e.get(1))});
        }
        out.sort((p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]));
        StringBuilder sb = new StringBuilder();
        for (int[] e : out) sb.append(e[0]).append(' ').append(e[1]).append('\n');
        System.out.print(sb);
    }
}
