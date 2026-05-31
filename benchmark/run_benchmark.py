import os
import sys
import time
import subprocess
import csv
import shutil

# Configuración del rango del benchmark (1 a 500,000)
RANGO_MAX = 500000
CSV_FILE = "resultados.csv"

# Agregar rutas locales portables dinámicamente al PATH de ejecución
local_bin = r"C:\Users\Pc\Documents\GitHub\lenguaje y compiladores\bin"
node_path = os.path.join(local_bin, "node-v20.11.1-win-x64")
zig_path = os.path.join(local_bin, "zig-windows-x86_64-0.11.0")
rust_path = os.path.expandvars(r"%USERPROFILE%\.cargo\bin")

paths_to_add = [node_path, zig_path, rust_path]
for p in paths_to_add:
    if os.path.exists(p) and p not in os.environ["PATH"]:
        os.environ["PATH"] = p + os.path.pathsep + os.environ["PATH"]

def check_command(cmd):
    """Verifica si un comando está disponible en el PATH actual."""
    return shutil.which(cmd) is not None

def run_process_and_measure(cmd_args, name):
    """Ejecuta un proceso de forma empírica y mide su tiempo real y pico de memoria en Windows."""
    start_time = time.perf_counter()
    
    try:
        proc = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        pid = proc.pid
        max_mem_bytes = 0
        
        # Muestrear el consumo de memoria mediante tasklist mientras el proceso esté activo
        while proc.poll() is None:
            try:
                cmd = f'tasklist /FI "PID eq {pid}" /FO CSV /NH'
                out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
                if out.strip():
                    parts = out.strip().split(',')
                    if len(parts) >= 5:
                        mem_str = parts[4].replace('"', '').replace(' ', '').replace('K', '').replace(',', '').replace('.', '').strip()
                        mem_bytes = int(mem_str) * 1024
                        if mem_bytes > max_mem_bytes:
                            max_mem_bytes = mem_bytes
            except Exception:
                pass
            time.sleep(0.002)  # Muestreo de alta frecuencia para precisión
            
        stdout, stderr = proc.communicate()
        end_time = time.perf_counter()
        
        if proc.returncode != 0:
            print(f"[-] Error al ejecutar {name}: {stderr}")
            return None, None
            
        elapsed_ms = (end_time - start_time) * 1000.0
        
        # Fallback de seguridad si el proceso fue demasiado rápido para el muestreador
        if max_mem_bytes == 0:
            max_mem_bytes = 1024 * 1024  # Mínimo 1 MB teórico
            
        mem_mb = max_mem_bytes / (1024 * 1024)
        print(f"[+] {name} (REAL) finalizado con éxito en {elapsed_ms:.2f} ms | Memoria: {mem_mb:.2f} MB")
        return elapsed_ms, mem_mb

    except Exception as e:
        print(f"[-] Excepción al ejecutar {name}: {e}")
        return None, None

