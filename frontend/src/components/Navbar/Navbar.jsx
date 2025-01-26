import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { FaBars, FaCaretDown } from "react-icons/fa";
import { jwtDecode } from "jwt-decode";
import Logo from "../../assets/logo.png";

export default function Navbar() {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    async function handleSignOut() {
        const token = localStorage.getItem("token");
        if (!token) {
            console.error("No token found");
            return;
        }
    
        try {
            const response = await fetch("http://localhost:8000/users/logout", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });
    
            if (!response.ok) {
                throw new Error("Failed to log out");
            }
    
            console.log("Logout successful");
            localStorage.removeItem("token");
            window.location.reload(); // Optionally redirect or reload the page
        } catch (error) {
            console.error("Logout error:", error);
        }
    }
    

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            try {
                const decoded = jwtDecode(token);
                console.log("decoded token: ", decoded);
                setUser(decoded); // Assuming the token contains the user's info
            } catch (error) {
                console.error("Invalid token", error);
                localStorage.removeItem("token"); // Remove invalid token
            }
        }
    }, []);

    return (
        <div className="flex justify-center">
            <nav className="rounded-2xl fixed px-4 h-[52px] items-center top-0 mt-4 w-9/12 max-w-[1070px] flex justify-between border-violet-400 bg-slate-50 border">
                <Link to="/" className="">
                    <div className="flex gap-0.5 items-center">
                        <span className="">
                            <img src={Logo} alt="logo" className="h-8" />
                        </span>
                        <span>
                            <h1 className="font-semibold text-slate-800 tracking-wide text-2xl">NeuroFlow</h1>
                        </span>
                    </div>
                </Link>
                <div className="flex gap-4">
                    {/* Mobile dropdown menu */}
                    <div className="block md:hidden mt-1">
                        <button onClick={toggleDropdown} className="text-slate-800">
                            <FaBars size={20} />
                        </button>
                        {isDropdownOpen && (
                            <div className="absolute right-0 mt-2 w-48 bg-slate-50 border rounded-lg shadow-lg">
                                {user ? (
                                    <button onClick={handleSignOut} className="transition ease-in-out hover:bg-slate-100 block px-4 py-2 text-slate-800 w-full text-left">Sign Out</button>
                                ) : (
                                    <Link to="/login" className="transition ease-in-out hover:bg-slate-100 block px-4 py-2 text-slate-800">Sign In</Link>

                                )}
                                <Link to="/try" className="transition ease-in-out hover:bg-slate-100 block px-4 py-2 text-slate-800">Try NeuroFlow</Link>
                            </div>
                        )}
                    </div>
                    <div className="hidden md:flex gap-4">
                        <Link to="/try">
                            <button className="transition ease-in-out hover:bg-violet-700 bg-violet-600 border border-violet-900 rounded-lg text-white px-4 tracking-wide py-0.5">
                                Try it!
                            </button>
                        </Link>
                        {user ? (
                            <div className="relative">
                                <button
                                    onClick={toggleDropdown}
                                    className="flex items-center rounded-lg text-slate-800 mt-0.5 -ml-2 -mr-2"
                                >
                                    <FaCaretDown size={20} />
                                </button>
                                {isDropdownOpen && (
                                    <div className="absolute right-0 mt-2 w-48 bg-slate-50 border rounded-lg shadow-lg">
                                        <button
                                            onClick={handleSignOut}
                                            className="block w-full text-left px-4 py-2 hover:bg-slate-100 text-slate-800"
                                        >
                                            Sign Out
                                        </button>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="flex border rounded-lg text-slate-800 border-violet-200">
                                <Link to="/login" className="transition ease-in-out hover:bg-slate-100 px-4 py-0.5">
                                    <button>
                                        Sign In
                                    </button>
                                </Link>
                                <span className="border border-violet-200">
                                </span>
                                <Link to="/signup" className="transition ease-in-out hover:bg-slate-100 px-4 py-0.5">
                                    <button>
                                        Sign Up
                                    </button>
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </nav>
        </div>
    );
}