import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String s = in.readLine(), p = in.readLine();
        if (s == null) s = "";
        if (p == null) p = "";
        System.out.println(new Solution().numDistinct(s, p));
    }
}
