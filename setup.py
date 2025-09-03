#!/usr/bin/env python3
"""
Setup script for Campus Ecosystem
This script helps set up the initial project structure and dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and handle errors."""
    try:
        # For Unix-like systems, command can be a string. For Windows, it's safer as a list.
        cmd_list = command if isinstance(command, list) else command.split()
        result = subprocess.run(
            cmd_list, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=check
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd_list)}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: Command '{cmd_list[0]}' not found. Is it installed and in your PATH?")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8 or higher is required. You are using {sys.version}.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected.")
    return True

def check_node_version():
    """Check if Node.js is installed and version is compatible."""
    print("Checking Node.js version...")
    if not run_command("node --version"):
        print("❌ Node.js is not installed or not in PATH.")
        print("Please install Node.js 16 or higher from https://nodejs.org/")
        return False
    print("✅ Node.js version is compatible.")
    return True

def create_virtual_environment():
    """Create Python virtual environment."""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists.")
        return True
    
    print("Creating Python virtual environment...")
    if not run_command(f"{sys.executable} -m venv venv"):
        print("❌ Failed to create virtual environment.")
        return False
    print("✅ Virtual environment created successfully.")
    return True

def install_python_dependencies():
    """Install Python dependencies from requirements.txt."""
    print("Installing Python dependencies...")
    pip_cmd = os.path.join("venv", "Scripts", "pip") if os.name == 'nt' else os.path.join("venv", "bin", "pip")
    
    if not run_command([pip_cmd, "install", "-r", "requirements.txt"]):
        print("❌ Failed to install Python dependencies.")
        return False
    print("✅ Python dependencies installed successfully.")
    return True

def install_node_dependencies():
    """Install Node.js dependencies from package.json."""
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd="frontend"):
        print("❌ Failed to install Node.js dependencies.")
        return False
    print("✅ Node.js dependencies installed successfully.")
    return True

def create_env_file():
    """Create .env file from the .env.example template."""
    env_file = Path("backend/.env")
    env_example = Path("backend/.env.example")
    
    if env_file.exists():
        print("✅ .env file already exists.")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ .env file created from template.")
        print("⚠️  IMPORTANT: You must now update the 'backend/.env' file with your actual configuration.")
        return True
    else:
        print("❌ 'backend/.env.example' not found. Cannot create .env file.")
        return False

def main():
    """Main setup function."""
    print("🚀 Campus Ecosystem Setup")
    print("=" * 50)
    
    # Prerequisite checks
    if not all([check_python_version(), check_node_version()]):
        return

    # Project setup
    print("\n📁 Setting up project structure...")
    if not create_virtual_environment(): return
    if not install_python_dependencies(): return
    if not install_node_dependencies(): return
    if not create_env_file(): return
    
    # Final instructions
    print("\n🎉 Setup script finished!")
    print("\n📋 Next Steps:")
    print("1. **Configure Environment**: Open `backend/.env` and fill in your details for:")
    print("   - `SECRET_KEY` (a new random string is highly recommended)")
    print("   - `DATABASE_URL` (e.g., postgresql://youruser:yourpassword@localhost/campus_ecosystem)")
    print("   - `GOOGLE_GEMINI_API_KEY`")
    print("   - `REDIS_URL`")
    print("2. **Setup Database**: Make sure PostgreSQL is running, then run:")
    print("   `python backend/manage.py migrate`")
    print("3. **Create Admin User**:")
    print("   `python backend/manage.py createsuperuser`")
    print("4. **Start Servers**: Open two separate terminal windows:")
    print("   - Terminal 1 (Backend): `python backend/manage.py runserver`")
    print("   - Terminal 2 (Frontend): `npm start --prefix frontend`")

    print("\n🌐 The application will be available at:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:8000")
    print("- Admin Panel: http://localhost:8000/admin")

if __name__ == "__main__":
    main()