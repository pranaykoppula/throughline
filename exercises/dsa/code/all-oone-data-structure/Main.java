import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        AllOne counts = new AllOne();
        StringBuilder out = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");
            if (parts[0].isEmpty()) continue;
            switch (parts[0]) {
                case "inc" -> counts.inc(parts[1]);
                case "dec" -> counts.dec(parts[1]);
                case "max" -> out.append('"').append(counts.getMaxKey()).append("\"\n");
                default -> out.append('"').append(counts.getMinKey()).append("\"\n");
            }
        }
        System.out.print(out);
    }
}
