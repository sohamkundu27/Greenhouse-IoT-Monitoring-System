import React from "react";
import ReactDOM from "react-dom/client"; // Correct import for createRoot
import { BrowserRouter } from "react-router-dom"; // Import BrowserRouter
import "./index.css";
import App from "./App";

// Importing Bootstrap stylesheet
import "bootstrap/dist/css/bootstrap.min.css"; 

// Creating the root
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>
);