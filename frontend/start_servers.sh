#!/bin/bash
python -m api.main > backend.log 2>&1 &
cd /app/frontend && npm run dev > /app/frontend.log 2>&1 &
