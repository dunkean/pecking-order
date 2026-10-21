@echo off
setlocal
cd /d "%~dp0"
cargo run --release -- studio --port 8773
