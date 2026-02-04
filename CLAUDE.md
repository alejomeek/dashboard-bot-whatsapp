# Dashboard Bot WhatsApp - Project Specifications

## 🎯 Project Overview

**Goal:** Build a Streamlit dashboard to manage WhatsApp bot conversations, allowing manual intervention when needed.

**User:** Solo developer (Alejo) - no login required  
**Bot:** WhatsApp Business API bot for Jugando y Educando  
**Deployment:** Streamlit Cloud (free tier)

---

## 📊 Tech Stack

- **Frontend:** Streamlit (Python)
- **Database:** Firebase Firestore (new project: `whatsapp-bot-jye`)
- **WhatsApp API:** Existing bot-whatsapp webhook
- **Deploy:** Streamlit Cloud
- **Notifications:** Visual badges (Telegram later)

---

## 🗄️ Firebase Structure

### Project: `whatsapp-bot-jye`

```
conversations/
  {phoneNumber}/                    # e.g., "+573174537055"
    mode: "bot" | "human"            # Who is responding
    status: "active" | "resolved"    # Conversation state
    lastMessage: timestamp
    escalatedAt: timestamp | null    # When escalated
    messages: [                      # Array of messages
      {
        from: "user" | "bot" | "human"
        text: string
        timestamp: timestamp
        messageId: string (WhatsApp ID)
      }
    ]
    
escalations/
  {escalationId}/                   # Auto-generated ID
    phoneNumber: string
    reason: string                  # Why escalated
    message: string                 # Last user message
    timestamp: timestamp
    resolved: boolean
```

---

## 🎨 UI Specifications

### Layout: Sidebar + Main

```
┌─────────────────┬──────────────────────────────────┐
│   SIDEBAR       │         MAIN PANEL               │
│   (30%)         │         (70%)                    │
├─────────────────┼──────────────────────────────────┤
│                 │                                  │
│ 🔴 +57 317...   │  Conversación: +57 317 453 7055  │
│    "Necesito... │  ─────────────────────────────── │
│    11:30 AM     │                                  │
│    [Bot Pausado]│  👤 Cliente (11:25 AM)           │
│                 │  "Busco rompecabezas"            │
│ ⚪ +57 300...   │                                  │
│    "Gracias"    │  🤖 Bot (11:25 AM)               │
│    10:15 AM     │  "Aquí tienes opciones..."       │
│                 │                                  │
│ ⚪ +57 311...   │  👤 Cliente (11:30 AM)           │
│    "Perfecto"   │  "Necesito factura 12345"        │
│    09:45 AM     │                                  │
│                 │  🤖 Bot (11:30 AM)               │
│ [+ Nueva]       │  "Un asesor te contactará"       │
│                 │  ─────────────────────────────── │
│ Filtros:        │                                  │
│ ☑ Bot activo    │  Modo: [🔴 Bot Pausado]         │
│ ☑ Humano        │                                  │
│ ☐ Resueltas     │  ┌────────────────────────────┐ │
│                 │  │ Escribe tu respuesta...    │ │
│ 🔍 Buscar...    │  │                            │ │
│                 │  └────────────────────────────┘ │
│                 │  [Enviar] [Reactivar Bot]       │
│                 │  [🗑️ Borrar Conversación]       │
└─────────────────┴──────────────────────────────────┘
```

### Visual Indicators

**Sidebar Conversation Item:**
- 🔴 Red dot = Needs attention (escalated, mode=human)
- ⚪ White dot = Normal (mode=bot)
- Badge number = Unread messages (optional later)
- Bold text = Unread/escalated
- Gray text = Resolved

**Main Panel:**
- 👤 User messages (left-aligned, gray bubble)
- 🤖 Bot messages (right-aligned, blue bubble)
- 🧑 Human messages (right-aligned, green bubble)

---

## ⚙️ Features Breakdown

### MVP Features (Must Have)

1. **View Conversations**
   - List all conversations in sidebar
   - Order by lastMessage (newest first)
   - Show phone number, preview, timestamp

2. **Conversation Detail**
   - Full message history
   - Scroll to see all messages
   - Visual distinction user/bot/human

3. **Manual Response**
   - Text input field
   - Send button
   - Auto-pause bot when human sends message

4. **Bot Control**
   - Toggle: "Bot Pausado" / "Bot Activo"
   - Visual indicator of current mode
   - Changes conversation.mode in Firebase

