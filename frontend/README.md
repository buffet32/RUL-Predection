# Predictive Maintenance Frontend

React + TypeScript + Vite frontend for the predictive maintenance system with real-time RUL prediction and maintenance decision support.

## Features

- **Dashboard**: Overview of all machines with statistics and charts
- **Machines**: View and manage all machines with filtering and search
- **Machine Details**: Detailed view of individual machines with prediction history and sensor data
- **Maintenance**: Prioritized maintenance recommendations grouped by urgency

## Technology Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation

## Project Structure

`
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   └── Header.tsx       # Page header
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── Machines.tsx     # Machines list
│   │   ├── MachineDetails.tsx # Machine details
│   │   └── Maintenance.tsx  # Maintenance recommendations
│   ├── services/            # API services
│   │   └── api.ts           # Axios API client
│   ├── types/               # TypeScript types
│   │   └── index.ts         # Type definitions
│   ├── layouts/             # Layout components
│   │   └── Layout.tsx       # Main layout wrapper
│   ├── App.tsx              # Root component with routing
│   └── main.ts              # Application entry point
├── public/                  # Static assets
├── .env                     # Environment variables
├── package.json             # Dependencies
├── tailwind.config.js       # Tailwind configuration
└── README.md               # This file
`

## Installation

### Prerequisites

1. **Node.js 18+** - Download from https://nodejs.org/
2. **npm** - Comes with Node.js
3. **FastAPI Backend** - Must be running on http://localhost:8000

### Setup Steps

1. **Navigate to frontend directory**
   `ash
   cd frontend
   `

2. **Install dependencies**
   `ash
   npm install
   `

3. **Configure environment variables**
   
   The .env file should already exist with:
   `
   VITE_API_URL=http://localhost:8000/api/v1
   `
   
   If the backend is running on a different port or URL, update this value.

## Running the Application

### Development Mode

`ash
npm run dev
`

The frontend will be available at: **http://localhost:5173**

### Production Build

`ash
npm run build
`

The optimized build will be in the dist/ directory.

### Preview Production Build

`ash
npm run preview
`

## Connecting to FastAPI Backend

The frontend communicates with the FastAPI backend via the API URL defined in .env.

### Backend Requirements

The FastAPI backend must be running and accessible at the configured URL.

### Starting the Backend

From the project root:
`ash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

The backend will be available at: **http://localhost:8000**

### API Documentation

Once the backend is running, access the API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Pages

### Dashboard (/)
- Total machines count
- Machines by status (Normal, Monitor, Maintenance, Critical)
- Average health score
- Maintenance status distribution chart
- Status breakdown bar chart
- Recent predictions table

### Machines (/machines)
- Searchable machine list
- Status filter dropdown
- Machine table with latest predictions
- Click to view machine details

### Machine Details (/machines/:id)
- Machine information
- AI Prediction section with:
  - Predicted RUL (Random Forest model output)
  - Effective RUL (after safety margin)
  - Health Score (AI-derived decision-support score)
  - Maintenance Status
- RUL predictions over time chart
- Health score over time chart
- Sensor readings over time chart

### Maintenance (/maintenance)
- Critical machines (immediate attention required)
- Maintenance recommended machines
- Monitor machines (watch closely)
- Color-coded urgency indicators

## API Endpoints Used

The frontend uses the following FastAPI endpoints:

- GET /api/v1/health - Health check
- GET /api/v1/machines/ - Get all machines
- GET /api/v1/machines/{id} - Get specific machine
- POST /api/v1/machines/ - Create machine
- PUT /api/v1/machines/{id} - Update machine
- DELETE /api/v1/machines/{id} - Delete machine
- GET /api/v1/predictions/ - Get predictions
- POST /api/v1/predictions/ - Create prediction
- GET /api/v1/maintenance/status/{machine_id} - Get maintenance status
- GET /api/v1/maintenance/summary - Get maintenance summary

## Error Handling

The frontend implements:
- Loading states during API calls
- Error messages for failed requests
- Empty states when no data is available
- Retry buttons for manual refresh

## Design

The interface is designed as a professional industrial monitoring system with:
- Clean, industrial color scheme
- Sidebar navigation
- Dashboard cards for key metrics
- Data tables with sorting and filtering
- Interactive charts for data visualization
- Responsive design for different screen sizes

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| VITE_API_URL | FastAPI backend URL | http://localhost:8000/api/v1 |

## Troubleshooting

### Backend Connection Error

If the frontend cannot connect to the backend:
1. Verify the backend is running: http://localhost:8000/api/v1/health
2. Check the VITE_API_URL in .env
3. Ensure CORS is enabled on the backend

### Build Errors

If you encounter build errors:
1. Delete 
ode_modules and package-lock.json
2. Run 
pm install again
3. Clear Vite cache: 
pm run dev -- --force

### Tailwind CSS Not Working

If Tailwind styles are not applied:
1. Verify 	ailwind.config.js exists
2. Check that @tailwind directives are in src/style.css
3. Restart the dev server

## Complete System Startup

To run the complete predictive maintenance system:

### Terminal 1 - Start PostgreSQL
`ash
# Windows
net start postgresql-x64-14

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql
`

### Terminal 2 - Start FastAPI Backend
`ash
cd PFA26/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

### Terminal 3 - Start React Frontend
`ash
cd PFA26/frontend
npm run dev
`

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Backend Changes

No backend changes were required for this frontend implementation. All endpoints used already exist in the FastAPI backend created in Phase 3A.

## Next Steps

- Add authentication/authorization
- Implement real-time updates with WebSockets
- Add more detailed analytics
- Implement alert notifications
- Add export functionality for reports
- Optimize for mobile devices
- Add unit tests for components

## License

This is part of the PFA26 Final Academic Project.
