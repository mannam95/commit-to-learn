package com.example.glass.translateapi;

import retrofit2.Call;
import retrofit2.http.GET;

public interface ApiInterface {
    @GET("todos/1")
    Call<Object> getData();
}
