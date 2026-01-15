import asyncio
import os
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

from app.model.snippet import Snippet, Visibility, User
from app.model.object_id import PyObjectId
from app.services.snippet_service import SnippetService
from app.repositories.snippet_repository import SnippetRepository
from app.connectors.grpc_search_connector import GRPCSearchConnector


class ImmediateBackgroundTasks:
    def add_task(self, func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            asyncio.create_task(func(*args, **kwargs))
        else:
            func(*args, **kwargs)


async def seed_database():
    load_dotenv()

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_USER = os.environ.get("MONGO_USER", "root")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "example")
    MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/admin?authSource=admin"

    mongo_client = AsyncMongoClient(MONGO_URL)
    db = mongo_client["codesnip"]
    collection = db["snippets"]

    repository = SnippetRepository(collection)
    search_connector = GRPCSearchConnector()
    bg_tasks = ImmediateBackgroundTasks()

    service = SnippetService(
        repository=repository,
        search_connector_client=search_connector,
        background_tasks=bg_tasks
    )

    seed_user = User(
        id="seed_master_001",
        username="SeedMaster",
        email_hash="d41d8cd98f00b204e9800998ecf8427e"
    )

    raw_data = [
        ("Binary Search", "Standard binary search implementation for sorted arrays.",
         "def binary_search(arr, x):\n    low = 0\n    high = len(arr) - 1\n    mid = 0\n    while low <= high:\n        mid = (high + low) // 2\n        if arr[mid] < x:\n            low = mid + 1\n        elif arr[mid] > x:\n            high = mid - 1\n        else:\n            return mid\n    return -1",
         "python", Visibility.PUBLIC),
        ("React useEffect", "Example of using useEffect hook for side effects.",
         "useEffect(() => {\n  const timer = setTimeout(() => {\n    console.log('Delayed log');\n  }, 1000);\n  return () => clearTimeout(timer);\n}, []);",
         "javascript", Visibility.PUBLIC),
        ("SQL Inner Join", "Basic SQL query to join two tables.",
         "SELECT users.name, orders.amount\nFROM users\nINNER JOIN orders ON users.id = orders.user_id;", "sql",
         Visibility.PUBLIC),
        ("Docker Compose", "Setup for a simple web service and redis.",
         "version: '3'\nservices:\n  web:\n    build: .\n    ports:\n      - '5000:5000'\n  redis:\n    image: 'redis:alpine'",
         "yaml", Visibility.PUBLIC),
        ("FastAPI Setup", "Minimal FastAPI application structure.",
         "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
         "python", Visibility.PUBLIC),
        ("Go Goroutine", "Spawning a concurrent goroutine in Go.",
         "package main\nimport \"fmt\"\n\nfunc main() {\n    go func() {\n        fmt.Println(\"Async work\")\n    }()\n    fmt.Println(\"Main thread\")\n}",
         "go", Visibility.PUBLIC),
        ("Rust Mutex", "Using Mutex for thread-safe data access.",
         "use std::sync::{Arc, Mutex};\nuse std::thread;\n\nfn main() {\n    let counter = Arc::new(Mutex::new(0));\n    let mut handles = vec![];\n\n    for _ in 0..10 {\n        let counter = Arc::clone(&counter);\n        let handle = thread::spawn(move || {\n            let mut num = counter.lock().unwrap();\n            *num += 1;\n        });\n        handles.push(handle);\n    }\n}",
         "rust", Visibility.PRIVATE),
        ("CSS Flex Center", "Centering a div utilizing Flexbox.",
         ".container {\n  display: flex;\n  justify_content: center;\n  align_items: center;\n  height: 100vh;\n}",
         "css", Visibility.PUBLIC),
        ("AWS S3 Policy", "JSON policy for public read access.",
         "{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"PublicReadGetObject\",\n      \"Effect\": \"Allow\",\n      \"Principal\": \"*\",\n      \"Action\": \"s3:GetObject\",\n      \"Resource\": \"arn:aws:s3:::example-bucket/*\"\n    }\n  ]\n}",
         "json", Visibility.PUBLIC),
        ("Kubernetes Pod", "Simple Pod definition for Nginx.",
         "apiVersion: v1\nkind: Pod\nmetadata:\n  name: nginx\nspec:\n  containers:\n  - name: nginx\n    image: nginx:1.14.2\n    ports:\n    - containerPort: 80",
         "yaml", Visibility.PUBLIC),
        ("Java Singleton", "Thread-safe Singleton pattern implementation.",
         "public class Singleton {\n    private static volatile Singleton instance;\n\n    private Singleton() {}\n\n    public static Singleton getInstance() {\n        if (instance == null) {\n            synchronized (Singleton.class) {\n                if (instance == null) {\n                    instance = new Singleton();\n                }\n            }\n        }\n        return instance;\n    }\n}",
         "java", Visibility.PUBLIC),
        ("Git Ignore", "Standard .gitignore for Python projects.",
         "__pycache__/\n*.py[cod]\n*$py.class\n.env\nvenv/\n.vscode/", "text", Visibility.PUBLIC),
        ("HTML5 Template", "Basic HTML5 boilerplate structure.",
         "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n<body>\n    <h1>Hello</h1>\n</body>\n</html>",
         "html", Visibility.PUBLIC),
        ("C++ Pointers", "Demonstration of pointer arithmetic.",
         "#include <iostream>\nusing namespace std;\n\nint main() {\n    int arr[] = {10, 20, 30};\n    int *ptr = arr;\n    ptr++;\n    cout << *ptr; // Outputs 20\n    return 0;\n}",
         "cpp", Visibility.PRIVATE),
        ("Pandas CSV Read", "Reading a CSV file into a DataFrame.",
         "import pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.head())", "python", Visibility.PUBLIC),
        ("TypeScript Interface", "Defining a User interface in TS.",
         "interface User {\n  id: number;\n  name: string;\n  email?: string;\n}\n\nconst user: User = {\n  id: 1,\n  name: \"Alice\"\n};",
         "typescript", Visibility.PUBLIC),
        ("Bash Loop", "Simple for loop in Bash script.",
         "#!/bin/bash\nfor i in {1..5}\ndo\n   echo \"Welcome $i times\"\ndone", "bash", Visibility.PUBLIC),
        ("GraphQL Query", "Fetching user data via GraphQL.",
         "query {\n  user(id: \"1\") {\n    firstName\n    lastName\n    email\n  }\n}", "graphql", Visibility.PUBLIC),
        ("Redis Set/Get", "Basic Redis commands.", "SET mykey \"Hello\"\nGET mykey", "redis", Visibility.PUBLIC),
        ("Vue.js Component", "Single file component example.",
         "<template>\n  <button @click=\"count++\">{{ count }}</button>\n</template>\n\n<script>\nexport default {\n  data() {\n    return { count: 0 }\n  }\n}\n</script>",
         "javascript", Visibility.PUBLIC),
        ("SwiftUI View", "Basic text view in SwiftUI.",
         "import SwiftUI\n\nstruct ContentView: View {\n    var body: some View {\n        Text(\"Hello, World!\")\n            .padding()\n    }\n}",
         "swift", Visibility.PUBLIC),
        ("Kotlin Coroutine", "Delaying execution with coroutines.",
         "import kotlinx.coroutines.*\n\nfun main() = runBlocking {\n    launch {\n        delay(1000L)\n        println(\"World!\")\n    }\n    println(\"Hello,\")\n}",
         "kotlin", Visibility.PUBLIC),
        ("Terraform EC2", "Defining an AWS instance resource.",
         "resource \"aws_instance\" \"web\" {\n  ami           = \"ami-12345678\"\n  instance_type = \"t2.micro\"\n\n  tags = {\n    Name = \"HelloWorld\"\n  }\n}",
         "hcl", Visibility.PUBLIC),
        ("Makefile", "Simple build command for Go app.", "build:\n\tgo build -o bin/app main.go\n\nrun:\n\t./bin/app",
         "makefile", Visibility.PUBLIC),
        ("C# Async Task", "Asynchronous method in C#.",
         "public async Task<string> GetDataAsync()\n{\n    using (var client = new HttpClient())\n    {\n        return await client.GetStringAsync(\"http://example.com\");\n    }\n}",
         "csharp", Visibility.PUBLIC),
        ("PHP PDO Connect", "Connecting to MySQL using PDO.",
         "$dsn = 'mysql:host=localhost;dbname=testdb';\n$username = 'root';\n$password = '';\n\ntry {\n    $dbh = new PDO($dsn, $username, $password);\n} catch (PDOException $e) {\n    echo 'Connection failed: ' . $e->getMessage();\n}",
         "php", Visibility.PUBLIC),
        ("Ruby on Rails Route", "Defining a simple GET route.",
         "Rails.application.routes.draw do\n  get '/welcome', to: 'pages#home'\nend", "ruby", Visibility.PUBLIC),
        ("Scala Actor", "Simple Akka actor definition.",
         "import akka.actor.Actor\n\nclass HelloActor extends Actor {\n  def receive = {\n    case \"hello\" => println(\"hello back at you\")\n    case _       => println(\"huh?\")\n  }\n}",
         "scala", Visibility.PRIVATE),
        ("Elixir Match", "Pattern matching in Elixir function.",
         "defmodule Math do\n  def zero?(0), do: true\n  def zero?(x) when is_integer(x), do: false\nend", "elixir",
         Visibility.PUBLIC),
        ("Haskell Factorial", "Recursive factorial implementation.",
         "factorial :: Integer -> Integer\nfactorial 0 = 1\nfactorial n = n * factorial (n - 1)", "haskell",
         Visibility.PUBLIC),
        ("Lua Script", "Defining a function in Lua.",
         "function factorial(n)\n  if n == 0 then\n    return 1\n  else\n    return n * factorial(n - 1)\n  end\nend",
         "lua", Visibility.PUBLIC),
        ("PowerShell Get", "Filtering processes by handle count.",
         "Get-Process | Where-Object {$_.Handles -gt 1000} | Select-Object ProcessName, Handles", "powershell",
         Visibility.PUBLIC),
        ("Ansible Playbook", "Ensuring a service is running.",
         "- hosts: webservers\n  tasks:\n    - name: Ensure nginx is running\n      service:\n        name: nginx\n        state: started",
         "yaml", Visibility.PUBLIC),
        (
        "Prometheus Query", "Calculating request rate over 5m.", "rate(http_requests_total{job=\"api\"}[5m])", "promql",
        Visibility.PUBLIC),
        ("Elasticsearch JSON", "Search query for matching text.",
         "{\n  \"query\": {\n    \"match\": {\n      \"message\": \"error\"\n    }\n  }\n}", "json", Visibility.PUBLIC),
        ("Tailwind Button", "Styled button with hover state.",
         "<button class=\"bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded\">\n  Button\n</button>",
         "html", Visibility.PUBLIC),
        ("Next.js Page", "Simple page component with export.",
         "export default function Home() {\n  return <h1>Welcome to Next.js!</h1>\n}", "javascript", Visibility.PUBLIC),
        ("Django Model", "Defining a database model for Blog.",
         "from django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()\n    pub_date = models.DateTimeField('date published')",
         "python", Visibility.PUBLIC),
        ("Flask Route", "Route with URL parameter.",
         "from flask import Flask\napp = Flask(__name__)\n\n@app.route('/user/<username>')\ndef show_user_profile(username):\n    return f'User {username}'",
         "python", Visibility.PUBLIC),
        ("Spring Boot App", "Main class for Spring Boot.",
         "@SpringBootApplication\npublic class Application {\n    public static void main(String[] args) {\n        SpringApplication.run(Application.class, args);\n    }\n}",
         "java", Visibility.PUBLIC),
        ("Arduino Blink", "Loop to blink the built-in LED.",
         "void setup() {\n  pinMode(LED_BUILTIN, OUTPUT);\n}\n\nvoid loop() {\n  digitalWrite(LED_BUILTIN, HIGH);\n  delay(1000);\n  digitalWrite(LED_BUILTIN, LOW);\n  delay(1000);\n}",
         "cpp", Visibility.PUBLIC),
        ("Matlab Plot", "Plotting a sine wave.", "x = 0:pi/100:2*pi;\ny = sin(x);\nplot(x,y)\ntitle('Sine Wave')",
         "matlab", Visibility.PRIVATE),
        ("R DataFrame", "Creating a data frame in R.",
         "employees <- data.frame(\n  Name = c(\"John\", \"Jane\"),\n  Age = c(30, 25),\n  Role = c(\"Dev\", \"Designer\")\n)",
         "r", Visibility.PUBLIC),
        ("Dart Flutter", "Stateless widget structure.",
         "import 'package:flutter/material.dart';\n\nclass MyWidget extends StatelessWidget {\n  @override\n  Widget build(BuildContext context) {\n    return Container();\n  }\n}",
         "dart", Visibility.PUBLIC),
        ("Assembly x86", "Moving value to register.",
         "section .text\n  global _start\n\n_start:\n  mov eax, 1\n  mov ebx, 42\n  int 0x80", "assembly",
         Visibility.PRIVATE),
        ("Perl Regex", "Substituting text in a string.",
         "my $string = \"The cat sat on the mat.\";\n$string =~ s/cat/dog/;\nprint $string;", "perl",
         Visibility.PUBLIC),
        ("Groovy Script", "Simple print in Groovy.", "def name = 'World'\nprintln \"Hello ${name}\"", "groovy",
         Visibility.PUBLIC),
        ("Nginx Config", "Reverse proxy configuration block.",
         "server {\n    listen 80;\n    location / {\n        proxy_pass http://localhost:3000;\n        proxy_http_version 1.1;\n    }\n}",
         "nginx", Visibility.PUBLIC),
        ("Regex Email", "Pattern to validate email address.", "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
         "text", Visibility.PUBLIC),
        ("Batch Script", "Echo off and print hello.", "@echo off\necho Hello World\npause", "batch", Visibility.PUBLIC),
    ]

    print(f"Starting seed of {len(raw_data)} snippets...")

    try:
        inserted_count = 0
        for title, desc, code, lang, vis in raw_data:
            new_id = ObjectId()

            snippet_model = Snippet(
                id=PyObjectId(str(new_id)),
                title=title,
                description=desc,
                code=code,
                language=lang,
                visibility=vis,
                author=seed_user,
                created_at=datetime.now()
            )

            created = await service.add_snippet(snippet_model)

            print(f"[{inserted_count + 1}/{len(raw_data)}] Created: {created.title} ({created.language})")
            inserted_count += 1

        print("Waiting for background indexing tasks...")
        await asyncio.sleep(3)

    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await mongo_client.close()
        if hasattr(search_connector, 'close'):
            await search_connector.close()
        print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(seed_database())