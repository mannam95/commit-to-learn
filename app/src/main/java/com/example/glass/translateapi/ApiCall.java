package com.example.glass.translateapi;

import android.util.Log;

import com.google.gson.Gson;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import okhttp3.MultipartBody;
import javax.net.ssl.HttpsURLConnection;

import okhttp3.MediaType;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class ApiCall {
    private ApiService apiService;
    private ApiInterface apiInterface;

    public ApiCall() {
        apiService = ApiService.getInstance();
        apiInterface = apiService.getApiInterface();
    }

    public interface ResponseCallback {
        void onSuccess(String response);

        void onError(String response);
    }

    public void performAPIRequest(final ResponseCallback callback, byte[] imageData) {
        MultipartBody.Builder builder = new MultipartBody.Builder();
        builder.setType(MultipartBody.FORM);

        RequestBody requestBody = RequestBody.create(MediaType.parse("multipart/form-data"), imageData);

        builder.addFormDataPart("fileName", "image.jpg", requestBody);

        MultipartBody requestBodyNew = builder.build();

        // Create MultipartBody.Part using file name and RequestBody
        // MultipartBody.Part body = MultipartBody.Part.createFormData("fileName", "image.jpg", requestBody);

        Call<Object> call = apiInterface.getData(requestBodyNew);

        call.enqueue(new Callback<Object>() {
            @Override
            public void onResponse(Response<Object> response) {
                if (response.isSuccess()) {
                    Gson gson = new Gson();

                    String jsonResponseBody = gson.toJson(response.body());

                    ApiResponse apiResponse = gson.fromJson(jsonResponseBody, ApiResponse.class);

                    Log.d("API {arsed Response", apiResponse.getTransText());

                    // Handle the API response here
                    callback.onSuccess(apiResponse.getTransText());
                } else {
                    // Handle error cases
                    callback.onError("Error Resp Else");
                }
            }

            @Override
            public void onFailure(Throwable t) {
                // Handle network failures
                callback.onError("Error Resp Others");
            }
        });
    }
}
