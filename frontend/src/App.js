import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ItemDetail from "./components/ItemDetail";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/item/:id" element={<ItemDetail />} />
            </Routes>
        </Router>
    );
}

export default App;