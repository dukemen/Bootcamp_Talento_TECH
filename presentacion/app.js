/* =============================================
   PRESENTACION INTERACTIVA - BOOTCAMP TALENTO TECH
   JavaScript principal
   ============================================= */

// =============================================
// ESTADO GLOBAL
// =============================================
let currentSlide = 0;
const totalSlides = 10;
let isTransitioning = false;
let touchStartY = 0;
let touchStartX = 0;

// =============================================
// INICIALIZACION
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    initKeyboardNav();
    initTouchNav();
    initToolsToggle();
    initScrollNav();
    showPipelineDetail(0);
    showCodeStep(0, null);
    updateSlideUI();

    // Ocultar hint del teclado despues de un tiempo
    setTimeout(() => {
        const hint = document.getElementById('keyboardHint');
        if (hint) hint.classList.add('hidden');
    }, 5000);
});

// =============================================
// PARTICULAS ANIMADAS (Portada)
// =============================================
function initParticles() {
    const container = document.getElementById('particles');
    if (!container) return;

    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
        particle.style.animationDelay = (Math.random() * 10) + 's';
        particle.style.width = (Math.random() * 4 + 2) + 'px';
        particle.style.height = particle.style.width;

        const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        container.appendChild(particle);
    }
}

// =============================================
// NAVEGACION POR TECLADO
// =============================================
function initKeyboardNav() {
    document.addEventListener('keydown', (e) => {
        switch (e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
            case 'PageDown':
            case ' ':
                e.preventDefault();
                nextSlide();
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
            case 'PageUp':
                e.preventDefault();
                prevSlide();
                break;
            case 'Home':
                e.preventDefault();
                goToSlide(0);
                break;
            case 'End':
                e.preventDefault();
                goToSlide(totalSlides - 1);
                break;
        }

        // Numeros 0-9 para ir directo a un slide
        const num = parseInt(e.key);
        if (!isNaN(num) && num >= 0 && num <= 9) {
            goToSlide(num);
        }
    });
}

// =============================================
// NAVEGACION TACTIL
// =============================================
function initTouchNav() {
    const container = document.getElementById('slidesContainer');

    container.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
        touchStartX = e.touches[0].clientX;
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const touchEndX = e.changedTouches[0].clientX;
        const diffY = touchStartY - touchEndY;
        const diffX = touchStartX - touchEndX;

        // Requiere un deslizamiento minimo de 50px
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // Deslizamiento horizontal
            if (Math.abs(diffX) > 50) {
                if (diffX > 0) nextSlide();
                else prevSlide();
            }
        } else {
            // Deslizamiento vertical
            if (Math.abs(diffY) > 50) {
                if (diffY > 0) nextSlide();
                else prevSlide();
            }
        }
    }, { passive: true });
}

// =============================================
// NAVEGACION CON RUEDA DEL MOUSE
// =============================================
function initScrollNav() {
    let lastScrollTime = 0;
    const scrollThrottle = 800;

    document.addEventListener('wheel', (e) => {
        e.preventDefault();
        const now = Date.now();
        if (now - lastScrollTime < scrollThrottle) return;
        lastScrollTime = now;

        if (e.deltaY > 0) nextSlide();
        else prevSlide();
    }, { passive: false });
}

// =============================================
// FUNCIONES DE NAVEGACION
// =============================================
function nextSlide() {
    if (isTransitioning || currentSlide >= totalSlides - 1) return;
    goToSlide(currentSlide + 1);
}

function prevSlide() {
    if (isTransitioning || currentSlide <= 0) return;
    goToSlide(currentSlide - 1);
}

function goToSlide(index) {
    if (index < 0 || index >= totalSlides || index === currentSlide || isTransitioning) return;

    isTransitioning = true;
    const slides = document.querySelectorAll('.slide');
    const navItems = document.querySelectorAll('.nav-item');

    // Desactivar slide actual
    slides[currentSlide].classList.remove('active');
    navItems[currentSlide].classList.remove('active');

    // Activar nuevo slide
    currentSlide = index;
    slides[currentSlide].classList.add('active');
    navItems[currentSlide].classList.add('active');

    updateSlideUI();

    // Animar contadores si estamos en el slide de hallazgos
    if (currentSlide === 7) {
        animateCounters();
    }

    // Animar barras si estamos en visualizaciones
    if (currentSlide === 6) {
        animateBars();
    }

    setTimeout(() => {
        isTransitioning = false;
    }, 600);
}

