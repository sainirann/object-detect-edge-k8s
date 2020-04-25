package com.example.choosefromgallery;

import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {
    private static final int PICK_IMAGE = 100;
    static final String PREDICTION_URL = "http://192.168.0.15:31507";

    private ImageView imageView;
    private Button button, predict;
    private Uri imageUri;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = findViewById(R.id.imageView);
        button = findViewById(R.id.buttonLoadPicture);
        predict = findViewById(R.id.predict_picture);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openGallery();
            }
        });
    }

    private void openGallery() {
        Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_IMAGE);
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == PICK_IMAGE){
            imageUri = data.getData();
            imageView.setImageURI(imageUri);
            predict.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try {
                        new RequestTask(getContentResolver().openInputStream(imageUri))
                            .execute(PREDICTION_URL, imageUri.getPath()).get();
                        Toast.makeText(getApplicationContext(), "Image Successfully Predicted", Toast.LENGTH_LONG).show();
                    } catch (Exception e) {
                        Log.e(getClass().getCanonicalName(), e.getMessage());
                    }
                }
            });
        }
    }

    static class RequestTask extends AsyncTask<String, Void, String> {
        private final InputStream imageStream;

        RequestTask(InputStream imageStream) {
            this.imageStream = imageStream;
        }

        private byte[] getBytes(InputStream inputStream) throws IOException {
            ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream();
            int bufferSize = 1024;
            byte[] buffer = new byte[bufferSize];
            int len = 0;
            while ((len = inputStream.read(buffer)) != -1) {
                byteBuffer.write(buffer, 0, len);
            }
            return byteBuffer.toByteArray();
        }

        @Override
        protected String doInBackground(String... strings) {
            try {
                URL url = new URL(strings[0]);
                String imagePath = strings[1];
                if (executeRequest(url, imagePath)) {
                    return "";
                }
            } catch (Exception e) {
                Log.e(getClass().getCanonicalName(), "Error in request task", e);
            }
            return null;
        }

        boolean executeRequest(URL url, String imagePath) {
            try {
                byte[] inputData = getBytes(imageStream);
                RequestBody postBodyImage = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart("image", imagePath, RequestBody.create(MediaType.parse("image/*jpg"), inputData))
                    .build();

                OkHttpClient client = new OkHttpClient.Builder()
                    .connectTimeout(29, TimeUnit.SECONDS)
                    .writeTimeout(20, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .build();

                Request request = new Request.Builder()
                    .url(url)
                    .post(postBodyImage)
                    .build();

                Log.i(getClass().getCanonicalName(), "Submitting request");

                Response response = client.newCall(request).execute();
                if (response.isSuccessful()) {
                    Log.i(getClass().getCanonicalName(), "Image uploaded successfully");
                    return true;
                } else {
                    Log.e(getClass().getCanonicalName(), "Response is not successful" + response.code());
                }
                response.close();
            } catch (Exception e) {
                Log.e(getClass().getCanonicalName(), "Error in request task", e);
            }
            return false;
        }

    }
}
