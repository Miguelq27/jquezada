import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, diff, integrate, latex, sympify, plot
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Cálculo",
    page_icon="📐",
    layout="wide"
)

# Título principal
st.title("📐 Calculadora de Integrales y Derivadas")
st.markdown("---")

# Sidebar para seleccionar operación
st.sidebar.header("Seleccionar Operación")
operation = st.sidebar.selectbox(
    "¿Qué deseas calcular?",
    ["Derivadas", "Integrales", "Ambas"]
)

# Variable simbólica
x = symbols('x')

# Función para mostrar LaTeX
def display_latex(expr):
    return f"$${latex(expr)}$$"

# Función para graficar
def plot_function(expr, title, x_range=(-5, 5)):
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        
        # Convertir expresión simbólica a función numpy
        func = sp.lambdify(x, expr, 'numpy')
        y_vals = func(x_vals)
        
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'${latex(expr)}$')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(title)
        ax.legend()
        
        return fig
    except Exception as e:
        st.error(f"Error al graficar: {str(e)}")
        return None

# Función principal
def main():
    # Entrada de función
    st.header("Entrada de Función")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        function_input = st.text_input(
            "Introduce la función f(x):",
            value="x**2 + 2*x + 1",
            help="Ejemplos: x**2, sin(x), exp(x), log(x), x**3 + 2*x - 1"
        )
    
    with col2:
        calculate_button = st.button("Calcular", type="primary")
    
    # Ejemplos de funciones
    with st.expander("📝 Ejemplos de funciones"):
        st.write("• **Polinomios**: x**2, x**3 + 2*x - 1, 3*x**4 - 2*x**2 + 5")
        st.write("• **Trigonométricas**: sin(x), cos(x), tan(x)")
        st.write("• **Exponenciales**: exp(x), 2**x")
        st.write("• **Logarítmicas**: log(x), ln(x)")
        st.write("• **Raíces**: sqrt(x), x**(1/2)")
        st.write("• **Complejas**: x**2 * sin(x), exp(x) * cos(x)")
    
    if calculate_button or function_input:
        try:
            # Parsear la función
            function_expr = sympify(function_input)
            
            # Mostrar función original
            st.subheader("Función Original")
            st.latex(f"f(x) = {latex(function_expr)}")
            
            # Crear columnas para organizar resultados
            if operation == "Derivadas":
                show_derivatives(function_expr)
            elif operation == "Integrales":
                show_integrals(function_expr)
            else:  # Ambas
                col1, col2 = st.columns(2)
                with col1:
                    show_derivatives(function_expr)
                with col2:
                    show_integrals(function_expr)
            
            # Gráfica de la función original
            st.subheader("📊 Gráfica de la Función")
            fig = plot_function(function_expr, f"Gráfica de f(x) = {latex(function_expr)}")
            if fig:
                st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error al procesar la función: {str(e)}")
            st.info("Verifica que la sintaxis sea correcta. Usa ** para potencias y funciones como sin, cos, exp, log.")