function updateSlideUI() {
    // Actualizar barra de progreso
    const progress = ((currentSlide + 1) / totalSlides) * 100;
    document.getElementById('progressBar').style.width = progress + '%';

    // Actualizar contador
    document.getElementById('currentSlide').textContent = currentSlide + 1;

    // Habilitar/deshabilitar botones
    document.getElementById('prevBtn').disabled = currentSlide === 0;
    document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
}

// =============================================
// NAVEGACION LATERAL - Click en items
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const slideIndex = parseInt(item.dataset.slide);
            goToSlide(slideIndex);
        });
    });

    // Toggle del menu en mobile
    const navToggle = document.getElementById('navToggle');
    const slideNav = document.getElementById('slideNav');
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            slideNav.classList.toggle('open');
        });
    }
});

// =============================================
// HERRAMIENTAS - Toggle de detalles
// =============================================
function initToolsToggle() {
    document.querySelectorAll('.tool-item').forEach(item => {
        item.addEventListener('click', () => {
            // Cerrar otros
            document.querySelectorAll('.tool-item.expanded').forEach(other => {
                if (other !== item) other.classList.remove('expanded');
            });
            item.classList.toggle('expanded');
        });
    });
}

// =============================================
// PIPELINE INTERACTIVO
// =============================================
const pipelineData = [
    {
        title: 'Paso 1: Carga de Datos',
        description: 'Los datos se cargan directamente desde un archivo CSV alojado en GitHub. El dataset contiene 1,000 registros de transacciones de un supermercado con 17 columnas.',
        code: 'url = "https://raw.githubusercontent.com/.../supermarket_sales.csv"\ndf = pd.read_csv(url)\nprint(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")'
    },
    {
        title: 'Paso 2: Exploracion de Datos',
        description: 'Se examinan las primeras y ultimas filas, los tipos de datos de cada columna, y la informacion general del DataFrame para entender la estructura.',
        code: 'df.head()       # Primeras 5 filas\ndf.tail()       # Ultimas 5 filas\ndf.info()       # Tipos y nulos\ndf.describe()   # Estadisticas'
    },
    {
        title: 'Paso 3: Filtrado de Datos',
        description: 'Se seleccionan columnas relevantes (Branch, Product line, Total, Rating) y se filtran las ventas mayores a $300 USD para enfocarse en transacciones significativas.',
        code: 'columnas = ["Branch", "Product line", "Total", "Rating"]\ndf_sel = df[columnas]\ndf_filtrado = df[df["Total"] > 300]'
    },
    {
        title: 'Paso 4: Transformacion',
        description: 'Se crean nuevas columnas calculadas, como el total sin impuestos. Se eliminan columnas innecesarias como gross margin percentage e Invoice ID.',
        code: 'df["Total_sin_impuesto"] = df["Total"] - df["Tax 5%"]\ndf.drop(columns=["gross margin percentage", "Invoice ID"],\n        inplace=True)'
    },
    {
        title: 'Paso 5: Agrupacion y Agregacion',
        description: 'Se agrupan los datos por linea de producto y por sucursal para calcular totales de ventas y obtener el Top 10 de transacciones.',
        code: 'ventas_producto = df.groupby("Product line")["Total"].sum()\nventas_sucursal = df.groupby("Branch")["Total"].sum()\ntop10 = df.nlargest(10, "Total")'
    },
    {
        title: 'Paso 6: Visualizacion',
        description: 'Se generan 5 tipos de graficos profesionales: barras horizontales, lineas temporales, pastel, histogramas con estadisticas y mapa de calor de correlacion.',
        code: 'plt.barh(...)        # Ventas por producto\nplt.plot(...)         # Ventas diarias\nplt.pie(...)          # Metodos de pago\nplt.hist(...)         # Distribucion totales\nsns.heatmap(...)      # Correlaciones'
    }
];

