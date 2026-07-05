"""
Management command to populate the database with sample data.
Run once after migrations:   python manage.py seed_data

This is useful both for local development and for Render's first deploy.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.courses.models import Category, Course, Instructor, Lesson, Module
from apps.blog.models import Post, Tag

User = get_user_model()

CATEGORIES = ["Python", "JavaScript", "Data Science", "Machine Learning", "Web Development", "UI/UX Design", "DevOps", "Mobile Development"]
TAGS = ["Python", "JavaScript", "React", "Django", "Machine Learning", "Data Science", "Career", "Tutorial", "Web Dev", "AI"]


class Command(BaseCommand):
    help = "Seed the database with sample courses and blog posts."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Superuser
        if not User.objects.filter(email="admin@mentorbyte.com").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@mentorbyte.com",
                password="Admin@1234",
                full_name="Admin User",
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Superuser created (admin@mentorbyte.com / Admin@1234)"))
        else:
            admin = User.objects.get(email="admin@mentorbyte.com")

        # Categories
        categories = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat
        self.stdout.write(f"  ✓ {len(categories)} categories")

        # Tags
        tags = {}
        for name in TAGS:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags[name] = tag
        self.stdout.write(f"  ✓ {len(tags)} tags")

        # Instructors
        instructors_data = [
            {"name": "Dr. Sarah Chen", "title": "Senior Data Scientist", "bio": "Former Google engineer with 12 years in ML."},
            {"name": "Mike Rodriguez", "title": "Full Stack Developer", "bio": "React & Django specialist. Open source contributor."},
            {"name": "Prof. James Kim", "title": "ML Research Lead", "bio": "PhD in AI from Stanford. Published 40+ papers."},
            {"name": "Anna Thompson", "title": "Backend Architect", "bio": "Node.js & Python expert, AWS certified."},
            {"name": "David Park", "title": "UI/UX Lead", "bio": "Design lead at top SaaS companies for 10 years."},
        ]
        instructors = []
        for data in instructors_data:
            inst, _ = Instructor.objects.get_or_create(name=data["name"], defaults=data)
            instructors.append(inst)
        self.stdout.write(f"  ✓ {len(instructors)} instructors")

        # Courses
        courses_data = [
            {
                "title": "Complete Python Bootcamp for Beginners",
                "category": "Python",
                "instructor": instructors[0],
                "short_description": "Learn Python from scratch — variables to OOP — with 50+ real projects.",
                "description": "This comprehensive Python course covers everything from the absolute basics to advanced topics like decorators, generators, and async programming. Perfect for beginners who want a solid foundation.",
                "level": "beginner",
                "price": 49.99,
                "discount_price": 19.99,
                "duration_hours": 22,
                "is_featured": True,
                "students_count": 42500,
                "what_you_will_learn": ["Python syntax and data types", "Functions and OOP", "File handling", "Web scraping with BeautifulSoup", "Build 10+ real projects"],
                "requirements": ["No prior programming experience needed", "A computer with internet access"],
                "modules": [
                    {"title": "Getting Started", "lessons": [{"title": "Installing Python & VS Code", "duration_minutes": 10, "is_preview": True}, {"title": "Your First Python Program", "duration_minutes": 15, "is_preview": True}]},
                    {"title": "Python Fundamentals", "lessons": [{"title": "Variables and Data Types", "duration_minutes": 25}, {"title": "Control Flow", "duration_minutes": 30}, {"title": "Functions", "duration_minutes": 35}]},
                    {"title": "Object-Oriented Programming", "lessons": [{"title": "Classes and Objects", "duration_minutes": 40}, {"title": "Inheritance", "duration_minutes": 30}]},
                ],
            },
            {
                "title": "Django REST Framework Masterclass",
                "category": "Python",
                "instructor": instructors[1],
                "short_description": "Build production-ready REST APIs with Django, DRF, JWT, and PostgreSQL.",
                "description": "A deep dive into building scalable REST APIs with Django REST Framework. We cover authentication, permissions, serializers, viewsets, filtering, and deployment to Render.",
                "level": "intermediate",
                "price": 79.99,
                "discount_price": 29.99,
                "duration_hours": 18,
                "is_featured": True,
                "students_count": 18200,
                "what_you_will_learn": ["DRF serializers and views", "JWT authentication", "PostgreSQL integration", "Testing with pytest", "Deploy to Render"],
                "requirements": ["Basic Python knowledge", "Familiarity with web concepts"],
                "modules": [
                    {"title": "DRF Basics", "lessons": [{"title": "Serializers Deep Dive", "duration_minutes": 35, "is_preview": True}, {"title": "ViewSets and Routers", "duration_minutes": 30}]},
                    {"title": "Authentication", "lessons": [{"title": "JWT Auth Setup", "duration_minutes": 25}, {"title": "Permissions & Throttling", "duration_minutes": 20}]},
                ],
            },
            {
                "title": "Machine Learning A-Z with Python",
                "category": "Machine Learning",
                "instructor": instructors[2],
                "short_description": "From linear regression to deep learning — hands-on ML with real datasets.",
                "description": "The most complete Machine Learning course covering supervised, unsupervised, and reinforcement learning. Build end-to-end ML pipelines using scikit-learn, TensorFlow, and Pandas.",
                "level": "intermediate",
                "price": 99.99,
                "discount_price": 39.99,
                "duration_hours": 40,
                "is_featured": True,
                "students_count": 63000,
                "what_you_will_learn": ["Regression & Classification", "Decision Trees & Random Forests", "Neural Networks", "Model evaluation & tuning", "Deploy ML models"],
                "requirements": ["Python basics", "High school math"],
                "modules": [
                    {"title": "Data Preprocessing", "lessons": [{"title": "Pandas Fundamentals", "duration_minutes": 45, "is_preview": True}, {"title": "Feature Engineering", "duration_minutes": 40}]},
                    {"title": "Supervised Learning", "lessons": [{"title": "Linear Regression", "duration_minutes": 50}, {"title": "Logistic Regression", "duration_minutes": 45}, {"title": "SVM", "duration_minutes": 40}]},
                ],
            },
            {
                "title": "React & TypeScript — The Complete Guide",
                "category": "JavaScript",
                "instructor": instructors[1],
                "short_description": "Build modern, type-safe React applications with TypeScript, hooks, and state management.",
                "description": "A practical React + TypeScript course that covers everything from JSX basics to advanced patterns like compound components, render props, and full-stack integration with REST APIs.",
                "level": "intermediate",
                "price": 69.99,
                "discount_price": None,
                "duration_hours": 28,
                "is_featured": True,
                "students_count": 29400,
                "what_you_will_learn": ["TypeScript with React", "Hooks in depth", "Context API & Zustand", "React Query for API calls", "Deploy to Netlify"],
                "requirements": ["JavaScript basics", "HTML/CSS fundamentals"],
                "modules": [
                    {"title": "TypeScript Basics", "lessons": [{"title": "Types & Interfaces", "duration_minutes": 30, "is_preview": True}, {"title": "Generics", "duration_minutes": 25}]},
                    {"title": "React Hooks", "lessons": [{"title": "useState & useEffect", "duration_minutes": 35}, {"title": "Custom Hooks", "duration_minutes": 30}]},
                ],
            },
            {
                "title": "Node.js & Express — Scalable Backend",
                "category": "Web Development",
                "instructor": instructors[3],
                "short_description": "Build high-performance REST APIs and microservices with Node.js, Express, and MongoDB.",
                "description": "Full backend engineering with Node.js. Learn async patterns, stream processing, Express middleware, MongoDB with Mongoose, Redis caching, and Docker containerisation.",
                "level": "advanced",
                "price": 89.99,
                "discount_price": 34.99,
                "duration_hours": 32,
                "is_featured": False,
                "students_count": 15600,
                "what_you_will_learn": ["Node.js async/await & streams", "RESTful API design", "MongoDB & Mongoose", "Redis caching", "Docker & deployment"],
                "requirements": ["JavaScript proficiency", "Basic understanding of HTTP"],
                "modules": [
                    {"title": "Express Fundamentals", "lessons": [{"title": "Routing & Middleware", "duration_minutes": 40, "is_preview": True}, {"title": "Error Handling", "duration_minutes": 25}]},
                ],
            },
            {
                "title": "UI/UX Design Masterclass",
                "category": "UI/UX Design",
                "instructor": instructors[4],
                "short_description": "Design beautiful, user-centred products using Figma, design systems, and UX research.",
                "description": "A complete design course from wireframing to high-fidelity prototypes. Learn Figma workflows, typography, colour theory, accessibility, and how to hand off designs to developers.",
                "level": "beginner",
                "price": 59.99,
                "discount_price": 24.99,
                "duration_hours": 20,
                "is_featured": False,
                "students_count": 22100,
                "what_you_will_learn": ["Figma from scratch", "Design systems", "UX research methods", "Accessibility best practices", "Prototyping & handoff"],
                "requirements": ["No design experience needed"],
                "modules": [
                    {"title": "Figma Basics", "lessons": [{"title": "The Figma Interface", "duration_minutes": 20, "is_preview": True}, {"title": "Frames & Components", "duration_minutes": 30}]},
                ],
            },
        ]

        for data in courses_data:
            modules_data = data.pop("modules", [])
            cat_name = data.pop("category")
            data["category"] = categories[cat_name]
            course, created = Course.objects.get_or_create(title=data["title"], defaults=data)
            if created:
                for order, mod_data in enumerate(modules_data):
                    lessons_data = mod_data.pop("lessons", [])
                    module = Module.objects.create(course=course, order=order, **mod_data)
                    for l_order, lesson_data in enumerate(lessons_data):
                        Lesson.objects.create(module=module, order=l_order, **lesson_data)
            else:
                # Restore data dict keys for next iteration (not strictly needed but safe)
                pass

        self.stdout.write(f"  ✓ {len(courses_data)} courses")

        # Blog posts
        posts_data = [
            {
                "title": "10 Python Libraries Every Developer Should Know in 2025",
                "excerpt": "Discover the most powerful Python libraries that will supercharge your development workflow.",
                "content": """Python's ecosystem is one of the richest in any programming language. Here are 10 libraries that every developer should have in their toolkit in 2025.

