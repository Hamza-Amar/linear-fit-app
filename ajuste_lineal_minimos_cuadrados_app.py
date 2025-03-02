import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.optimize import curve_fit

def linear_model(x, m, b):
    return m * x + b

def linear_fit(x, y, y_err):
    popt, pcov = curve_fit(linear_model, x, y, sigma=y_err, absolute_sigma=True)
    slope, intercept = popt
    slope_err, intercept_err = np.sqrt(np.diag(pcov))
    r_value = np.corrcoef(x, y)[0, 1]
    return slope, intercept, slope_err, intercept_err, r_value

def plot_linear_fit(x, y, x_err, y_err, slope, intercept, slope_err, intercept_err, r_value, slope_res, intercept_res, x_label="Eje X", y_label="Eje Y", title="Ajuste lineal con barras de error"):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', color='darkblue', ecolor='gray', elinewidth=1, capsize=3, label='Datos')
    
    x_fit = np.linspace(min(x) - 1, max(x) + 1, 100)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, color='crimson', linewidth=2, linestyle='-', label=f'Fit: $y={slope:.{slope_res}f}x + {intercept:.{intercept_res}f}$')
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)
    
    textstr = f"$r = {r_value:.2f}$\n$\sigma(A) = {slope_err:.{slope_res}f}$\n$\sigma(B) = {intercept_err:.{intercept_res}f}$"
    ax.annotate(textstr, xy=(0.05, 0.75), xycoords='axes fraction', fontsize=12, color='black', bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'))
    
    st.pyplot(fig)

if __name__ == "__main__":
    st.markdown("<h1>Laboratorio de Física II<br>Regresión lineal con errores<br>Método de mínimos cuadrados</h1>", unsafe_allow_html=True)
     
    st.write("¡Ingrese sus datos, errores y vea la línea ajustada!")
    
    x_values = st.text_area("Introduzca los valores de X (separados por comas)", "1, 2, 3, 4, 5")
    y_values = st.text_area("Introduzca los valores de Y (separados por comas)", "2.1, 2.9, 3.8, 5.1, 5.9")
    x_errors = st.text_area("Introduzca los valores de los errores de X (separados por comas)", "0.1, 0.2, 0.1, 0.3, 0.2")
    y_errors = st.text_area("Introduzca los valores de los errores de Y (separados por comas)", "0.2, 0.2, 0.3, 0.2, 0.3")
    slope_res = st.number_input("Número de decimales para la pendiente", 0, 10, 1)
    intercept_res = st.number_input("Número de decimales para la ordenada al origen", 0, 10, 1)
    x_label = st.text_input("Etiqueta del eje X", "m (g)")
    y_label = st.text_input("Etiqueta del eje Y", "$\Delta y$ (cm)")
    
    if st.button("Calcular ajuste"):
        x = np.array([float(i) for i in x_values.split(',')])
        y = np.array([float(i) for i in y_values.split(',')])
        x_err = np.array([float(i) for i in x_errors.split(',')])
        y_err = np.array([float(i) for i in y_errors.split(',')])
        
        slope, intercept, slope_err, intercept_err, r_value = linear_fit(x, y, y_err)
        plot_linear_fit(x, y, x_err, y_err, slope, intercept, slope_err, intercept_err, r_value, slope_res, intercept_res, x_label, y_label)
