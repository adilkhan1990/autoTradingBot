# AuthBot - Trading Bot Platform

A comprehensive trading bot platform with secure authentication and bot management capabilities.

## Phase 1: Project Setup & Architecture ✅

### Backend Features
- **FastAPI** with structured architecture (core, api, auth, bots, db)
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT-based authentication** with secure password hashing
- **RESTful API** with automatic OpenAPI documentation
- **Docker containerization** for easy deployment
- **Environment-based configuration**

### Frontend Features
- **Next.js 15** with App Router
- **TailwindCSS** for styling
- **ShadCN UI** components
- **Redux Toolkit** for state management
- **TypeScript** for type safety
- **Responsive design** with modern UI/UX

## Project Structure

```
authbot/
├── backend/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   └── users.py         # User management endpoints
│   │   └── v1/
│   │       └── api.py           # API router
│   ├── auth/
│   │   └── utils.py             # Authentication utilities
│   ├── core/
│   │   └── config.py            # Configuration settings
│   ├── db/
│   │   ├── models/
│   │   │   └── user.py          # User database model
│   │   ├── base.py              # Database configuration
│   │   └── init_db.py           # Database initialization
│   ├── schemas/
│   │   └── user.py              # Pydantic schemas
│   ├── main.py                  # FastAPI application entry point
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (public)/
│   │   │   │   ├── login/       # Login page
│   │   │   │   └── signup/      # Signup page
│   │   │   ├── dashboard/       # Protected dashboard
│   │   │   ├── layout.tsx       # Root layout
│   │   │   └── page.tsx         # Landing page
│   │   ├── components/ui/       # ShadCN UI components
│   │   ├── lib/
│   │   │   └── api/
│   │   │       └── client.ts    # API client
│   │   └── store/
│   │       ├── index.ts         # Redux store
│   │       ├── authSlice.ts     # Authentication state
│   │       └── provider.tsx     # Redux provider
│   └── .env.local               # Frontend environment variables
├── docker-compose.yml           # Multi-container setup
├── .env                         # Backend environment variables
└── README.md                    # This file
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd authbot
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**
   - Install PostgreSQL
   - Create a database named `authbot`
   - Update `.env` file with your database credentials

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### Users
- `GET /api/v1/users/` - List users
- `GET /api/v1/users/{id}` - Get user by ID

## Environment Variables

### Backend (.env)
```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=authbot
POSTGRES_PORT=5432
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features Implemented

### ✅ Backend
- [x] FastAPI application structure
- [x] PostgreSQL database integration
- [x] User authentication (JWT)
- [x] Password hashing (bcrypt)
- [x] User registration and login
- [x] CORS configuration
- [x] Environment-based configuration
- [x] Docker containerization
- [x] API documentation (OpenAPI/Swagger)

### ✅ Frontend
- [x] Next.js 15 with App Router
- [x] Landing page with modern design
- [x] Login and signup pages
- [x] Redux state management
- [x] API client integration
- [x] Protected dashboard route
- [x] Responsive design
- [x] TypeScript integration
- [x] ShadCN UI components
- [x] TailwindCSS styling

## Development

### Testing the Application

1. **Start the services** (using Docker or manual setup)

2. **Create a test account**
   - Visit http://localhost:3000
   - Click "Sign Up"
   - Fill out the registration form
   - Complete registration

3. **Log in**
   - Go to login page
   - Enter your credentials
   - You'll be redirected to the dashboard

4. **API Testing**
   - Visit http://localhost:8000/docs for interactive API documentation
   - Test endpoints directly from the Swagger UI

### Database Management

The application automatically creates database tables on startup. For manual database operations:

```bash
# Connect to PostgreSQL (if running locally)
psql -h localhost -U postgres -d authbot

# View tables
\dt

# View users
SELECT * FROM users;
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication with configurable expiration
- **CORS Protection**: Configured for frontend domain
- **Input Validation**: Pydantic schemas for request/response validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## Next Steps (Future Phases)

- [ ] Bot creation and management system
- [ ] Real-time trading bot monitoring
- [ ] Performance analytics and reporting
- [ ] Advanced trading strategies
- [ ] User role management
- [ ] API rate limiting
- [ ] Enhanced security features
- [ ] WebSocket integration for real-time updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