1. **Pydantic** — Data validation using Python type hints. Essential for building robust APIs.

2. **FastAPI** — A modern, fast web framework for building APIs with automatic docs.

3. **Polars** — A blazingly fast DataFrame library written in Rust, the spiritual successor to Pandas.

4. **Ruff** — An extremely fast Python linter and formatter, written in Rust.

5. **httpx** — A fully featured HTTP client with async support — modern replacement for requests.

6. **SQLModel** — Combines SQLAlchemy and Pydantic for clean database models.

7. **Typer** — Build CLI applications with Python type hints.

8. **Rich** — Beautiful terminal output: tables, progress bars, syntax highlighting.

9. **Celery** — Distributed task queues for background jobs.

10. **Pytest** — The gold-standard testing framework for Python.""",
                "author": admin,
                "tags": ["Python", "Tutorial"],
            },
            {
                "title": "The Complete Guide to React Query in 2025",
                "excerpt": "Master data fetching, caching, and synchronisation with React Query and learn why it replaces Redux for most use cases.",
                "content": """React Query (now TanStack Query) has become the de facto standard for server state management in React applications.

**Why React Query?**

Traditional state management with Redux or Context API conflates client state and server state. React Query separates these concerns cleanly.

**Key Concepts:**
- **Queries** — Fetching data that is read-only
- **Mutations** — Creating, updating, or deleting data
- **Invalidation** — Automatically refetch stale data

