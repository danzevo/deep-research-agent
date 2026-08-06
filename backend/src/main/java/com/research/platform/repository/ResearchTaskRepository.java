package com.research.platform.repository;

import com.research.platform.entity.ResearchTask;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ResearchTaskRepository extends JpaRepository<ResearchTask, Long> {
// JpaRepository gives us built-in methods like save(), findById(), and findAll()
}