# Greenhouse IoT Monitoring System
 

---

# 🌿 Greenhouse Monitoring System

### **Project Purpose**
The **Greenhouse Monitoring System** is an IoT-based solution designed to monitor environmental conditions in a greenhouse or indoor space. Using real-time sensor data, the system helps optimize plant health and resource usage. It collects temperature, humidity, light intensity, and water-level data, processes it, and displays it on an interactive web dashboard.

This project showcases a combination of **hardware programming**, **cloud integration**, and **full-stack development**.

---

## **How It Works**
1. **Data Collection**:
   - A **Raspberry Pi** reads data from three sensors:
     - 🌡️ **DHT22**: Temperature and humidity sensor.
     - 💡 **LDR**: Light intensity sensor.
     - 📏 **HC-SR04**: Ultrasonic distance sensor for water level measurement.

2. **Data Processing**:
   - Sensor data is collected and processed in **C** on the Raspberry Pi for efficiency.

3. **Cloud Integration**:
   - The processed data is sent to **Azure IoT Hub**, where it is stored and prepared for retrieval.

4. **Backend**:
   - A **Django** backend fetches the real-time sensor data from Azure and exposes it via APIs.

5. **Frontend**:
   - A **React** web dashboard displays the data, featuring:
     - Real-time charts and visualizations.
     - Metrics for temperature, humidity, light levels, and water levels.

6. **Containerization**:
   - The Django backend and React frontend are **containerized using Docker** for ease of deployment.

---

## **System Diagram**
```
Sensors → Raspberry Pi (C) → Azure IoT Hub → Django API → React Dashboard
```

---

## **Tools, Frameworks, and Languages Used**

### **Hardware and Sensors**
- **Raspberry Pi** (Data collection and processing)
- **DHT22**: Temperature and humidity sensor
- **LDR**: Light sensor
- **HC-SR04**: Ultrasonic sensor for distance measurement

### **Languages**
- **C**: Sensor data collection and processing on the Raspberry Pi
- **Python**: Backend development with Django
- **JavaScript (React)**: Frontend development for real-time visualization

### **Cloud Tools**
- **Azure IoT Hub**: Real-time data storage and cloud processing
- **Azure App Services**: Deployment of the Django backend and React frontend

### **Containerization**
- **Docker**: Containerizing backend and frontend for consistent deployment

---

## **Features**
- 🌡️ **Real-Time Monitoring**: Temperature, humidity, light levels, and water levels displayed live.
- 📊 **Data Visualization**: Interactive charts and metrics for insights.
- ☁️ **Cloud Integration**: Data securely sent and stored on Azure IoT Hub.
- 🖥️ **User Dashboard**: Accessible dashboard built with React for monitoring and analysis.
- 🛠️ **Scalable and Portable**: Docker containers make the system easy to deploy anywhere.
