import { Routes, Route } from "react-router"
import Navbar from "../../components/Navbar/Navbar";
import HomePage from "../HomePage/HomePage";
import AuthPage from "../AuthPage/AuthPage";

export default function App() {
  return (
    <>
    <Navbar />
    <div style={{ marginTop: '60px' }}>
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/try"></Route>
        <Route path="/authenticate" element={<AuthPage />}></Route>
      </Routes>
    </div>
    </>
  );
}