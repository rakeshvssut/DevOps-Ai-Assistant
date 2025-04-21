FROM eclipse/temurin:17-jdk-17 as build

# Set the working directory to /app
WORKDIR /app

# Copy Maven settings file
COPY pom.xml /app/

# Add Maven dependencies to the image
RUN mkdir -p /app/target
RUN mvn dependency:resolve -Dmaven.test.skip=true

# Compile and package the application
RUN mvn clean package -DskipTests

# Copy the JAR file to the runtime image
COPY --from=build/target/* .

# Set the entrypoint for the container
CMD ["java", "-jar", "hello-world.jar"]

EXPOSE 8080

FROM eclipse/temurin:17-jdk-17 as runtime

# Set the working directory to /app
WORKDIR /app

# Copy the JAR file to the runtime image
COPY --from=latest hello-world.jar .

# Set the entrypoint for the container
CMD ["java", "-jar", "hello-world.jar"]

EXPOSE 8080