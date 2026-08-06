# Enterprise AI Research Platform

An Event-Driven Microservices platform that takes a user query, searches the web, reads multiple websites, and uses a local Large Language Model (via LM Studio) to synthesize a comprehensive research report.

## Architecture

This project has been refactored into a scalable Microservices architecture:
* **API Gateway & Core Service**: Java Spring Boot 
* **Message Broker**: RabbitMQ
* **AI Worker**: Python (Pydantic, pika, pydantic-settings)
* **Database**: PostgreSQL
* **LLM Provider**: LM Studio (Local)
* **Search/Scraping**: Tavily API, Jina AI

## Infrastructure Setup

1. **Start Infrastructure (Docker)**
   ```bash
   docker-compose up -d
   ```
   This spins up PostgreSQL (5433) and RabbitMQ (5672, Dashboard: 15672).

2. **Start the Java API (Backend)**
   ```bash
   cd backend
   mvn clean spring-boot:run
   ```

3. **Start the Python AI Worker**
   ```bash
   cd ai-worker
   pip install -r requirements.txt
   python main.py --worker
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   TAVILY_API_KEY="your_tavily_token"
   ```

## Usage
Submit a research task via the Spring Boot API:
```bash
curl -X POST http://localhost:8080/api/research -H "Content-Type: application/json" -d "{\"topic\": \"Artificial Intelligence in Healthcare\"}"
```
