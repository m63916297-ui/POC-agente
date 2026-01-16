# POC-agente
Agente de recursos humanos usado para análisis de cesantías

Agente Virtual de Cesantías

```
# Agente Virtual de Cesantías

Este proyecto implementa un agente virtual inteligente diseñado para proporcionar información sobre una empresa y las cesantías de los clientes. El agente utiliza técnicas de procesamiento de lenguaje natural y búsqueda vectorial para ofrecer respuestas precisas y contextualizadas.

## Características Principales

- **Consulta de Cesantías**: Permite a los clientes consultar el saldo de sus cesantías mediante su número de documento.
- **Información Empresarial**: Responde preguntas sobre servicios, horarios, ubicación y políticas generales de la empresa.
- **Memoria de Conversación**: Mantiene el contexto de la conversación a través de threads.
- **Búsqueda Vectorial (RAG)**: Utiliza FAISS para búsquedas semánticas eficientes.

## Estructura del Proyecto

```
.
├── app.py                 # Aplicación principal y definición del agente
├── cesancias_causadas.xlsx # Base de datos de cesantías
├── models_llm.py          # Configuración de modelos de lenguaje
├── prompt.py              # Definición de prompts del sistema
├── vector_search.py       # Funcionalidad de búsqueda vectorial
├── tools.py               # Herramientas del agente
├── vector_db/             # Base de datos vectorial (índice FAISS y metadatos)
├── .env                   # Variables de entorno (no incluido en el repositorio)
└── requirements.txt       # Dependencias del proyecto
```

## Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-directorio>
   ```

2. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Crear un archivo `.env` con las siguientes variables:
   ```
   # Configuración Azure OpenAI
   deploy=<nombre-del-despliegue>
   version=<version-de-api>
   apikey=<tu-api-key>
   endpoint=<tu-endpoint>
   
   # Configuración Embeddings
   deploy_e=<nombre-del-despliegue-embeddings>
   version_e=<version-de-api-embeddings>
   apijey_e=<tu-api-key-embeddings>
   endpoint_e=<tu-endpoint-embeddings>
   
   # Configuración Groq
   ClientGroq=<tu-api-key-groq>
   ```

5. **Preparar la base de datos vectorial:**
   Asegúrate de tener los archivos `vector_db/cesantias.index` y `vector_db/cesantias_meta.json` en el directorio `vector_db/`.

## Uso

Para ejecutar el agente:

```bash
python app.py
```

El agente estará listo para recibir consultas sobre:
- Información de cesantías (requiere número de documento)
- Información general de la empresa

## Ejemplos de Uso

**Consulta de cesantías:**
```
Usuario: "Hola, quiero saber cuánto tengo en cesantías, mi cédula es 124473."
Agente: "Con gusto. Según el registro, tu saldo de cesantías actual es de 3,544,566.00, correspondiente al mes 5 del año 2025."
```

**Información de la empresa:**
```
Usuario: "¿Dónde queda la oficina principal?"
Agente: [Respuesta basada en la búsqueda vectorial]
```

## Arquitectura

El sistema está compuesto por:

1. **Agente Principal**: Implementado con LangGraph, gestiona el flujo de conversación.
2. **Herramientas**:
   - `validardoc`: Valida documentos y consulta información de cesantías.
   - `retreival_RAG`: Realiza búsquedas semánticas en la base de conocimiento.
3. **Modelos de Lenguaje**:
   - Azure OpenAI para generación de respuestas y embeddings.
   - Groq para clasificación de documentos.
4. **Base de Datos**:
   - Excel para datos de cesantías.
   - FAISS para búsqueda vectorial eficiente.

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.
```

