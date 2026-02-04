# Dashboard Bot WhatsApp

Dashboard de gestión para conversaciones del bot de WhatsApp de Jugando y Educando.

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales

Edita el archivo `.env` con tus credenciales reales:

```bash
# WhatsApp API
WHATSAPP_TOKEN=tu_token_real
WHATSAPP_PHONE_ID=tu_phone_id_real
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en: http://localhost:8501

## 🧪 Testing con datos demo

### Crear conversaciones de prueba

```bash
python3 setup_demo_data.py
```

Esto creará 4 conversaciones de ejemplo:
- 1 conversación activa en modo bot
- 2 conversaciones escaladas a modo humano
- 1 conversación resuelta

### Limpiar datos de prueba

```bash
python3 cleanup_demo_data.py
```

## 📱 Funcionalidades

### Sidebar
- ✅ Lista de conversaciones ordenadas por actividad
- ✅ Filtros (Bot activo, Humano, Resueltas)
- ✅ Búsqueda por número de teléfono
- ✅ Indicadores visuales (🔴 escaladas, ⚪ normales)
- ✅ Preview del último mensaje

### Chat View
- ✅ Historial completo de mensajes
- ✅ Diferenciación visual (usuario/bot/humano)
- ✅ Enviar respuestas manuales
- ✅ Toggle modo bot (Activo/Pausado)
- ✅ Borrar conversación
- ✅ Auto-pausa del bot al responder

## 🎯 Uso

1. **Seleccionar conversación**: Click en una conversación del sidebar
2. **Ver historial**: Revisa todos los mensajes intercambiados
3. **Responder**: Escribe tu mensaje y haz click en "Enviar"
4. **Control del bot**:
   - **Bot Activo**: El bot responde automáticamente
   - **Bot Pausado**: Solo respuestas manuales
5. **Filtrar**: Usa los checkboxes para filtrar conversaciones
6. **Buscar**: Escribe un número para buscar conversaciones específicas

## 📁 Estructura del Proyecto

```
dashboard-bot-whatsapp/
├── app.py                      # Aplicación principal
├── setup_demo_data.py          # Script para crear datos de prueba
├── cleanup_demo_data.py        # Script para limpiar datos de prueba
├── config/
│   └── firebase.py             # Configuración Firebase
├── services/
│   ├── firebase_service.py     # Operaciones CRUD Firebase
│   └── whatsapp_service.py     # Envío de mensajes WhatsApp
├── components/
│   ├── sidebar.py              # Componente sidebar
│   └── chat_view.py            # Componente vista de chat
├── utils/
│   └── helpers.py              # Funciones auxiliares
├── .env                        # Variables de entorno
├── requirements.txt            # Dependencias Python
└── firebase-service-account.json  # Credenciales Firebase
```

## 🔧 Configuración

### Variables de entorno (.env)

```bash
# Firebase
FIREBASE_PROJECT_ID=whatsapp-bot-jye

# WhatsApp API
WHATSAPP_TOKEN=tu_token
WHATSAPP_PHONE_ID=tu_phone_id
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

### Firebase

Las credenciales de Firebase están en `firebase-service-account.json`.
El proyecto de Firebase es: `whatsapp-bot-jye`

## 📊 Estado del Proyecto

**Comandos Completados:**
- ✅ COMMAND 1: Project Setup
- ✅ COMMAND 2: Firebase Configuration
- ✅ COMMAND 3: Firebase Service Layer
- ✅ COMMAND 4: WhatsApp Service
- ✅ COMMAND 5: Sidebar Component
- ✅ COMMAND 6: Chat View Component
- ✅ COMMAND 7: Main App Integration
- ✅ COMMAND 8: Styling & Polish

**Pendientes:**
- ⏳ COMMAND 9: Bot Webhook Integration
- ⏳ COMMAND 10: Streamlit Cloud Deploy

## 🛠️ Desarrollo

### Testing Local

```bash
# Ejecutar con datos demo
python3 setup_demo_data.py
streamlit run app.py

# Limpiar cuando termines
python3 cleanup_demo_data.py
```

### Multi-tab Support

La aplicación soporta múltiples pestañas/ventanas. Cada pestaña mantiene su propio estado de selección.

## 📝 Notas

- El bot se pausa automáticamente cuando un humano envía un mensaje
- Los mensajes se guardan en Firebase aunque WhatsApp API no esté configurado
- Usa el modo "Bot Pausado" para conversaciones que requieren atención manual
- Marca conversaciones como "Resueltas" cuando ya no requieren seguimiento

## 👨‍💻 Autor

Desarrollado por Alejo para Jugando y Educando
