#!/bin/bash
python -m api.main > backend.log 2>&1 &
cd frontend
npm run dev > ../frontend.log 2>&1 &
