import os
import platform
import subprocess
import sys

def get_paths():
    """Calculates absolute paths based on script location"""
    # Assume this script is in /root/scripts/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level, then down into challenges/01-binary-pwn
    challenge_dir = os.path.abspath(os.path.join(script_dir, "..", "challenges", "01-binary-pwn"))
    
    return challenge_dir

def check_compiler(system_os):
    """Checks if GCC is installed"""
    check_cmd = ["where", "gcc"] if system_os == "Windows" else ["which", "gcc"]
    try:
        subprocess.check_call(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def compile_binary(source_path, output_path, system_os):
    """Compiles a single C file"""
    compiler = "gcc"
    
    if system_os == "Windows":
        # Windows Flags (MinGW)
        flags = [
            "-o", output_path,
            "-fno-stack-protector",       # Disable Canary
            "-Wno-deprecated-declarations", # Hide 'gets' warning
            "-static"                     # Bundle libraries (portability)
        ]
    else:
        # Linux Flags
        flags = [
            "-o", output_path,
            "-fno-stack-protector",
            "-z", "execstack",            # Allow stack execution
            "-no-pie",                    # Disable ASLR for binary text segment
            "-Wno-deprecated-declarations"
        ]

    cmd = [compiler, source_path] + flags
    
    try:
        subprocess.check_call(cmd)
        print(f"    [+] Success: {os.path.basename(output_path)} created.")
        return True
    except subprocess.CalledProcessError:
        print(f"    [!] Failed to compile {os.path.basename(source_path)}")
        return False

def build_project():
    print("==============================================")
    print("     CYBER ARENA - PYTHON BUILD SYSTEM        ")
    print("==============================================")

    system_os = platform.system()
    challenge_dir = get_paths()
    print(f"[*] Detected OS: {system_os}")
    print(f"[*] Challenge Dir: {challenge_dir}")

    # 1. Check Dependencies
    if not check_compiler(system_os):
        print("[!] Error: GCC compiler not found.")
        print("    Windows: Install MinGW/w64devkit.")
        print("    Linux: sudo apt install build-essential")
        sys.exit(1)

    # PHASE 1: VULNERABLE BINARY
    print("\n[1/3] Building Vulnerable Binary (vault.c)...")
    src_vuln = os.path.join(challenge_dir, "vault.c")
    out_vuln = os.path.join(challenge_dir, "vault.exe" if system_os == "Windows" else "vault")
    
    if os.path.exists(src_vuln):
        compile_binary(src_vuln, out_vuln, system_os)
    else:
        print(f"    [!] Error: Source file not found: {src_vuln}")

    # PHASE 2: PATCHED BINARY
    print("\n[2/3] Building Patched Binary (vault_patched.c)...")
    src_patch = os.path.join(challenge_dir, "vault_patched.c")
    out_patch = os.path.join(challenge_dir, "vault_patched.exe" if system_os == "Windows" else "vault_patched")
    
    if os.path.exists(src_patch):
        compile_binary(src_patch, out_patch, system_os)
    else:
        print("    [-] Skip: vault_patched.c not found.")

    # PHASE 3: WEB DEPENDENCIES
    print("\n[3/3] Installing Python Web Dependencies...")
    try:
        # Use sys.executable to ensure we use the same python running this script
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests", "--quiet"])
        print("    [+] Success: Flask and Requests installed.")
    except subprocess.CalledProcessError:
        print("    [!] Warning: Could not install Python libraries.")

    print("\n==============================================")
    print("       BUILD COMPLETE - READY TO PLAY         ")
    print("==============================================")

    # PHASE 4: CRYPTO CHALLENGE
    print("\n[4/4] Generating Crypto Artifacts...")
    crypto_dir = os.path.join(os.path.dirname(challenge_dir), "03-crypto-crack")
    crypto_script = os.path.join(crypto_dir, "secure_vault.py")
    
    if os.path.exists(crypto_script):
        try:
            # Run the script with --setup to create the .enc file
            subprocess.check_call([sys.executable, crypto_script, "--setup"], cwd=crypto_dir)
            print("    [+] Success: flag.enc generated.")
        except subprocess.CalledProcessError:
            print("    [!] Failed to generate crypto files.")
    else:
        print(f"    [-] Skip: {crypto_script} not found.")

if __name__ == "__main__":
    build_project()
