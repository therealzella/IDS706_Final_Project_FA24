.PHONY: install run-backend run-frontend test clean

install:
	cd backend_service && make install
	cd frontend_service && make install

run-backend:
	cd backend_service && make run &
	@echo "Backend server started in background..."
	@sleep 3

run-frontend:
	cd frontend_service && make run

run: run-backend run-frontend

clean:
	@echo "Cleaning up processes..."
	-pkill -f "uvicorn"
	-pkill -f "streamlit"
	cd backend_service && make clean
	cd frontend_service && make clean
	@echo "Cleanup complete"