import { Routes, Route } from "react-router"
import Navbar from "../../components/Navbar/Navbar";
import HomePage from "../HomePage/HomePage";

export default function App() {
  return (
    <>
    <Navbar />
    <div style={{ marginTop: '84px' }}>
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
      </Routes>
    </div>
    </>
  );
}