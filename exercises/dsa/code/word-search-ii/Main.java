import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder all = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) all.append(line).append(' ');
        StringTokenizer st = new StringTokenizer(all.toString());
        int rows = Integer.parseInt(st.nextToken()), cols = Integer.parseInt(st.nextToken());
        char[][] board = new char[rows][];
        for (int r = 0; r < rows; r++) board[r] = st.nextToken().toCharArray();
        int k = Integer.parseInt(st.nextToken());
        String[] words = new String[k];
        for (int i = 0; i < k; i++) words[i] = st.nextToken();
        List<String> out = new ArrayList<>(new Solution().findWords(board, words));
        Collections.sort(out);
        StringBuilder sb = new StringBuilder();
        for (String w : out) sb.append(w).append('\n');
        System.out.print(sb);
    }
}
