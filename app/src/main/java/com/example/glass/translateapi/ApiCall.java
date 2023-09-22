package com.example.glass.translateapi;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

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

    public void performAPIRequest(final ResponseCallback callback) {
        Call<Object> call = apiInterface.getData();

        call.enqueue(new Callback<Object>() {
            @Override
            public void onResponse(Response<Object> response) {
                if (response.isSuccess()) {
                    // Handle the API response here
                    callback.onSuccess("Success Resp");
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
