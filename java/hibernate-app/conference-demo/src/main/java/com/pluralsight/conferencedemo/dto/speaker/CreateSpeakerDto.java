package com.pluralsight.conferencedemo.dto.speaker;


import jakarta.persistence.Lob;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor

public class CreateSpeakerDto {
    @NotBlank(message = "first name is mandatory")
    String firstName;
    String lastName;
    String title;
    String company;
    String speakerBio;
    @Lob
    byte[] speakerPhoto;
}