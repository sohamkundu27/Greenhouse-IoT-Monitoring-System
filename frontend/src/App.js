import React from "react";
import { Routes, Route } from "react-router-dom";
import SensorDashboard from "./SensorDashboard";
import DailyStats from "./DailyStats";

const App = () => {
    return (
        <Routes>
            <Route path="/" element={<SensorDashboard />} />
            <Route path="/daily-stats" element={<DailyStats />} />
        </Routes>
    );
};

export default App;