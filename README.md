<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/RSA%20Encryption-2C3E50?style=for-the-badge&logo=letsencrypt&logoColor=white" alt="RSA">
</p>

# 🔐 Nuncius

**Nuncius** is an end-to-end encrypted, real-time CLI chat application built from the ground up with custom RSA cryptography and Apache Kafka for distributed message streaming.

> *"Nuncius"* — Latin for "messenger"

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔒 **End-to-End Encryption** | Custom RSA implementation with 1024-bit keys — messages are encrypted on the sender's device and can only be decrypted by the intended recipient |
| ⚡ **Real-Time Messaging** | Apache Kafka powers instantaneous, pub/sub message delivery across all connected clients |
| 🖥️ **Interactive CLI** | Beautiful terminal interface using `curses` with live updates, header bar, and typing indicator |
| 👥 **Multi-User Support** | Scalable architecture handles multiple concurrent users with real-time presence notifications |
| 🔑 **Public Key Exchange** | Automatic public key distribution when users join — new keys are broadcast to all clients instantly |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                           Client Application                          │
├─────────────────┬────────────────────────────────────────────────────┤
│   CLI (curses)  │  Real-time terminal UI with input handling        │
│   Producer      │  Encrypts & publishes messages to Kafka            │
│   Consumer      │  Subscribes to Kafka topic & decrypts messages     │
│   Listener      │  Maintains socket connection to auth server        │
│   Encryption    │  RSA key generation, encrypt/decrypt operations    │
└─────────────────┴────────────────────────────────────────────────────┘
           │                                    │
           │ Socket (auth, key exchange)        │ Kafka (messages)
           ▼                                    ▼
    ┌──────────────┐                   ┌──────────────────┐
    │  Auth Server │                   │   Kafka Broker   │
    │  (Python)    │                   │   (localhost)    │
    └──────────────┘                   └──────────────────┘
    • User authentication               • Message streaming
    • Public key registry               • Topic: "messages"
    • Online presence tracking          • Multi-partition support
```

---

## 🔐 Cryptography

### RSA Implementation

This project features a **custom RSA implementation** (not using pre-built crypto libraries) to demonstrate understanding of asymmetric encryption:

```python
# Key Generation (encryption.py)
p = randprime(2**511, 2**512)    # 512-bit prime
q = randprime(2**512, 2**513)    # 513-bit prime
n = p * q                         # 1024-bit modulus
phi = (p - 1) * (q - 1)
e, d = choose_ed(phi)            # Public/private exponent pair
```

**Security Features:**
- **1024-bit RSA keys** generated using cryptographically secure random primes
- **Per-recipient encryption** — each message is encrypted individually for every online user
- **Message signing capability** for future authentication features
- Private keys **never leave the client device**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Apache Kafka running locally
- Network access between clients and server

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nuncius.git
cd nuncius

# Install dependencies
pip install -r requirements.txt
```

### Running

**1. Start the Auth Server:**
```bash
cd server
python auth.py
```

**2. Start Kafka** (if not already running):
```bash
# Using Docker
docker run -d --name kafka \
  -p 9092:9092 \
  apache/kafka:latest
```

**3. Launch the Client:**
```bash
cd client
python main.py
```

---

## 📁 Project Structure

```
nuncius/
├── client/
│   ├── cli.py           # Curses-based terminal UI
│   ├── consumer.py      # Kafka consumer (decrypt & display)
│   ├── producer.py      # Kafka producer (encrypt & send)
│   ├── listener.py      # Auth server socket listener
│   ├── encryption.py    # Custom RSA implementation
│   ├── keys.py          # Public key management
│   └── constants.py     # Configuration values
├── server/
│   ├── auth.py          # Multi-threaded auth server
│   └── users.json       # User credentials store
└── requirements.txt
```

---

## 🛠️ Technical Skills Demonstrated

| Category | Technologies & Concepts |
|----------|------------------------|
| **Cryptography** | RSA algorithm, prime generation, modular arithmetic, public key infrastructure |
| **Distributed Systems** | Apache Kafka, pub/sub messaging, event streaming |
| **Networking** | Socket programming, TCP connections, JSON protocol design |
| **Concurrency** | Multi-threading (Python `threading`), async I/O, producer/consumer pattern |
| **Systems Programming** | Terminal UI with `curses`, low-level I/O handling |
| **Security** | End-to-end encryption, key exchange protocols, secure authentication |
