@echo off
echo Cleaning up git history...
rmdir /s /q .git
echo.
echo Re-initializing repository...
git init
git add .
git commit -m "Final version (Clean)"
git branch -M main
git remote add origin https://github.com/rishicharadva16/AI_Healthcare_Project.git
echo.
echo Pushing project to GitHub (Force)...
git push -u origin main --force
echo.
pause