function showPipelineDetail(index) {
    const steps = document.querySelectorAll('.pipeline-step');
    steps.forEach((step, i) => {
        step.classList.toggle('active-step', i === index);
    });

    const detail = document.getElementById('pipelineDetailContent');
    const data = pipelineData[index];
    detail.innerHTML = `
        <h5>${data.title}</h5>
        <p>${data.description}</p>
        <code>${data.code}</code>
    `;
}

// =============================================
// VISUALIZACIONES - Tabs de graficos
// =============================================
function showChart(index, btn) {
    document.querySelectorAll('.chart-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.querySelectorAll('.chart-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById('chart-' + index).classList.add('active');
    if (btn) btn.classList.add('active');

    if (index === 0) animateBars();
}

function animateBars() {
    document.querySelectorAll('.bar').forEach(bar => {
        bar.style.animation = 'none';
        bar.offsetHeight; // trigger reflow
        bar.style.animation = 'growBar 1s ease forwards';
    });
}

// =============================================
// CODIGO EN VIVO - Explorador de codigo
// =============================================
const codeSteps = [
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Importar librerias necesarias</span>
<span class="code-keyword">import</span> pandas <span class="code-keyword">as</span> pd        <span class="code-comment"># Manipulacion de datos</span>
<span class="code-keyword">import</span> numpy <span class="code-keyword">as</span> np         <span class="code-comment"># Computacion numerica</span>
<span class="code-keyword">import</span> matplotlib.pyplot <span class="code-keyword">as</span> plt  <span class="code-comment"># Graficos</span>
<span class="code-keyword">import</span> seaborn <span class="code-keyword">as</span> sns       <span class="code-comment"># Visualizacion estadistica</span>
<span class="code-keyword">from</span> scipy <span class="code-keyword">import</span> stats    <span class="code-comment"># Estadistica avanzada</span>`,
        explanation: 'Se importan las 5 librerias principales: Pandas para datos tabulares, NumPy para calculos, Matplotlib y Seaborn para graficos, y SciPy para estadisticas avanzadas.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Cargar datos desde URL de GitHub</span>
url = <span class="code-string">"https://raw.githubusercontent.com/...</span>
<span class="code-string">       .../supermarket_sales.csv"</span>

df = pd.read_csv(url)

<span class="code-keyword">print</span>(<span class="code-string">f"Filas: </span>{df.shape[0]}<span class="code-string">"</span>)
<span class="code-keyword">print</span>(<span class="code-string">f"Columnas: </span>{df.shape[1]}<span class="code-string">"</span>)`,
        explanation: 'Los datos se cargan directamente desde GitHub usando pd.read_csv(). Esto permite reproducibilidad sin necesidad de descargar archivos manualmente. El dataset tiene 1,000 filas y 17 columnas.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Seleccionar columnas de interes</span>
columnas = [<span class="code-string">"Branch"</span>, <span class="code-string">"Product line"</span>,
            <span class="code-string">"Total"</span>, <span class="code-string">"Rating"</span>]

df_seleccion = df[columnas]

<span class="code-keyword">print</span>(df_seleccion.head())
<span class="code-comment">#   Branch       Product line    Total  Rating</span>
<span class="code-comment"># 0      A  Health and beauty  522.83     9.1</span>
<span class="code-comment"># 1      C  Electronic access  76.40     9.6</span>`,
        explanation: 'Se seleccionan solo las columnas relevantes para el analisis: sucursal, linea de producto, total de venta y calificacion del cliente. Esto reduce el ruido y facilita el trabajo.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Filtrar ventas mayores a $300</span>
df_filtrado = df[df[<span class="code-string">"Total"</span>] > 300]

<span class="code-keyword">print</span>(<span class="code-string">f"Ventas > $300: </span>{len(df_filtrado)}<span class="code-string">"</span>)
<span class="code-keyword">print</span>(<span class="code-string">f"Porcentaje: </span>{len(df_filtrado)/len(df)*100:.1f}%<span class="code-string">"</span>)

<span class="code-comment"># Resultado: ~40% de las ventas superan $300</span>`,
        explanation: 'Se usa filtrado booleano de Pandas para quedarse solo con las transacciones significativas (mayores a $300 USD). Esto permite analizar el comportamiento de los compradores de mayor valor.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Agrupar por linea de producto</span>
ventas_producto = df.groupby(
    <span class="code-string">"Product line"</span>
)[<span class="code-string">"Total"</span>].sum().sort_values(ascending=<span class="code-keyword">False</span>)

<span class="code-comment"># Agrupar por sucursal</span>
ventas_sucursal = df.groupby(
    <span class="code-string">"Branch"</span>
)[<span class="code-string">"Total"</span>].sum()

<span class="code-comment"># Top 10 ventas</span>
top_10 = df.nlargest(10, <span class="code-string">"Total"</span>)`,
        explanation: 'groupby() es una de las operaciones mas poderosas de Pandas. Permite agrupar datos por categoria y calcular estadisticas (suma, promedio, etc.) para cada grupo. nlargest() obtiene los N registros con mayor valor.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Estadisticas descriptivas</span>
media = df[<span class="code-string">"Total"</span>].mean()        <span class="code-comment"># $322.97</span>
mediana = df[<span class="code-string">"Total"</span>].median()    <span class="code-comment"># $312.75</span>
moda = df[<span class="code-string">"Total"</span>].mode()[0]      <span class="code-comment"># $117.19</span>

varianza = df[<span class="code-string">"Total"</span>].var()       <span class="code-comment"># 38,673</span>
desv_std = df[<span class="code-string">"Total"</span>].std()       <span class="code-comment"># $196.65</span>

<span class="code-keyword">print</span>(<span class="code-string">f"Media: $</span>{media:.2f}<span class="code-string">"</span>)`,
        explanation: 'Se calculan medidas de tendencia central (media, mediana, moda) y de dispersion (varianza, desviacion estandar). La diferencia entre media y mediana sugiere una distribucion ligeramente asimetrica.'
    },
    {
        file: 'taller1_supermarket.py',
        code: `<span class="code-comment"># Grafico de barras horizontales</span>
fig, ax = plt.subplots(figsize=(10, 6))
ventas_producto.plot(
    kind=<span class="code-string">"barh"</span>,
    color=<span class="code-string">"skyblue"</span>,
    edgecolor=<span class="code-string">"navy"</span>,
    ax=ax
)
ax.set_title(<span class="code-string">"Ventas por Linea de Producto"</span>)
ax.set_xlabel(<span class="code-string">"Total de Ventas (USD)"</span>)
plt.tight_layout()
plt.savefig(<span class="code-string">"ventas_por_producto.png"</span>)`,
        explanation: 'Matplotlib permite crear graficos de alta calidad. plot(kind="barh") genera barras horizontales, ideales cuando los nombres de las categorias son largos. savefig() exporta el grafico como imagen PNG.'
    }
];

function showCodeStep(index, btn) {
    if (btn) {
        document.querySelectorAll('.code-step').forEach(s => s.classList.remove('active'));
        btn.classList.add('active');
    } else {
        const steps = document.querySelectorAll('.code-step');
        steps.forEach((s, i) => s.classList.toggle('active', i === index));
    }

    const data = codeSteps[index];
    document.getElementById('codeFileName').textContent = data.file;
    document.getElementById('codeContent').innerHTML = data.code;
    document.getElementById('codeExplanation').innerHTML = data.explanation;
}

// =============================================
// CONTADORES ANIMADOS
// =============================================
function animateCounters() {
    const counters = document.querySelectorAll('.stat-counter');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.target);
        const duration = 2000;
        const startTime = performance.now();
        counter.textContent = '0';

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing: ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(eased * target);

            counter.textContent = current.toLocaleString('es-CO');

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }

        requestAnimationFrame(updateCounter);
    });
}