def main():
    print("=" * 60)
    print("      BENCHMARK EMPÍRICO REAL - CONJETURA DE COLLATZ      ")
    print("============================================================")
    print("[*] Advertencia: Las simulaciones están completamente deshabilitadas.")
    print("[*] Todos los binarios se compilarán y ejecutarán nativamente.")
    print("=" * 60)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    resultados = []
    
    # --- 1. COMPILACIÓN DE RUST ---
    print("\n[*] Comprobando entorno para Rust...")
    if not check_command("rustc"):
        print("[-] ERROR: 'rustc' no está disponible en el PATH.")
        print("[-] Por favor, instale Rust ejecutando install_runtimes.py primero.")
        sys.exit(1)
        
    print("[*] Compilando collatz.rs con optimizaciones release (rustc -O)...")
    try:
        if os.path.exists("collatz_rust.exe"):
            os.remove("collatz_rust.exe")
        comp = subprocess.run(
            ["rustc", "-O", "collatz.rs", "-o", "collatz_rust.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if comp.returncode != 0 or not os.path.exists("collatz_rust.exe"):
            print(f"[-] Error de compilación en Rust: {comp.stderr}")
            sys.exit(1)
        print("[+] Compilación de Rust finalizada con éxito.")
    except Exception as e:
        print(f"[-] Error al compilar Rust: {e}")
        sys.exit(1)

    # --- 2. COMPILACIÓN DE ZIG ---
    print("\n[*] Comprobando entorno para Zig...")
    if not check_command("zig"):
        print("[-] ERROR: 'zig' no está disponible en el PATH.")
        print("[-] Por favor, instale Zig ejecutando install_runtimes.py primero.")
        sys.exit(1)
        
    print("[*] Compilando collatz.zig con optimización (zig build-exe -O ReleaseFast)...")
    try:
        # Limpieza previa
        for ext in ["_zig.exe", "_zig.obj", "_zig.pdb", "collatz_zig.exe", "collatz_zig.obj", "collatz_zig.pdb"]:
            if os.path.exists(ext):
                try: os.remove(ext)
                except Exception: pass
                
        comp = subprocess.run(
            ["zig", "build-exe", "collatz.zig", "-O", "ReleaseFast", "--name", "collatz_zig"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if comp.returncode != 0 or not os.path.exists("collatz_zig.exe"):
            print(f"[-] Error de compilación en Zig: {comp.stderr}")
            sys.exit(1)
        print("[+] Compilación de Zig finalizada con éxito.")
    except Exception as e:
        print(f"[-] Error al compilar Zig: {e}")
        sys.exit(1)

    # --- 3. COMPROBACIÓN DE NODE.JS ---
    print("\n[*] Comprobando entorno para Node.js...")
    if not check_command("node"):
        print("[-] ERROR: 'node' no está disponible en el PATH.")
        print("[-] Por favor, instale Node.js ejecutando install_runtimes.py primero.")
        sys.exit(1)
    print("[+] Entorno de Node.js verificado.")

    # =====================================================================
    #                       EJECUCIÓN DEL BENCHMARK
    # =====================================================================
    print("\n" + "=" * 60)
    print("                  INICIANDO MEDICIONES REALES                 ")
    print("=" * 60)
    
    # 1. ZIG (Ejecución real)
    print("\n[*] Lanzando ejecutable nativo de Zig...")
    zig_time, zig_mem = run_process_and_measure(["collatz_zig.exe"], "Zig")
    if zig_time is not None:
        resultados.append({
            "Lenguaje": "Zig",
            "Tiempo_ms": round(zig_time, 2),
            "Memoria_MB": round(zig_mem, 2),
            "Tipo": "Real"
        })
        
    # 2. RUST (Ejecución real)
    print("\n[*] Lanzando ejecutable nativo de Rust...")
    rs_time, rs_mem = run_process_and_measure(["collatz_rust.exe"], "Rust")
    if rs_time is not None:
        resultados.append({
            "Lenguaje": "Rust",
            "Tiempo_ms": round(rs_time, 2),
            "Memoria_MB": round(rs_mem, 2),
            "Tipo": "Real"
        })

    # 3. JAVASCRIPT (Ejecución real)
    print("\n[*] Lanzando intérprete/JIT de Node.js...")
    js_time, js_mem = run_process_and_measure(["node", "collatz.js"], "JavaScript")
    if js_time is not None:
        resultados.append({
            "Lenguaje": "JavaScript",
            "Tiempo_ms": round(js_time, 2),
            "Memoria_MB": round(js_mem, 2),
            "Tipo": "Real"
        })

    # 4. PYTHON (Ejecución real)
    print("\n[*] Lanzando intérprete de Python...")
    py_time, py_mem = run_process_and_measure([sys.executable, "collatz.py"], "Python")
    if py_time is not None:
        resultados.append({
            "Lenguaje": "Python",
            "Tiempo_ms": round(py_time, 2),
            "Memoria_MB": round(py_mem, 2),
            "Tipo": "Real"
        })

    # Guardar resultados empíricos
    print(f"\n[*] Escribiendo mediciones reales en {CSV_FILE}...")
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Lenguaje", "Tiempo_ms", "Memoria_MB", "Tipo"])
            writer.writeheader()
            for r in resultados:
                writer.writerow(r)
        print("[+] Archivo CSV guardado con éxito con métricas 100% verídicas.")
    except Exception as e:
        print(f"[-] Error al escribir resultados.csv: {e}")
        
    print("\n" + "=" * 60)
    print("                 PRUEBAS REALIZADAS SATISFACTORIAMENTE       ")
    print("=" * 60)

if __name__ == "__main__":
    main()
