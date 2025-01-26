import { Routes, Route } from "react-router"
import Navbar from "../../components/Navbar/Navbar";
import HomePage from "../HomePage/HomePage";
import LoginPage from "../LoginPage/LoginPage";
import SignupPage from "../SignupPage/SignupPage";
import TryPage from "../TryPage/TryPage";
import ReportPage from "../ReportPage/ReportPage";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/try" element={<TryPage />}></Route>
        <Route path="/login" element={<LoginPage />}></Route>
        <Route path="/signup" element={<SignupPage />}></Route>
        <Route path="/users/:userId/:postId" element={<ReportPage />}></Route>
      </Routes>
    </>
  );
}