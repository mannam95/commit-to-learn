package com.pluralsight.conferencedemo.services;

import com.pluralsight.conferencedemo.dto.session.CreateSessionDto;
import com.pluralsight.conferencedemo.dto.session.UpdateSessionDto;
import com.pluralsight.conferencedemo.models.Session;
import com.pluralsight.conferencedemo.repositories.SessionRepository;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SessionService {
    @Autowired
    private SessionRepository sessionRepository;
    public SessionService() {
    }

    public List<Session> getAllSessions() {
        return sessionRepository.findAll();
    }

    public Session getSessionById(Long id) {
        return sessionRepository.getOne(id);
    }

    public Session createNewSession(CreateSessionDto payload) {
        Session session = Session.builder()
                .sessionName(payload.getName())
                .sessionDescription(payload.getDescription())
                .sessionLength(payload.getLength())
                .build();
        return sessionRepository.saveAndFlush(session);
    }

    public void deleteBySessionId(Long id) {
        sessionRepository.deleteById(id);
    }

    public Session updateSession(Long id, UpdateSessionDto payload) {
        Session session = Session.builder()
                .sessionName(payload.getName())
                .sessionDescription(payload.getDescription())
                .sessionLength(payload.getLength())
                .build();
        Session existingSession = sessionRepository.getOne(id);
        BeanUtils.copyProperties(session, existingSession, "session_id");
        return sessionRepository.saveAndFlush(existingSession);
    }
}