**Basic Example:**

```javascript
const { data, isLoading, error } = useQuery({
  queryKey: ['courses'],
  queryFn: () => api.get('/api/courses/').then(r => r.data),
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

React Query handles loading states, error states, caching, background refetching, and pagination out of the box.""",
                "author": admin,
                "tags": ["React", "JavaScript"],
            },
            {
                "title": "Django to Production: A Complete Deployment Guide",
                "excerpt": "A step-by-step guide to deploying Django applications on Render with PostgreSQL, WhiteNoise, and custom domains.",
                "content": """Deploying Django can feel daunting, but with the right setup it's straightforward. This guide covers everything from environment variables to SSL certificates.

**Step 1: Prepare Your Settings**

Use python-decouple or django-environ to separate config from code. Never commit secrets.

**Step 2: Configure Database**

Use dj-database-url to parse the DATABASE_URL environment variable:

```python
DATABASES = {"default": dj_database_url.config(default=os.environ["DATABASE_URL"])}
```

**Step 3: Static Files**

Add WhiteNoise for serving static files without S3:

```python
MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware", ...]
```

**Step 4: Create render.yaml**

Render's deploy configuration file makes deployments declarative and reproducible.

**Step 5: Run Migrations on Deploy**

Add to your build command:

```bash
python manage.py migrate && python manage.py collectstatic --noinput
```""",
                "author": admin,
                "tags": ["Python", "Web Dev", "Career"],
            },
        ]

        for data in posts_data:
            tag_names = data.pop("tags", [])
            post, created = Post.objects.get_or_create(title=data["title"], defaults=data)
            if created:
                for tag_name in tag_names:
                    if tag_name in tags:
                        post.tags.add(tags[tag_name])

        self.stdout.write(f"  ✓ {len(posts_data)} blog posts")
        self.stdout.write(self.style.SUCCESS("\n✅  Seeding complete!"))
        self.stdout.write("  Admin login:  admin@mentorbyte.com  /  Admin@1234")
