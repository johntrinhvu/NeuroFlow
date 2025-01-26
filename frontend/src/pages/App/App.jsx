import { Routes, Route } from "react-router"
import Navbar from "../../components/Navbar/Navbar";
import HomePage from "../HomePage/HomePage";
import LoginPage from "../LoginPage/LoginPage";
import SignupPage from "../SignupPage/SignupPage";

export default function App() {
  return (
    <>
    <Navbar />
    <div style={{ marginTop: '60px' }}>
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/try"></Route>
        <Route path="/login" element={<LoginPage />}></Route>
        <Route path="/signup" element={<SignupPage />}></Route>
      </Routes>
    </div>
    </>
  );
}