5. **Multi-Conversation**
   - Open 2-3 conversations in separate tabs/windows
   - Each tab maintains independent state

6. **Filters**
   - Bot activo (mode=bot)
   - Humano respondiendo (mode=human)
   - Resueltas (status=resolved)

7. **Search**
   - Search by phone number
   - Simple text match

8. **Delete Conversation**
   - Manual delete button
   - Confirmation dialog
   - Removes from Firebase

### Nice-to-Have (Later)

- Response templates (quick replies)
- Telegram notifications
- Statistics dashboard
- Export conversation history
- Mark as unread

---

## 🔌 Integration with Existing Bot

### bot-whatsapp Webhook Changes Needed

**File:** `api/webhook.js`

**Before processing message:**
```javascript
// Check if conversation is in "human" mode
const conversation = await firebase
  .collection('conversations')
  .doc(phoneNumber)
  .get();

if (conversation.exists && conversation.data().mode === 'human') {
  console.log('[WEBHOOK] Human is handling - bot paused');
  return res.status(200).send('OK');
}

// Continue with bot processing...
```

**When escalation needed:**
```javascript
// Mark conversation as escalated
await firebase.collection('conversations').doc(phoneNumber).set({
  mode: 'human',
  status: 'active',
  escalatedAt: new Date(),
  lastMessage: new Date()
}, { merge: true });

// Add to escalations collection
await firebase.collection('escalations').add({
  phoneNumber: phoneNumber,
  reason: 'Bot cannot help',
  message: userMessage,
  timestamp: new Date(),
  resolved: false
});
```

**When saving messages:**
```javascript
// Add message to conversation history
await firebase.collection('conversations').doc(phoneNumber).update({
  messages: admin.firestore.FieldValue.arrayUnion({
    from: 'user',
    text: userMessage,
    timestamp: new Date(),
    messageId: webhookMessageId
  }),
  lastMessage: new Date()
});
```

---

## 📦 Project Structure

```
dashboard-bot-whatsapp/
├── CLAUDE.md                    # This file
├── .env                         # Environment variables
├── .gitignore
├── requirements.txt             # Python dependencies
├── app.py                       # Main Streamlit app
├── firebase-service-account.json
├── config/
│   └── firebase.py              # Firebase initialization
├── components/
│   ├── sidebar.py               # Conversation list sidebar
│   ├── chat_view.py             # Main chat display
│   └── filters.py               # Filter controls
├── services/
│   ├── firebase_service.py      # Firebase CRUD operations
│   └── whatsapp_service.py      # Send WhatsApp messages
└── utils/
    └── helpers.py               # Helper functions
```

---

## 🔐 Environment Variables

**File:** `.env`

