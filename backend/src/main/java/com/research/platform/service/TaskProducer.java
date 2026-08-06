package com.research.platform.service;

import com.research.platform.entity.ResearchTask;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j // Lombok annotation to easily use 'log.info()'
public class TaskProducer {
    private final RabbitTemplate rabbitTemplate;

    @Value("${app.rabbitmq.exchange}")
    private String exchange;

    @Value("${app.rabbitmq.routing-key-task}")
    private String routingKey;

    public void sendTaskToPython(ResearchTask task) {
        log.info("Publishing task ID {} to RabbitMQ...", task.getId());
        // Sends the task object to the exchange using the routing key we configured
        rabbitTemplate.convertAndSend(exchange, routingKey, task);

        log.info("Task published successfully");
    }
}