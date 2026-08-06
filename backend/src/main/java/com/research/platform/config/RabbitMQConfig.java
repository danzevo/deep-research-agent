package com.research.platform.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {
    @Value("${app.rabbitmq.exchange}")
    private String exchangeName;

    @Value("${app.rabbitmq.task-queue}")
    private String taskQueueName;

    @Value("${app.rabbitmq.result_queue}")
    private String resultQueueName;

    @Value("${app.rabbitmq.routing-key-task}")
    private String taskRoutingKey;

    @Value("${app.rabbitmq.routing-key-result}")
    private String resultRoutingKey;

    // 1. Define the Queues
    @Bean
    public Queue taskQueue() {
        return new Queue(taskQueueName, true); // true = durable (survives restarts)
    }

    @Bean
    public Queue resultQueue() {
        return new Queue(resultQueueName, true);
    }

    // 2. Define the Exchange
    @Bean
    public DirectExchange exchange() {
        return new DirectExchange(exchangeName);
    }

    // 3. Bind the Queues to the Exchange using Routing Keys
    @Bean
    public Binding taskBinding(Queue taskQueue, DirectExchange exchange) {
        return BindingBuilder.bind(taskQueue).to(exchange).with(taskRoutingKey);
    }

    @Bean 
    public Binding resultBinding(Queue resultQueue, DirectExchange exchange) {
        return BindingBuilder.bind(resultQueue).to(exchange).with(resultRoutingKey);
    }

    // 4. Message Converter (to send Java Objects as JSON automatically)
    @Bean
    public MessageConverter jsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }
}