import sys

P_IDLE = 20.0       # Фоновая мощность в покое (Idle baseline)
P_LOAD_O0 = 46.5    # Мощность под нагрузкой prog_O0 (4.9 GHz)
P_LOAD_O3 = 45.0    # Мощность под нагрузкой prog_O3 (4.8 GHz)

T_O0 = 5.079
T_O3 = 0.915

E_sys_O0 = P_LOAD_O0 * T_O0
E_sys_O3 = P_LOAD_O3 * T_O3

E_prog_O0 = (P_LOAD_O0 - P_IDLE) * T_O0
E_prog_O3 = (P_LOAD_O3 - P_IDLE) * T_O3

report = f"""======================================================================
ENERGY CONSUMPTION REPORT (RAPL / Idle Baseline Subtraction Model)
Methodology: Luis Cruz (2021) - Measuring Energy in Software
Platform: AMD AM5 (ASUS PRIME B650M-R) / Linux WSL2
======================================================================

1. Baseline Parameters:
   - Idle System Power (P_idle)       : {P_IDLE:.2f} W
   - Load Power - prog_O0 (P_load)    : {P_LOAD_O0:.2f} W (Freq: ~4.9 GHz)
   - Load Power - prog_O3 (P_load)    : {P_LOAD_O3:.2f} W (Freq: ~4.8 GHz)

2. Execution Time (Wall-clock):
   - prog_O0                          : {T_O0:.3f} s
   - prog_O3                          : {T_O3:.3f} s
   - Speedup factor                   : {T_O0 / T_O3:.2f}x

3. System Energy Consumption (Point 3.1):
   - Formula: E_sys = P_load * T
   - prog_O0 (System total)           : {E_sys_O0:.2f} Joules
   - prog_O3 (System total)           : {E_sys_O3:.2f} Joules
   - System Energy Saved              : {E_sys_O0 - E_sys_O3:.2f} J ({(1 - E_sys_O3 / E_sys_O0) * 100:.1f}% reduction)

4. Isolated Program Energy Consumption (Point 3.2):
   - Formula: E_prog = (P_load - P_idle) * T
   - prog_O0 (Dynamic process only)   : {E_prog_O0:.2f} Joules
   - prog_O3 (Dynamic process only)   : {E_prog_O3:.2f} Joules
   - Program Energy Saved             : {E_prog_O0 - E_prog_O3:.2f} J ({(1 - E_prog_O3 / E_prog_O0) * 100:.1f}% reduction)
======================================================================
"""

print(report)
with open("logs/energy_report.txt", "w") as f:
    f.write(report)
