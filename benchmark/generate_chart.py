import os
import sys
import subprocess

# Intentar importar librerías requeridas, instalándolas si es necesario
try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
except ImportError:
    print("[*] Librerías requeridas (matplotlib, pandas, numpy) no encontradas.")
    print("[*] Instalándolas automáticamente usando pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "pandas", "numpy"])
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        print("[+] Librerías instaladas con éxito.")
    except Exception as e:
        print(f"[-] No se pudieron instalar las librerías automáticamente: {e}")
        print("[-] Por favor, instálelas manualmente con: pip install matplotlib pandas numpy")
        sys.exit(1)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    csv_file = "resultados.csv"
    output_png = "grafica_benchmark.png"
    
    if not os.path.exists(csv_file):
        print(f"[-] No se encontró el archivo {csv_file}. Por favor, ejecute primero run_benchmark.py")
        sys.exit(1)
        
    # Leer datos
    df = pd.read_csv(csv_file)
    print("[*] Cargando datos del benchmark...")
    print(df)
    
    # Definir paleta de colores elegantes (Premium Dark/Modern Theme)
    # Python: Steel Blue, JS: Mint/Emerald, Rust: Rust Terracotta, Zig: Warm Amber/Orange
    color_map = {
        "Python": "#3776AB",
        "JavaScript": "#41B883",
        "Rust": "#DE5C46",
        "Zig": "#F7A41D"
    }
    
    colors = [color_map.get(lang, "#888888") for lang in df["Lenguaje"]]
    
    # Configurar estilo estético
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Benchmark Conjetura de Collatz (Rango 1 a 500,000)\nComparativa de Rendimiento y Consumo de Memoria", 
                 fontsize=16, fontweight='bold', color='#1A1A1A', y=0.98)
    
    # --- PANEL 1: Tiempo de Ejecución (Escala Logarítmica para manejar órdenes de magnitud) ---
    bars1 = ax1.bar(df["Lenguaje"], df["Tiempo_ms"], color=colors, edgecolor='#2D2D2D', width=0.55, zorder=3)
    ax1.set_yscale('log')
    ax1.set_title("Tiempo de Ejecución (Escala Logarítmica)", fontsize=13, fontweight='semibold', pad=12)
    ax1.set_ylabel("Tiempo de Ejecución (ms)", fontsize=11, fontweight='semibold')
    ax1.grid(True, which="both", ls="--", alpha=0.5, zorder=0)
    
    # Etiquetas de valor exacto en el tiempo
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{height:,.1f} ms',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 5 puntos de desfase vertical
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#2D2D2D')
        
    # --- PANEL 2: Consumo de Memoria ---
    bars2 = ax2.bar(df["Lenguaje"], df["Memoria_MB"], color=colors, edgecolor='#2D2D2D', width=0.55, zorder=3)
    ax2.set_title("Consumo de Memoria Estructurado (Escala Lineal)", fontsize=13, fontweight='semibold', pad=12)
    ax2.set_ylabel("Memoria Máxima (MB)", fontsize=11, fontweight='semibold')
    ax2.grid(True, ls="--", alpha=0.5, zorder=0)
    
    # Limitar eje Y para darle aire a los textos de las barras
    max_mem = df["Memoria_MB"].max()
    ax2.set_ylim(0, max_mem * 1.15)
    
    # Etiquetas de valor exacto en la memoria
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f} MB',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#2D2D2D')
        
    # Añadir leyenda de tipo de ejecución (Real vs Simulado)
    patches = []
    import matplotlib.patches as mpatches
    for _, row in df.iterrows():
        label = f"{row['Lenguaje']} ({row['Tipo']})"
        patches.append(mpatches.Patch(color=color_map.get(row['Lenguaje']), label=label))
    fig.legend(handles=patches, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.02), fontsize=10.5, frameon=True)
    
    # Limpieza visual
    for ax in [ax1, ax2]:
        ax.tick_params(axis='both', labelsize=10.5)
        # Quitar líneas de marco innecesarias
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)
            
    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    
    # Guardar imagen con alta resolución
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"[+] Gráfica comparativa generada y guardada en: {output_png}")
    plt.close()

if __name__ == "__main__":
    main()
