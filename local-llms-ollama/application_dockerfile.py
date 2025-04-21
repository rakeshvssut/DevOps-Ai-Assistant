import os
import ollama
import json
import re

# Function to read a file
def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def detect_project_type(project_dir, files):
    """Detect the type of project based on its files"""
    
    # Check for Java/Gradle project
    if any(f.endswith(".gradle") for f in files) or "gradlew" in files or "build.gradle" in files:
        return "java-gradle"
    
    # Check for Java/Maven project
    if "pom.xml" in files:
        return "java-maven"
    
    # Check for Python project
    if any(f.endswith(".py") for f in files) or "requirements.txt" in files or "setup.py" in files:
        return "python"
    
    # Check for Node.js project
    if "package.json" in files or "node_modules" in files:
        return "nodejs"
    
    # Default to generic
    return "generic"

def get_prompt_for_project_type(project_type, project_dir, files):
    """Generate appropriate prompt based on project type"""
    
    if project_type == "java-gradle":
        # Try to find build.gradle for more context
        build_gradle = read_file(os.path.join(project_dir, "build.gradle"))
        
        return f"""
        Generate a **correct Dockerfile** for a Java Gradle project.
        
        - Use a proper Java base image (like Eclipse Temurin/OpenJDK 17 or latest LTS)
        - Use multi-stage build with proper stage names
        - Optimize for **layer caching**
        - Include gradle build steps with proper caching
        - Copy the built JAR file to the runtime image with CORRECT syntax
        - Set the correct ENTRYPOINT to run the application
        - Ensure all COPY commands have proper syntax with valid source and destination
        
        ### **Project Files:**
        {json.dumps(files, indent=2)}
        
        ### **build.gradle Content (if available):**
        {build_gradle if build_gradle else "Not available"}
        
        IMPORTANT: 
        - Make sure multi-stage build uses proper stage names
        - The COPY command must use proper syntax (e.g., COPY --from=builder /app/build/libs/*.jar app.jar)
        - Check all commands for syntax errors
        - Return ONLY the Dockerfile content with NO explanations and NO markdown formatting.
        """
    
    elif project_type == "java-maven":
        # Try to find pom.xml for more context
        pom_xml = read_file(os.path.join(project_dir, "pom.xml"))
        
        return f"""
        Generate a **correct Dockerfile** for a Java Maven project.
        
        - Use a proper Java base image (like Eclipse Temurin/OpenJDK 17 or latest LTS)
        - Use multi-stage build with proper stage names (e.g., 'builder', not 'build')
        - Optimize for **layer caching**
        - Include maven build steps with proper caching
        - Copy the built JAR file to the runtime image with CORRECT syntax
        - Set the correct ENTRYPOINT to run the application
        - Ensure all COPY commands have proper syntax with valid source and destination
        
        ### **Project Files:**
        {json.dumps(files, indent=2)}
        
        ### **pom.xml Content (if available):**
        {pom_xml if pom_xml else "Not available"}
        
        IMPORTANT: 
        - Make sure multi-stage build uses proper stage names
        - The COPY command must use proper syntax (e.g., COPY --from=builder /app/target/*.jar app.jar)
        - Check all commands for syntax errors
        - Return ONLY the Dockerfile content with NO explanations and NO markdown formatting.
        """
    
    elif project_type == "python":
        # Try to find requirements.txt for more context
        requirements = read_file(os.path.join(project_dir, "requirements.txt"))
        
        return f"""
        Generate a **correct Dockerfile** for a Python project.
        
        - Use the latest Python image (slim-buster variant recommended)
        - Optimize for **layer caching**
        - Install dependencies from requirements.txt if present
        - Use proper Python best practices for Docker
        - Set the correct ENTRYPOINT to run the application
        
        ### **Project Files:**
        {json.dumps(files, indent=2)}
        
        ### **requirements.txt Content (if available):**
        {requirements if requirements else "Not available"}
        
        IMPORTANT: Return ONLY the Dockerfile content with NO explanations and NO markdown formatting.
        """
    
    elif project_type == "nodejs":
        # Read package.json for better context
        package_json_content = read_file(os.path.join(project_dir, "package.json"))
        package_data = json.loads(package_json_content) if package_json_content else {}
        
        # Detect start command (default to "node src/index.js" if not found)
        start_command = package_data.get("scripts", {}).get("start", "node src/index.js")
        
        return f"""
        Generate a **correct Dockerfile** for a Node.js project.
        
        - Use the **latest Node.js LTS** (version 20 or higher)
        - Optimize for **layer caching**
        - Install dependencies using **npm ci**
        - **Expose the correct port** based on package.json (if defined)
        - **Use the correct start command**: `{start_command}`
        
        ### **Project Files:**
        {json.dumps(files, indent=2)}
        
        ### **package.json Content:**
        {json.dumps(package_data, indent=2)}
        
        IMPORTANT: Return ONLY the Dockerfile content with NO explanations and NO markdown formatting.
        """
    
    else:
        # Generic prompt for unknown project types
        return f"""
        Generate a **correct Dockerfile** for this project based on the file structure:
        
        ### **Project Files:**
        {json.dumps(files, indent=2)}
        
        IMPORTANT: Return ONLY the Dockerfile content with NO explanations and NO markdown formatting.
        """

