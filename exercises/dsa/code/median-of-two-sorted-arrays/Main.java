import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Locale;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder all = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) all.append(line).append(' ');
        StringTokenizer st = new StringTokenizer(all.toString());
        int m = Integer.parseInt(st.nextToken());
        int[] a = new int[m];
        for (int i = 0; i < m; i++) a[i] = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());
        int[] b = new int[n];
        for (int i = 0; i < n; i++) b[i] = Integer.parseInt(st.nextToken());
        System.out.println(String.format(Locale.ROOT, "%.5f", new Solution().findMedianSortedArrays(a, b)));
    }
}
