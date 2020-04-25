package com.example.choosefromgallery;

import org.junit.Test;

import java.io.InputStream;
import java.net.URL;

import static org.junit.Assert.assertEquals;

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() {
        assertEquals(4, 2 + 2);
    }

    @Test
    public void sendImage() throws Exception {
        InputStream is = this.getClass().getResourceAsStream("human.jpeg");
        MainActivity.RequestTask requestTask = new MainActivity.RequestTask(is);
        requestTask.executeRequest(new URL(MainActivity.PREDICTION_URL), "human.jpeg");
    }
}