def validate_dockerfile(content):
    """Perform basic validation on the Dockerfile content"""
    if not content or not content.strip():
        return False, "Empty Dockerfile content"
    
    # Check if it starts with FROM
    if not content.strip().startswith("FROM"):
        return False, "Dockerfile doesn't start with FROM"
    
    # Check for common syntax errors in COPY commands with --from
    copy_from_pattern = r'COPY\s+--from=([^\s]+)\s+([^\s]+)\s+([^\s]+)'
    matches = re.findall(copy_from_pattern, content)
    if matches:
        for match in matches:
            build_stage, source, dest = match
            if '/' in build_stage and not build_stage.startswith('"') and not build_stage.startswith("'"):
                return False, f"Invalid build stage name in COPY command: {build_stage}"
    
    return True, "Validation passed"

def generate_dockerfile(project_dir):
    """Generate a Dockerfile for the specified project directory"""
    
    # Get list of files and directories
    files = os.listdir(project_dir)
    
    # Detect project type
    project_type = detect_project_type(project_dir, files)
    print(f"Detected project type: {project_type}")
    
    # Generate appropriate prompt
    prompt = get_prompt_for_project_type(project_type, project_dir, files)
    
    # Call Ollama
    response = ollama.chat(model="llama3.2:latest", messages=[{"role": "user", "content": prompt}])
    content = response["message"]["content"]
    
    # Extract only the Dockerfile content using regex
    dockerfile_pattern = r"```dockerfile\s*([\s\S]*?)\s*```|```\s*([\s\S]*?)\s*```"
    matches = re.search(dockerfile_pattern, content)
    
    if matches:
        # Return the first non-empty group
        for group in matches.groups():
            if group:
                return group.strip()
    
    # If no markdown code blocks found, clean the content
    lines = content.split('\n')
    dockerfile_lines = []
    
    collecting = True  # Changed from False to True to collect all lines by default
    for line in lines:
        # Skip explanatory text at beginning that doesn't look like Dockerfile content
        if not dockerfile_lines and not line.strip():
            continue
        if not dockerfile_lines and not re.match(r'^(FROM|#|ARG)', line.strip()):
            continue
        
        dockerfile_lines.append(line)
    
    return '\n'.join(dockerfile_lines).strip()

# Main execution
if __name__ == "__main__":
    PROJECT_DIR = input("Enter project directory path: ")
    
    if not os.path.exists(PROJECT_DIR):
        print(f"Error: Directory '{PROJECT_DIR}' does not exist.")
        exit(1)
    
    dockerfile_content = generate_dockerfile(PROJECT_DIR)
    
    # Validate the Dockerfile
    is_valid, validation_message = validate_dockerfile(dockerfile_content)
    if not is_valid:
        print(f"⚠️ Warning: {validation_message}")
        
        # Retry with more specific instructions for problematic project types
        if "java" in detect_project_type(PROJECT_DIR, os.listdir(PROJECT_DIR)):
            print("Retrying with more explicit instructions for Java project...")
            retry_prompt = f"""
            Generate a Dockerfile for a Java project, focusing on correct syntax.
            
            IMPORTANT REQUIREMENTS:
            1. Use multiple stages with CLEAR stage names (use 'builder', not 'build')
            2. For multi-stage COPY commands, use proper syntax: COPY --from=builder /source/path /destination/path
            3. Ensure all COPY commands have proper source and destination
            4. The format must be "COPY --from=builder /path/to/source /path/to/destination"
            5. All stages must have an explicit name using AS keyword
            
            Project files: {json.dumps(os.listdir(PROJECT_DIR), indent=2)}
            
            Return ONLY valid Dockerfile content with NO explanations.
            """
            
            response = ollama.chat(model="llama3.2:latest", messages=[{"role": "user", "content": retry_prompt}])
            dockerfile_content = response["message"]["content"].strip()
            
            # Clean up the content
            dockerfile_pattern = r"```dockerfile\s*([\s\S]*?)\s*```|```\s*([\s\S]*?)\s*```"
            matches = re.search(dockerfile_pattern, dockerfile_content)
            if matches:
                for group in matches.groups():
                    if group:
                        dockerfile_content = group.strip()
                        break
    
    # Save the generated Dockerfile
    dockerfile_path = os.path.join(PROJECT_DIR, "Dockerfile")
    with open(dockerfile_path, "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    
    print(f"✅ Dockerfile generated successfully at: {dockerfile_path}")
    print("Preview of generated Dockerfile:")
    print("-----------------------------------")
    print(dockerfile_content[:500] + "..." if len(dockerfile_content) > 500 else dockerfile_content)
    print("-----------------------------------")