@echo off
setlocal

echo ==================================================
echo    HYBRID CLIENT BUILDER [Windows/MinGW]
echo ==================================================

REM --- CONFIGURATION ---
set "RUST_DIR=logic"
set "CPP_DIR=ui"
set "TARGET=x86_64-pc-windows-gnu"
set "OUT_EXE=cyber_term.exe"

REM --- STEP 1: CHECK DEPENDENCIES ---
where g++ >nul 2>nul
if %errorlevel% neq 0 goto :ErrorGCC

where cargo >nul 2>nul
if %errorlevel% neq 0 goto :ErrorRust

REM --- STEP 2: BUILD RUST ---
echo.
echo [1/2] Compiling Rust Logic (GNU Target)...

cd "%RUST_DIR%"
if %errorlevel% neq 0 goto :ErrorPath

REM Build the static library
cargo build --release --target %TARGET% --quiet
if %errorlevel% neq 0 goto :ErrorBuildRust

cd ..
set "RUST_LIB=%RUST_DIR%\target\%TARGET%\release\libcyber_core.a"

REM --- STEP 3: LINK WITH C++ ---
echo.
echo [2/2] Compiling C++ UI and Linking...

REM ADDED -lntdll HERE TO FIX LINKER ERROR
g++ "%CPP_DIR%\main.cpp" -o "%OUT_EXE%" "%RUST_LIB%" -static-libgcc -static-libstdc++ -lws2_32 -luserenv -lbcrypt -ladvapi32 -lntdll

if %errorlevel% neq 0 goto :ErrorLink

REM --- SUCCESS ---
echo.
echo [SUCCESS] Created %OUT_EXE%
echo You can now run: %OUT_EXE%
echo.
pause
exit /b 0

REM --- ERROR HANDLERS ---
:ErrorGCC
echo [!] Error: g++ not found.
pause
exit /b 1

:ErrorRust
echo [!] Error: cargo not found.
pause
exit /b 1

:ErrorPath
echo [!] Error: logic folder not found.
pause
exit /b 1

:ErrorBuildRust
echo [!] Rust build failed.
cd ..
pause
exit /b 1

:ErrorLink
echo [!] Linking failed.
pause
exit /b 1
