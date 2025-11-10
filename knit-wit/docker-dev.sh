#!/bin/bash
# Docker development environment management script for Knit-Wit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if .env exists
check_env() {
    if [ ! -f .env ]; then
        warn ".env file not found. Creating from .env.example..."
        cp .env.example .env
        success ".env file created. Please review and update values if needed."
    fi
}

# Main commands
case "$1" in
    start)
        info "Starting Docker Compose services..."
        check_env
        docker-compose up
        ;;

    start-d|daemon)
        info "Starting Docker Compose services in detached mode..."
        check_env
        docker-compose up -d
        success "Services started. Use './docker-dev.sh logs' to view logs."
        ;;

    stop)
        info "Stopping Docker Compose services..."
        docker-compose down
        success "Services stopped."
        ;;

    restart)
        info "Restarting Docker Compose services..."
        docker-compose restart
        success "Services restarted."
        ;;

    restart-backend|rb)
        info "Restarting backend service..."
        docker-compose restart backend
        success "Backend service restarted."
        ;;

    logs)
        if [ -z "$2" ]; then
            docker-compose logs -f
        else
            docker-compose logs -f "$2"
        fi
        ;;

    build)
        info "Rebuilding Docker images..."
        docker-compose build
        success "Images rebuilt."
        ;;

    rebuild)
        info "Rebuilding and starting services..."
        docker-compose up --build
        ;;

    reset)
        warn "This will stop all services and remove volumes (data will be lost)."
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Resetting environment..."
            docker-compose down -v
            success "Environment reset."
        else
            info "Reset cancelled."
        fi
        ;;

    clean)
        warn "This will remove all stopped containers, networks, and dangling images."
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            info "Cleaning Docker environment..."
            docker system prune -f
            success "Docker environment cleaned."
        else
            info "Clean cancelled."
        fi
        ;;

    status|ps)
        info "Docker Compose services status:"
        docker-compose ps
        ;;

    health)
        info "Checking service health..."
        echo ""
        echo "Backend health:"
        docker inspect knitwit-backend --format='{{.State.Health.Status}}' 2>/dev/null || echo "Service not running"
        echo ""
        echo "Database health:"
        docker inspect knitwit-db --format='{{.State.Health.Status}}' 2>/dev/null || echo "Service not running"
        ;;

    db|psql)
        info "Connecting to PostgreSQL database..."
        docker-compose exec db psql -U knitwit -d knitwit_dev
        ;;

    pgadmin)
        info "Starting services with pgAdmin..."
        check_env
        docker-compose --profile tools up -d
        success "pgAdmin available at http://localhost:5050"
        success "Email: admin@knitwit.local | Password: admin"
        ;;

    shell|sh)
        if [ "$2" = "db" ]; then
            info "Opening shell in database container..."
            docker-compose exec db sh
        else
            info "Opening shell in backend container..."
            docker-compose exec backend sh
        fi
        ;;

    test)
        info "Running backend tests in Docker..."
        docker-compose exec backend pytest
        ;;

    lint)
        info "Running backend linters in Docker..."
        docker-compose exec backend black app tests
        docker-compose exec backend isort app tests
        docker-compose exec backend ruff app tests
        ;;

    help|--help|-h)
        echo "Knit-Wit Docker Development Environment Manager"
        echo ""
        echo "Usage: ./docker-dev.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start              Start all services (foreground)"
        echo "  start-d, daemon    Start all services (background)"
        echo "  stop               Stop all services"
        echo "  restart            Restart all services"
        echo "  restart-backend,rb Restart only backend service"
        echo "  logs [service]     View logs (all or specific service)"
        echo "  build              Rebuild Docker images"
        echo "  rebuild            Rebuild images and start services"
        echo "  reset              Stop services and remove volumes (data loss!)"
        echo "  clean              Remove stopped containers and dangling images"
        echo "  status, ps         Show service status"
        echo "  health             Check health status of services"
        echo "  db, psql           Connect to PostgreSQL database"
        echo "  pgadmin            Start services with pgAdmin UI"
        echo "  shell [db]         Open shell in backend (or db) container"
        echo "  test               Run backend tests in Docker"
        echo "  lint               Run backend linters in Docker"
        echo "  help               Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./docker-dev.sh start          # Start in foreground"
        echo "  ./docker-dev.sh start-d        # Start in background"
        echo "  ./docker-dev.sh logs backend   # View backend logs"
        echo "  ./docker-dev.sh db             # Connect to database"
        echo ""
        ;;

    *)
        error "Unknown command: $1\n\nUse './docker-dev.sh help' for available commands."
        ;;
esac