```bash
# Firebase
FIREBASE_PROJECT_ID=whatsapp-bot-jye

# WhatsApp API (from bot-whatsapp project)
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

---

## 📋 Step-by-Step Commands

### COMMAND 1: Project Setup
**Goal:** Initialize project structure and dependencies

**Tasks:**
1. Create directory structure
2. Create `.gitignore`
3. Create `requirements.txt` with dependencies:
   - streamlit
   - firebase-admin
   - python-dotenv
   - requests
4. Create `.env` file template
5. Move `firebase-service-account.json` to project root

**Validation:** Run `pip install -r requirements.txt` successfully

---

### COMMAND 2: Firebase Configuration
**Goal:** Initialize Firebase connection

**Tasks:**
1. Create `config/firebase.py`
2. Initialize Firebase Admin SDK
3. Test connection to Firestore
4. Create helper function to get db instance

**Validation:** Can read/write test document to Firebase

---

### COMMAND 3: Firebase Service Layer
**Goal:** CRUD operations for conversations

**Tasks:**
1. Create `services/firebase_service.py`
2. Functions:
   - `get_all_conversations()` → List of conversations
   - `get_conversation(phone_number)` → Single conversation with messages
   - `update_conversation_mode(phone_number, mode)` → Change bot/human
   - `add_message(phone_number, from, text)` → Add message to array
   - `delete_conversation(phone_number)` → Remove conversation
   - `mark_resolved(phone_number)` → Change status to resolved

**Validation:** Test each function with sample data

---

### COMMAND 4: WhatsApp Service
**Goal:** Send messages via WhatsApp API

**Tasks:**
1. Create `services/whatsapp_service.py`
2. Function: `send_message(phone_number, text)`
3. Use WhatsApp Cloud API
4. Handle errors gracefully

**Validation:** Send test message successfully

---

### COMMAND 5: Sidebar Component
**Goal:** Display conversation list

**Tasks:**
1. Create `components/sidebar.py`
2. Render conversation list with:
   - Phone number
   - Last message preview (30 chars)
   - Timestamp
   - Status indicator (🔴/⚪)
   - Click to select
3. Add filters (checkboxes)
4. Add search input

**Validation:** Displays conversations from Firebase

---

### COMMAND 6: Chat View Component
**Goal:** Display and interact with single conversation

**Tasks:**
1. Create `components/chat_view.py`
2. Display message history:
   - Format user/bot/human messages
   - Show timestamps
   - Scroll to bottom
3. Text input for reply
4. Send button
5. Bot mode toggle
6. Delete conversation button

**Validation:** Can view messages and send replies

---

### COMMAND 7: Main App Integration
**Goal:** Combine all components into working app

**Tasks:**
1. Create `app.py`
2. Set page config (wide layout, title)
3. Initialize Firebase
4. Render sidebar
5. Render chat view based on selection
6. Handle multi-tab support (experimental_rerun)

**Validation:** Full app works locally

---

### COMMAND 8: Styling & Polish
**Goal:** Improve UI/UX

**Tasks:**
1. Add custom CSS for chat bubbles
2. Improve spacing and margins
3. Add loading spinners
4. Add success/error messages
5. Format timestamps nicely

**Validation:** App looks professional

---

### COMMAND 9: Bot Webhook Integration
**Goal:** Update bot to work with dashboard

**Tasks:**
1. Add Firebase write to bot-whatsapp webhook
2. Check conversation mode before responding
3. Save all messages to Firebase
4. Handle escalations

**File to modify:** `/Users/alejomeek/Documents/bot-whatsapp/api/webhook.js`

**Validation:** Bot pauses when mode=human

---

### COMMAND 10: Streamlit Cloud Deploy
**Goal:** Deploy to production

**Tasks:**
1. Create `secrets.toml` for Streamlit Cloud
2. Add Firebase service account to secrets
3. Add environment variables
4. Push to GitHub
5. Connect to Streamlit Cloud
6. Deploy

**Validation:** App accessible via public URL

---

## 🧪 Testing Checklist

**Before Deploy:**
- [ ] Can view conversations
- [ ] Can see full message history
- [ ] Can send manual response
- [ ] Message appears in WhatsApp
- [ ] Bot pauses when mode=human
- [ ] Can reactivate bot
- [ ] Bot resumes responding
- [ ] Filters work correctly
- [ ] Search finds conversations
- [ ] Can delete conversation
- [ ] Multi-tab works (open 2 conversations)
- [ ] Timestamps display correctly
- [ ] Status indicators accurate (🔴/⚪)

---

## 🚀 Deployment Instructions

### Streamlit Cloud Setup

1. **Prepare GitHub Repo:**
   ```bash
   cd /Users/alejomeek/Documents/dashboard-bot-whatsapp
   git init
   git add .
   git commit -m "Initial dashboard commit"
   git remote add origin https://github.com/alejomeek/dashboard-bot-whatsapp.git
   git push -u origin main
   ```

2. **Create Streamlit Account:**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub

3. **Deploy App:**
   - Click "New app"
   - Select repository: `dashboard-bot-whatsapp`
   - Main file: `app.py`
   - Advanced settings → Secrets:
     ```toml
     [firebase]
     type = "service_account"
     project_id = "whatsapp-bot-jye"
     private_key_id = "772e6e9ad4e7d688a617251ceab4938070e57cff"
     private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAjcEEF2nSgVVu\n8KteM7/uO6zh3bHqvAh4HdK8XVUHqhvMO+Z8rfAhy0a5NJZ7zDpM7DmZGwHW62zq\nxQPdYGiZ7Hm1+BC//EufT7ISqhQKKlXTksA9GCZsGqd7LAk+q4ANQWhZZPucGmIT\n6SpYThd3wJf2NLtsdpXnoLdNj4DoFl5qRSytqrgZiV/E3rMvKNulJBlgT59vLyET\nja8KzZOFkLnV6rRjdLmuXVAMkuEcaIUDSvAD4zcRRdyOnCc8fDrqfDCVcXo0Z2Qt\n3+gcYeMmmZHWxJG9aZgVwMwqir7G9dD6MUb65NHAti/oHxlIIy8+ABJSxCuLNM94\nC/fDrgEdAgMBAAECggEAK0UfmQMG64BXWb8ZD2n7KTa9TqNiWiDHmXCAPQaPN1H1\nfbN/Q8jVk86JldB4uZinCEa0WdDNHMYaW3aK/Aowb1iJ8EeuwenY95Ox7UpNhwxE\n7a7GZuRArB3gQYhfincBJ1lpsN8FwKpYHGfS9XWVBfrgWzo13PWYEa1Wy8Xh/qU1\nj/YxcvsaLBn2MovIWnynPWb3VK2gmDcofr8FGyqYsxeh8mWahjr+fABy0pRHx8k4\nqtjo+jXvLppkkSqS/uI3u1iHagrOynnb0X8uSjEz+m6IlIa5UNgxnapm9GUHdnoP\nB+80WCY5LSzCfLKk06r+UqwMfiiVkwhfgY9cM1noGQKBgQD85CcljZ/P++5okTyb\nXO/7hBtcJSU7NnLZGEBIA7tLbkJ9HA91H/IX8emi+hzo/5Xm6KXJHX+EB7FNorEY\nAgTfW4ujI1/2cr+rn6XA9kH83X3E4fwHMTJ1ZkJxgS1ScF0H7/seHrfOAb+DIzFJ\nMyeG/WUmyxVqttbvpPiaAZNyxQKBgQDC67gmLSlNVyuZD5uX+aD0gCqTMndcpCFf\nB0q18Ax9uxxHTYoSMo60Z8BS8BE4o/k4nAGTH3DvEFCX2LiJvz2Y3b5/rV2kFVvx\nxfyWQvnKDbzVibIvdgEgxGVgnUaIWJqpmnMQW3bSCHe1YPi4VghKUUcGEeH+Vzh2\nLX6LME3aeQKBgA4rWmYoQUQOAZWqTZMG6gtVo5LOIf/nVRgE29UtIFlhnCgWYmdV\nmuLskwKmsOf9KhD+CAv0syhapfyLmRCXTF6XaoOBf+b3FvYuw8LECX55iop1fwGI\nKCObzy0856Uu1oeTUqalYfcQ8gIO/rvzOcu+duRtjI2mIPTccXFvlSthAoGBAL4y\nnqz50lx6W7tuBGhmGA2cZm7dhqUqLrn4dolTpAynoK9e1QRuutsEhiEnydYYAp6f\nc9Xojx1nMQ0KVv9qUaOxdCpHs6Dhiqc/hvnkfrMPdpxzUSCIqA8eNMHylZmDw98N\nK4vhg+7sfkrJRckxgcNqzb/5gSjaWOjP+bO9vaoZAoGAJOEvjNOU+hl2iB/Sha6l\neiMsKd8aJtqlQIHW8sNvYUTbRQRS0GQ2/18Pd5ebaLvAsOActBllXJfKn6LxiG2T\nN0BecyNsxv2kq6GJMzE3pu611XDNNOaJJhSZtbCczjwRRv9CnqLn91TmTrqo7CZU\n60Ez5gblps/ar2+R1dK6yXE=\n-----END PRIVATE KEY-----\n"
     client_email = "firebase-adminsdk-fbsvc@whatsapp-bot-jye.iam.gserviceaccount.com"
     
     [whatsapp]
     token = "your_whatsapp_token_here"
     phone_id = "your_phone_id_here"
     ```

4. **Deploy:** Click "Deploy"

---

## 📞 Support & Next Steps

**After MVP is working:**
1. Add Telegram notifications
2. Add response templates
3. Add conversation analytics
4. Multi-agent support (if needed)

**Questions/Issues:**
- Return to main chat for strategic decisions
- Execute commands incrementally
- Test after each command before proceeding

---

## ✅ Success Criteria

**Dashboard is successful when:**
- ✅ Can see all active conversations
- ✅ Can manually respond to customers
- ✅ Bot pauses when human intervenes
- ✅ Can manage 2-3 conversations simultaneously
- ✅ Deployed and accessible 24/7
- ✅ Stable (no crashes, handles errors gracefully)

---

**Ready to start COMMAND 1!** 🚀
