package others;

import java.util.Arrays;
import java.util.List;

public class Test2 {
    public static void main(String[] args) {

        List<String> javaVersions = Arrays.asList("Java 6", "Java 7", "Java 8");
        boolean flag = javaVersions.stream().allMatch(str -> {
            System.out.println("Testing: " + str);
            return str.contains("8");
        });
        System.out.println(flag);
    }
}



