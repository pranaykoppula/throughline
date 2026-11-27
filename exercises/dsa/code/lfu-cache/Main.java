import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        LFUCache cache = new LFUCache(Integer.parseInt(in.readLine().trim()));
        StringBuilder out = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");
            if (parts[0].isEmpty()) continue;
            if (parts[0].equals("get")) {
                out.append(cache.get(Integer.parseInt(parts[1]))).append('\n');
            } else {
                cache.put(Integer.parseInt(parts[1]), Integer.parseInt(parts[2]));
            }
        }
        System.out.print(out);
    }
}
