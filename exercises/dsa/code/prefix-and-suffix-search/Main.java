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
        String[] words = new String[n];
        for (int i = 0; i < n; i++) words[i] = st.nextToken();
        WordFilter search = new WordFilter(words);
        int q = Integer.parseInt(st.nextToken());
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < q; i++) {
            String pref = st.nextToken(), suff = st.nextToken();
            out.append(search.f(pref, suff)).append('\n');
        }
        System.out.print(out);
    }
}
