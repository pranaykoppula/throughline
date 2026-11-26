import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        MedianFinder finder = new MedianFinder();
        StringBuilder out = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");
            if (parts[0].isEmpty()) continue;
            if (parts[0].equals("add")) {
                finder.addNum(Integer.parseInt(parts[1]));
            } else {
                out.append(String.format(Locale.ROOT, "%.5f", finder.findMedian())).append('\n');
            }
        }
        System.out.print(out);
    }
}
