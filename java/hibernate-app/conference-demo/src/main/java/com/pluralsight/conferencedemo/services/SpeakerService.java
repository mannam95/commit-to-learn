package com.pluralsight.conferencedemo.services;

import com.pluralsight.conferencedemo.dto.speaker.CreateSpeakerDto;
import com.pluralsight.conferencedemo.dto.speaker.UpdateSpeakerDto;
import com.pluralsight.conferencedemo.models.Speaker;
import com.pluralsight.conferencedemo.repositories.SpeakerRepository;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SpeakerService {
    @Autowired
    private SpeakerRepository speakerRepository;
    public SpeakerService() {
    }

    public List<Speaker> getAllSpeakers() {
        return speakerRepository.findAll();
    }

    public Speaker getSpeakerById(Long id) {
        return speakerRepository.getOne(id);
    }

    public Speaker createNewSpeaker(CreateSpeakerDto payload) {
        Speaker speaker = Speaker.builder()
                .firstName(payload.getFirstName())
                .lastName(payload.getLastName())
                .title(payload.getTitle())
                .company(payload.getCompany())
                .speakerBio(payload.getSpeakerBio())
                .speakerPhoto(payload.getSpeakerPhoto())
                .build();
        return speakerRepository.saveAndFlush(speaker);
    }

    public void deleteBySpeakerId(Long id) {
        speakerRepository.deleteById(id);
    }

    public Speaker updateSpeaker(Long id, UpdateSpeakerDto payload) {
        Speaker speaker = Speaker.builder()
                .firstName(payload.getFirstName())
                .lastName(payload.getLastName())
                .title(payload.getTitle())
                .company(payload.getCompany())
                .speakerBio(payload.getSpeakerBio())
                .speakerPhoto(payload.getSpeakerPhoto())
                .build();
        Speaker existingSpeaker = speakerRepository.getOne(id);
        BeanUtils.copyProperties(speaker, existingSpeaker, "Speaker_id");
        return speakerRepository.saveAndFlush(existingSpeaker);
    }
}
