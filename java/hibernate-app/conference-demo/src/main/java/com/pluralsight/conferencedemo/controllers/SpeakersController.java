package com.pluralsight.conferencedemo.controllers;

import com.pluralsight.conferencedemo.dto.speaker.CreateSpeakerDto;
import com.pluralsight.conferencedemo.dto.speaker.UpdateSpeakerDto;
import com.pluralsight.conferencedemo.models.Speaker;
import com.pluralsight.conferencedemo.services.SpeakerService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/speakers")
@Validated
public class SpeakersController {
    @Autowired
    private SpeakerService speakerService;

    @GetMapping
    public List<Speaker> list() {
        return speakerService.getAllSpeakers();
    }

    @GetMapping
    @RequestMapping("{id}")
    public Speaker get(@PathVariable Long id) {
        return speakerService.getSpeakerById(id);
    }

    @PostMapping
    public Speaker create(@RequestBody @Valid CreateSpeakerDto speaker) {
        return speakerService.createNewSpeaker(speaker);
    }

    @RequestMapping(value = "{id}", method = RequestMethod.DELETE)
    public void delete(@PathVariable Long id) {
        speakerService.deleteBySpeakerId(id);
    }

    @RequestMapping(value = "{id}", method = RequestMethod.PUT)
    public Speaker update(@PathVariable Long id, @RequestBody @Valid UpdateSpeakerDto speaker) {
        return speakerService.updateSpeaker(id, speaker);
    }
}
