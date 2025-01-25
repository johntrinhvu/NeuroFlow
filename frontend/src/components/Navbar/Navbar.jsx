import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <div className="flex justify-center">
            <nav className="rounded-2xl fixed px-4 h-[52px] items-center top-0 mt-4 w-9/12 max-w-[1070px] flex justify-between border-slate-400 bg-slate-50 border">
                <span>
                    <Link to="/" className="">
                        <h1 className="font-semibold text-slate-800 tracking-wide">Home</h1>
                    </Link>
                </span>
                <span>
                    <Link to="/try">
                        <button className="bg-violet-600 border border-violet-900 rounded-lg text-white px-4 tracking-wide py-0.5">
                            Try it!
                        </button>
                    </Link>
                </span>
            </nav>
        </div>
    );
}