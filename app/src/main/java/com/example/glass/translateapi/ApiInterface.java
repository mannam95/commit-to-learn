package com.example.glass.translateapi;

import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface ApiInterface {
    @POST("get_translated_text")
    Call<Object> getData(@Body RequestBody requestBody);
}
