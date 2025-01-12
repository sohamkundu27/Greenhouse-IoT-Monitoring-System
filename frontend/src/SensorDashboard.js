import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; 
import axios from 'axios';

const SensorDashboard = () => {
    const [sensorData, setSensorData] = useState(null); // For latest sensor data

    useEffect(() => {
        const fetchData = () => {
            axios.get('http://localhost:8000/api/sensors/')
                .then(response => {
                    const allData = response.data;
                    if (allData.length > 0) {
                        setSensorData(allData[allData.length - 1]); // Set the latest data
                    }
                })
                .catch(error => console.error('Error fetching sensor data:', error));
        };

        // Fetch data initially and then every 60 seconds
        fetchData();
        const interval = setInterval(fetchData, 60000); // 60000 ms = 1 minute

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    return (
        <div className="dashboard">
            {sensorData ? (
                <div className="sensor-grid">
                    <h1 className="dashboard-title">Current Greenhouse Status</h1>
                    <div className="sensor-row sensor-header">
                        <div className="sensor-item">Temperature</div>
                        <div className="sensor-item">Humidity</div>
                        <div className="sensor-item">Water Level</div>
                        <div className="sensor-item">Rain</div>
                        <div className="sensor-item">Light/Dark</div>
                    </div>

                    <div className="sensor-row">
                        <div className="sensor-item">{sensorData.temperature}</div>
                        <div className="sensor-item">{sensorData.humidity}</div>
                        <div className="sensor-item">{sensorData.water_level}%</div>
                        <div className="sensor-item">{sensorData.rain ? 'Yes' : 'No'}</div>
                        <div className="sensor-item">{sensorData.light ? 'Light' : 'Dark'}</div>
                    </div>
                </div>
            ) : (
                <p>Loading sensor data...</p>
            )}
            <div className="button-container">
                <Link to="/daily-stats">
                    <button className="back-button">View High/Low Temperatures</button>
                </Link>
            </div>
        </div>
    );
};

export default SensorDashboard;