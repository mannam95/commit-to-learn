package com.pluralsight.conferencedemo.dto.session;


import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor

public class UpdateSessionDto {
    @NotBlank(message = "session name is mandatory")
    String name;
    String description;
    int length;
}
