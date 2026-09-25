# Predictive Maintenance Backend API

FastAPI backend for the predictive maintenance system with RUL prediction and maintenance decision support.

## Features

- **Health Check**: API and database status monitoring
- **Machine CRUD**: Create, read, update, delete machines
- **Sensor Reading Storage**: Store sensor data for machines
- **RUL Prediction**: Real-time RUL prediction using trained ML model
- **Prediction History**: Track prediction history over time
- **Maintenance Status**: Get current maintenance status and recommendations
- **PostgreSQL Persistence**: All data stored in PostgreSQL database

## Technology Stack

- **Python 3.8+**
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Joblib** - ML model loading

## Project Structure

`
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy models
│   │   └── __init__.py      # Machine, SensorReading, Prediction
│   ├── schemas/             # Pydantic schemas
│   │   └── __init__.py      # Request/response models
│   ├── routes/              # API endpoints
│   │   ├── health.py        # Health check
│   │   ├── machines.py      # Machine CRUD
│   │   ├── sensor_readings.py # Sensor reading storage
│   │   ├── predictions.py   # RUL predictions
│   │   └── maintenance.py   # Maintenance status
│   └── services/            # Business logic
│       └── prediction_service.py # ML model integration
├── tests/                   # Unit tests
│   └── test_api.py
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
`

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **PostgreSQL 12 or higher**
3. **pip** (Python package manager)

### Setup Steps

1. **Clone the repository** (if not already done)
   `ash
   cd PFA26/backend
   `

2. **Create virtual environment**
   `ash
   python -m venv venv
   `

3. **Activate virtual environment**
   
   Windows:
   `ash
   venv\\Scripts\\activate
   `
   
   Linux/Mac:
   `ash
   source venv/bin/activate
   `

4. **Install dependencies**
   `ash
   pip install -r requirements.txt
   `

5. **Configure environment variables**
   `ash
   copy .env.example .env
   `
   
   Edit .env and set your database credentials:
   `
   DATABASE_URL=postgresql://username:password@localhost:5432/predictive_maintenance
   `

## Database Setup

### Using PostgreSQL (Local)

1. **Install PostgreSQL** if not already installed
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: rew install postgresql
   - Linux: sudo apt-get install postgresql postgresql-contrib

2. **Start PostgreSQL service**
   
   Windows:
   `ash
   # Start PostgreSQL service
   net start postgresql-x64-14  # or your version
   `
   
   Mac:
   `ash
   brew services start postgresql
   `
   
   Linux:
   `ash
   sudo systemctl start postgresql
   `

3. **Create database**
   `ash
   # Connect to PostgreSQL
   psql -U postgres
   
   # In psql:
   CREATE DATABASE predictive_maintenance;
   \\q
   `

4. **Verify connection**
   `ash
   psql -U postgres -d predictive_maintenance
   `

### Using Docker (Optional)

`ash
docker run --name postgres-pm -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=predictive_maintenance -p 5432:5432 -d postgres:14
`

## Running the Application

### Development Mode

`ash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

### Production Mode

`ash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
`

## API Documentation

Once the server is running, access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

**GET** /api/v1/health

Returns API health status, database connection, and model loading status.

### Machines

- **POST** /api/v1/machines/ - Create a new machine
- **GET** /api/v1/machines/ - Get all machines (with pagination)
- **GET** /api/v1/machines/{machine_id} - Get specific machine
- **PUT** /api/v1/machines/{machine_id} - Update machine
- **DELETE** /api/v1/machines/{machine_id} - Delete machine

### Sensor Readings

- **POST** /api/v1/sensor-readings/ - Store sensor reading
- **GET** /api/v1/sensor-readings/ - Get sensor readings (with filters)
- **GET** /api/v1/sensor-readings/{reading_id} - Get specific reading

### Predictions

- **POST** /api/v1/predictions/ - Create RUL prediction
- **GET** /api/v1/predictions/ - Get prediction history
- **GET** /api/v1/predictions/{prediction_id} - Get specific prediction

### Maintenance

- **GET** /api/v1/maintenance/status/{machine_id} - Get maintenance status for machine
- **GET** /api/v1/maintenance/summary - Get maintenance summary across all machines

## Example Usage

### Create a Machine

`ash
curl -X POST "http://localhost:8000/api/v1/machines/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Turbine-001",
    "description": "Main turbine unit",
    "location": "Plant A"
  }'
`

### Create a Prediction

`ash
curl -X POST "http://localhost:8000/api/v1/predictions/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "machine_id": 1,
    "cycle": 100,
    "setting_1": 0.0,
    "setting_2": 0.0,
    "setting_3": 100.0,
    "sensor_2": 518.67,
    "sensor_3": 641.82,
    "sensor_4": 1589.24,
    "sensor_6": 14.62,
    "sensor_7": 21.61,
    "sensor_8": 550.69,
    "sensor_9": 2388.06,
    "sensor_11": 47.54,
    "sensor_12": 521.61,
    "sensor_13": 2388.02,
    "sensor_14": 8142.44,
    "sensor_15": 8.31,
    "sensor_17": 391.00,
    "sensor_20": 39.14,
    "sensor_21": 23.29
  }'
`

### Get Maintenance Status

`ash
curl "http://localhost:8000/api/v1/maintenance/status/1"
`

## Running Tests

`ash
# From backend directory
pytest tests/
`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:password@localhost:5432/predictive_maintenance |
| APP_NAME | Application name | Predictive Maintenance API |
| APP_VERSION | Application version | 1.0.0 |
| DEBUG | Debug mode | False |
| MODEL_PATH | Path to ML model | ../models/final_rul_model.joblib |
| SCALER_PATH | Path to scaler | ../models/preprocessing_pipeline.joblib |
| DECISION_CONFIG_PATH | Path to decision layer config | ../ml/results/decision_layer_config.json |
| API_PREFIX | API URL prefix | /api/v1 |

## ML Model Integration

The backend loads the trained ML model from:
- models/final_rul_model.joblib - Random Forest model
- models/preprocessing_pipeline.joblib - Feature scaler
- ml/results/decision_layer_config.json - Decision layer configuration

The model is loaded at startup and used for real-time RUL predictions.

## Troubleshooting

### Database Connection Error

If you get a database connection error:
1. Verify PostgreSQL is running
2. Check DATABASE_URL in .env file
3. Ensure database exists

### Model Loading Error

If the ML model fails to load:
1. Verify model files exist in the correct paths
2. Check file permissions
3. Ensure all ML dependencies are installed

### Port Already in Use

If port 8000 is already in use:
`ash
# Use a different port
uvicorn app.main:app --port 8001
`

## Security Notes

- **Do not commit .env file** to version control
- **Change default database credentials** in production
- **Configure CORS appropriately** for production
- **Use HTTPS** in production
- **Implement authentication** for production use

## Next Steps

- Add authentication/authorization
- Implement rate limiting
- Add logging and monitoring
- Set up CI/CD pipeline
- Deploy to production server
- Add more comprehensive tests

## License

This is part of the PFA26 Final Academic Project.