def show_derivatives(function_expr):
    st.subheader("🔄 Derivadas")
    
    # Primera derivada
    first_derivative = diff(function_expr, x)
    st.write("**Primera derivada:**")
    st.latex(f"f'(x) = {latex(first_derivative)}")
    
    # Segunda derivada
    second_derivative = diff(function_expr, x, 2)
    st.write("**Segunda derivada:**")
    st.latex(f"f''(x) = {latex(second_derivative)}")
    
    # Tercera derivada
    third_derivative = diff(function_expr, x, 3)
    st.write("**Tercera derivada:**")
    st.latex(f"f'''(x) = {latex(third_derivative)}")
    
    # Derivada de orden n
    st.write("**Derivada de orden personalizado:**")
    order = st.number_input("Orden de la derivada:", min_value=1, max_value=10, value=1)
    nth_derivative = diff(function_expr, x, order)
    st.latex(f"f^{{({order})}}(x) = {latex(nth_derivative)}")
    
    # Gráficas de derivadas
    with st.expander("📈 Gráficas de Derivadas"):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Función y sus Derivadas", fontsize=16)
        
        x_vals = np.linspace(-5, 5, 1000)
        
        # Función original
        try:
            func = sp.lambdify(x, function_expr, 'numpy')
            y_vals = func(x_vals)
            axes[0,0].plot(x_vals, y_vals, 'b-', linewidth=2)
            axes[0,0].set_title(f'f(x) = ${latex(function_expr)}$')
            axes[0,0].grid(True, alpha=0.3)
        except:
            axes[0,0].text(0.5, 0.5, 'Error al graficar', ha='center', va='center')
        
        # Primera derivada
        try:
            func1 = sp.lambdify(x, first_derivative, 'numpy')
            y1_vals = func1(x_vals)
            axes[0,1].plot(x_vals, y1_vals, 'r-', linewidth=2)
            axes[0,1].set_title(f"f'(x) = ${latex(first_derivative)}$")
            axes[0,1].grid(True, alpha=0.3)
        except:
            axes[0,1].text(0.5, 0.5, 'Error al graficar', ha='center', va='center')
        
        # Segunda derivada
        try:
            func2 = sp.lambdify(x, second_derivative, 'numpy')
            y2_vals = func2(x_vals)
            axes[1,0].plot(x_vals, y2_vals, 'g-', linewidth=2)
            axes[1,0].set_title(f"f''(x) = ${latex(second_derivative)}$")
            axes[1,0].grid(True, alpha=0.3)
        except:
            axes[1,0].text(0.5, 0.5, 'Error al graficar', ha='center', va='center')
        
        # Tercera derivada
        try:
            func3 = sp.lambdify(x, third_derivative, 'numpy')
            y3_vals = func3(x_vals)
            axes[1,1].plot(x_vals, y3_vals, 'm-', linewidth=2)
            axes[1,1].set_title(f"f'''(x) = ${latex(third_derivative)}$")
            axes[1,1].grid(True, alpha=0.3)
        except:
            axes[1,1].text(0.5, 0.5, 'Error al graficar', ha='center', va='center')
        
        plt.tight_layout()
        st.pyplot(fig)

def show_integrals(function_expr):
    st.subheader("∫ Integrales")
    
    # Integral indefinida
    indefinite_integral = integrate(function_expr, x)
    st.write("**Integral indefinida:**")
    st.latex(f"\\int f(x) \\, dx = {latex(indefinite_integral)} + C")
    
    # Integral definida
    st.write("**Integral definida:**")
    col1, col2 = st.columns(2)
    with col1:
        lower_limit = st.number_input("Límite inferior:", value=0.0)
    with col2:
        upper_limit = st.number_input("Límite superior:", value=1.0)
    
    try:
        definite_integral = integrate(function_expr, (x, lower_limit, upper_limit))
        st.latex(f"\\int_{{{lower_limit}}}^{{{upper_limit}}} f(x) \\, dx = {latex(definite_integral)}")
        
        # Valor numérico
        numerical_value = float(definite_integral.evalf())
        st.write(f"**Valor numérico:** {numerical_value:.6f}")
        
    except Exception as e:
        st.error(f"Error al calcular la integral definida: {str(e)}")
    
    # Gráfica del área bajo la curva
    with st.expander("📊 Visualización del Área Bajo la Curva"):
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Rango para graficar
            x_plot = np.linspace(lower_limit - 1, upper_limit + 1, 1000)
            func = sp.lambdify(x, function_expr, 'numpy')
            y_plot = func(x_plot)
            
            # Graficar función
            ax.plot(x_plot, y_plot, 'b-', linewidth=2, label=f'f(x) = ${latex(function_expr)}$')
            
            # Área bajo la curva
            x_fill = np.linspace(lower_limit, upper_limit, 100)
            y_fill = func(x_fill)
            ax.fill_between(x_fill, 0, y_fill, alpha=0.3, color='lightblue', 
                           label=f'Área = {numerical_value:.3f}')
            
            # Líneas verticales en los límites
            ax.axvline(x=lower_limit, color='red', linestyle='--', alpha=0.7)
            ax.axvline(x=upper_limit, color='red', linestyle='--', alpha=0.7)
            
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Área bajo la curva desde x = {lower_limit} hasta x = {upper_limit}')
            ax.legend()
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error al crear la gráfica: {str(e)}")

# Información adicional en el sidebar
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Información")
st.sidebar.write("Esta aplicación utiliza SymPy para cálculos simbólicos.")
st.sidebar.write("Puedes introducir funciones matemáticas usando sintaxis de Python.")

st.sidebar.markdown("---")
st.sidebar.header("🔗 Funciones Disponibles")
st.sidebar.write("• **Básicas**: +, -, *, /, **")
st.sidebar.write("• **Trigonométricas**: sin, cos, tan")
st.sidebar.write("• **Exponenciales**: exp, **")
st.sidebar.write("• **Logarítmicas**: log, ln")
st.sidebar.write("• **Raíces**: sqrt")
st.sidebar.write("• **Constantes**: pi, e")

if __name__ == "__main__":
    main() 