import { Routes, Route } from "react-router"
import { UserProvider } from "../../contexts/UserContext/UserContext";
import Navbar from "../../components/Navbar/Navbar";
import HomePage from "../HomePage/HomePage";
import LoginPage from "../LoginPage/LoginPage";
import SignupPage from "../SignupPage/SignupPage";
import TryPage from "../TryPage/TryPage";
import ReportPage from "../ReportPage/ReportPage";
import ProfilePage from "../ProfilePage/ProfilePage";

export default function App() {
  return (
    <UserProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/try" element={<TryPage />}></Route>
        <Route path="/login" element={<LoginPage />}></Route>
        <Route path="/signup" element={<SignupPage />}></Route>
        <Route path="/users/:userId/:postId" element={<ReportPage />}></Route>
        <Route path="/users/:userId" element={<ProfilePage />}></Route>
      </Routes>
    </UserProvider>
  );
}