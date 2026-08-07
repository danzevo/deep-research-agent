# Stage 1: Build the application using Maven
FROM maven:3.9.6-eclipse-temurin-17-alpine as builder
WORKDIR /app
# Copy the pom.xml and source code
COPY pom.xml .
COPY src ./src
# Build the jar file (skipping tests for speed in CI)
RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
# Copy the built jar from the builder stage
COPY --from=builder /app/target/*.jar app.jar
# Expose the Spring Boot port
EXPOSE 8080
# Run the jar
ENTRYPOINT ["java", "-jar", "app.jar"]