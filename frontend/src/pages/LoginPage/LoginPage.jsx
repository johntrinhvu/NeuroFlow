import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import './AuthPage.css';
import SignInForm from '../../components/SignInForm/SignInForm';
import Logo from '../../assets/logo.png';

export default function AuthPage() {
  return (
    <div className="mt-24 page-wrapper">
      <header className="flex justify-center items-center mt-6">
        <img src={ Logo } alt="NeuroFlowLogo" className="w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 lg:w-48 lg:h-48" />
      </header>
      <main>
        <section className="content-wrapper -mt-14">
            <SignInForm />
            <p className="other-page">
                Don't have an account yet?  
                <Link to="/signup" className="other-page-link">Sign Up</Link>
            </p>
        </section>
      </main>
      <footer className="oai-footer">
        <p className="footer-text">Created by: Abhay Singh, Andrew Ho, Dylan Tran, and John Vu</p>
      </footer>
    </div>
  );
}