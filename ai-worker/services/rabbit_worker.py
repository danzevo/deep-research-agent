import pika
import json
import time
from core.config import settings

from core.database import get_session
from services.agent_service import run_research

def _process_task(ch, method, properties, body):
    """Callback function that handles incoming messages"""
    print("\n--------------------------------------------------")
    print(f" [x] Received raw message: {body}")

    task_data = json.loads(body)
    task_id = task_data.get('id')
    topic = task_data.get('topic')

    print(f" [x] Task ID: {task_data.get('id')}")
    print(f" [x] Topic to research: {task_data.get('topic')}")

    # 2. Open a database session (just like in your old main.py)
    session = next(get_session())

    try:
        print(f" [x] Starting AI research for topic: '{topic}'...")

        # 3. Run your actual AI agent!
        result = run_research(topic, session)

        if result:
            print(f" [x] Research completed successfully!")
            
            # 1. Package the result into a JSON dictionary
            result_payload = {
                "id": task_id,
                "resultMarkdown": result.report_markdown
            }

            # 2. Publish it back to RabbitMQ so Java can hear it!
            # We use the exact exchange and routing key we set up in application.yml
            ch.basic_publish(
                exchange="research_exchange",
                routing_key="result.routing.key",
                body=json.dumps(result_payload),
                properties=pika.BasicProperties(
                    content_type='application/json'
                )
            )
            print(" [x] Report sent back to Java successfully!")
            
    except Exception as e:
        print(f" [x] ERROR during research: {e}")
    finally:
        # 4. Clean up the database session
        session.close()

    # 5. Tell RabbitMQ we are finished with this task
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done! Waiting for next task...")
    print("--------------------------------------------------\n")

def start_worker():
    """Connects to RabbitMQ and starts listening"""
    print(f"[*] Connecting to RabbitMQ at {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}...")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, heartbeat=600)
    )
    channel = connection.channel()

    # Ensure queue exists
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

    # Attach the callback function
    channel.basic_consume(
        queue=settings.RABBITMQ_QUEUE,
        on_message_callback=_process_task, auto_ack=False
    )

    print(f"[*] Waiting for tasks on queue '{settings.RABBITMQ_QUEUE}'. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
        connection.close()