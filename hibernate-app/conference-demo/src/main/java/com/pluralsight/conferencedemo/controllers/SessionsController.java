package com.pluralsight.conferencedemo.controllers;

import com.pluralsight.conferencedemo.dto.session.CreateSessionDto;
import com.pluralsight.conferencedemo.dto.session.UpdateSessionDto;
import com.pluralsight.conferencedemo.models.Session;
import com.pluralsight.conferencedemo.services.SessionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/sessions")
@Validated
public class SessionsController {
    @Autowired
    private SessionService sessionService;

    @GetMapping
    public List<Session> list() {
        return sessionService.getAllSessions();
    }

    @GetMapping
    @RequestMapping("{id}")
    public Session get(@PathVariable Long id) {
        return sessionService.getSessionById(id);
    }

    @PostMapping
    public Session create(@RequestBody @Valid CreateSessionDto session) {
        return sessionService.createNewSession(session);
    }

    @RequestMapping(value = "{id}", method = RequestMethod.DELETE)
    public void delete(@PathVariable Long id) {
        sessionService.deleteBySessionId(id);
    }

    @RequestMapping(value = "{id}", method = RequestMethod.PUT)
    public Session update(@PathVariable Long id, @RequestBody @Valid UpdateSessionDto session) {
        return sessionService.updateSession(id, session);
    }
}
